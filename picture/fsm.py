from transitions.extensions import GraphMachine

class TocMachine ( GraphMachine ):
    def __init__ ( self, **machine_configs ):
        self.machine = GraphMachine ( model = self, **machine_configs )

    def is_going_to_fetch ( self, event ):
        text = event.message.text
        return text.lower() == "go to fetch"

    def is_going_to_random ( self, event ):
        text = event.message.text
        return text.lower() == "go to random"

    def is_going_to_picture ( self, evnet ):
        text = event.message.text
        return text.lower() == "go to picture"

    def is_going_to_oracle ( self, event ):
        text = event.message.text
        return text.lower() == "go to oracle"

    def is_going_to_legalities ( self, event ):
        text = event.message.text
        return text.lower() == "go to legalities"

    def is_going_to_help ( self, event ):
        text = event.message.text
        return text.lower() == "go to help"

    def is_going_to_foo ( self, event ):
        text = event.message.text
        return text.lower() == "go to foo"

    def on_enter_fetch ( self, event ):
        print ( "I'm entering fetch" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_fetch ( self ):
        print ( "Leaving fetch" )

    def on_enter_random ( self, event ):
        print ( "I'm entering random" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_random ( self ):
        print ( "Leaving random" )

    def on_enter_picture ( self, event ):
        print ( "I'm entering picture" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_picture ( self ):
        print ( "Leaving picture" )

    def on_enter_oracle ( self, event ):
        print ( "I'm entering oracle" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_oracle ( self ):
        print ( "Leaving oracle" )

    def on_enter_legalities ( self, event ):
        print ( "I'm entering legalities" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_legalities ( self ):
        print ( "Leaving legalities" )

    def on_enter_help ( self, event ):
        print ( "I'm entering help" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_help ( self ):
        print ( "Leaving help" )

    def on_enter_foo ( self, event ):
        print ( "I'm entering foo" )

        reply_token = event.reply_token
        self.go_back()

    def on_exit_foo ( self ):
        print ( "Leaving foo" )
