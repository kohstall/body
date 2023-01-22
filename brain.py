import cerebellum
from llm_fns import *
import math
import random

cerebellum = cerebellum.Cerebellum()
current_position, touch = cerebellum.move([-5, -5], 1, "continue")
action_examples = base_action_examples
# current_position, touch = "[0, 0]", "False"


# class Cerebellum:
#     def __init__(self):
#         pass

#     def move(self, command, velocity, stop):
#         print(command, velocity, stop)
#         return command, False

# cerebellum = Cerebellum()


def speak(text):
    print(text)


while 1:

    command = input("State a command: ")

    actions, action_example = generate_action(
        command, current_position, touch, action_examples
    )
    if len(action_examples) > 5:
        action_examples.pop(0)
    action_examples.append(action_example)

    try:
        exec(actions)
    except Exception as e:
        print(what_went_wrong(actions, e))
