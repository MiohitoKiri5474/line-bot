from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

import time, scrython, json, requests
from PIL import Image
 
line_bot_api = LineBotApi ( settings.LINE_CHANNEL_ACCESS_TOKEN )
parser = WebhookParser ( settings.LINE_CHANNEL_SECRET )

ngrok_url = '7105-2001-b011-e009-31f7-a99e-900c-e0c9-cfe7.jp.ngrok.io'

def is_creature ( cards ):
    spt = cards.type_line().split ( ' ' )
    if len ( spt ) == 1:
        return spt[0] == 'Creature'
    return spt[0] == 'Creature' or ( spt[0] == 'Legendary' and spt[1][0] == 'Creature' )

def full_cards_information ( cards ):
    rpy = cards.name()
    if cards.reserved():
        rpy += '\t<Reserved>'
    rpy += '\n'
    if cards.type_line() != 'Land':
        rpy += cards.mana_cost() + '\n'
    rpy += cards.type_line() + '\n'
    rpy += cards.oracle_text()
    if is_creature ( cards ):
        rpy += '\n' + cards.power() + '/' + cards.toughness()
    return rpy

def storge_card_name ( uid, string ):
    with open ( uid + '.txt', 'w' ) as f:
        f.write ( string )
        f.close()

def get_card_name ( uid ):
    with open ( uid + '.txt', 'r' ) as f:
        res = f.read()
        f.close()
    return res

def fetch_card_check ( string ):
    spt = str ( string ).split ( ' ' )
    return spt[0].lower() == 'fetch'

def fetch_card_name ( string ):
    spt = str ( string ).split ( ' ' )
    res = ''
    for i in spt:
        if i != spt[0]:
            res += i + ' '
    return res

def legalities_card_check ( string ):
    spt = str ( string ).split ( ' ' )
    return spt [0].lower() == 'legalities'

def fetch_try ( name ):
    try:
        cards = scrython.cards.Named ( fuzzy = name )
        return cards
    except scrython.foundation.ScryfallError:
        return 'Failed to find cards, please provide card name more completely.'

def get_legalities ( cards ):
    rpy = 'Legalities of ' + cards.name() + ':\n'
    for i in cards.legalities():
        rpy += '    ' + i + ':'
        for j in range ( 17 - len ( i ) ):
            rpy += ' '
        if cards.legalities()[i] == 'legal':
            rpy += 'Legal'
        else:
            rpy += 'Not Legal'
        if i != 'premodern':
            rpy += '\n'

    return rpy

    

@csrf_exempt
def callback ( request ):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode ( 'utf-8' )
 
        try:
            events = parser.parse ( body, signature )
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance ( event, MessageEvent ):
                rpy = ''
                if event.message.text.lower() == 'foo':
                    rpy = TextSendMessage ( 'bar' )
                elif event.message.text.lower() == 'random':
                    cards = scrython.cards.Random()
                    print ( cards.name() )
                    storge_card_name ( event.source.user_id, cards.name() )

                    rpy = full_cards_information ( cards )
                elif event.message.text.lower() == 'oracle':
                    name = get_card_name ( event.source.user_id )
                    if name == '':
                        rpy = TextSendMessage ( '[Error] Previous result is not exist.' )
                    else:
                        cards = scrython.cards.Named ( fuzzy = name )
                        rpy = TextSendMessage ( full_cards_information ( cards ) )
                elif event.message.text.lower() == 'help':
                    rpy = 'How to use this line bot:\n\n'
                    rpy += 'random                         Get a random card and get it\'s informations.\n'
                    rpy += 'fetch [card name]              Get informations of [card name].\n'
                    rpy += 'legalities [card name (opt)]   Get legalities information of [card name].\n'
                    rpy += '                               If [card name] is not provided, the last time search result will be return.\n'
                    rpy += 'oracle                         Get card information last time search.\n'
                    rpy += 'picture                        Get card image last time search.\n'
                    rpy += 'help                           Show this help page.\n'
                    rpy += 'foo                            Test this bot, if you get \'bar\' for the reply, this bot works successfully.'

                    rpy = TextSendMessage ( rpy )
                elif fetch_card_check ( event.message.text ):
                    names = fetch_card_name ( event.message.text )
                    if names == '':
                        rpy = TextSendMessage ( 'You need provide a card name to fetch.' )
                    else:
                        cards = fetch_try ( names )
                        if type ( cards ) == str:
                            rpy = TextSendMessage ( cards )
                        else:
                            storge_card_name ( event.source.user_id, cards.name() )
                            rpy = full_cards_information ( cards )

                            rpy = [TextSendMessage ( full_cards_information ( cards ) ), ImageSendMessage ( original_content_url = cards.image_uris()['png'], preview_image_url = cards.image_uris()['png'] )]
                elif event.message.text.lower() == 'picture':
                    name = get_card_name ( event.source.user_id )
                    if name == "":
                        rpy = TextSendMessage ( '[Error] Previous result is not exist.' )
                    else:
                        cards = scrython.cards.Named ( fuzzy = name )
                        rpy = ImageSendMessage ( original_content_url = cards.image_uris()['png'], preview_image_url = cards.image_uris()['png'] )
                elif legalities_card_check ( event.message.text ):
                    names = fetch_card_name ( event.message.text )
                    if names == '':
                        cards = scrython.cards.Named ( fuzzy = get_card_name ( event.source.user_id ) )
                        rpy = TextSendMessage ( get_legalities ( cards ) )
                    else:
                        cards = fetch_try ( names )
                        if type ( cards ) == str:
                            rpy = TextSendMessage ( cards )
                        else:
                            storge_card_name ( event.source.user_id, cards.name() )
                            rpy = TextSendMessage ( get_legalities ( cards ) )
                else:
                    rpy = TextSendMessage ( '[Error] Unknown command, please try again.' )

                line_bot_api.reply_message ( event.reply_token, rpy )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
