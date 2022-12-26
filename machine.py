from fsm import TocMachine

machine = TocMachine ( 
    states = [
        "user",
        "fetch",
        "random",
        "legalities",
        "oracle",
        "picture",
        "help",
        "foo"
    ],
    transitions = [
        {
            "trigger": "advance",
            "source": "user",
            "dest": "fetch",
            "conditions": "is_going_to_fetch",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "random",
            "conditions": "is_going_to_random",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "legalities",
            "conditions": "is_going_to_legalities",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "oracle",
            "conditions": "is_going_to_oracle",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "help",
            "conditions": "is_going_to_help",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "foo",
            "conditions": "is_going_to_foo",
        },
        {
            "trigger": "go_back",
            "source": [
                "fetch",
                "random",
                "legalities",
                "oracle",
                "picture",
                "help",
                "foo"
            ],
            "dest": "user"
        },
    ],
    initial = "user",
    auto_transitions = False,
    show_conditions = True,
)

def show_fsm():
    machine.get_graph().draw ( "fsm.png", prog = "dot", format = "png" )
    # return send_file ( "fsm.png", mimetype = "image/png" )


show_fsm()
