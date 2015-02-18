from splash import *
from select import *
from round import *

roundnormal = Round('normal')
roundAI = Round('AI')
select = Select()

states = {"splash": Splash(),
          "select": select,
          "round": roundnormal,
          "roundAI": roundAI}

state = "splash"

while states[state].running:
    game = states[state]
    result = game.run()

    if result != None:
        if state == 'round':
            roundnormal.__init__('normal')
        elif state == 'roundAI':
            roundAI.__init__('AI')
        elif state == 'select':
            select.__init__()
        state = result
