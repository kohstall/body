import math
import random

import speech_recognition as sr

import cerebellum
from commands import say
from llm_fns import *

r = sr.Recognizer()
mic = sr.Microphone()

cerebellum = cerebellum.Cerebellum()
current_position, touch, mode = cerebellum.move([-5, -5], 3, "continue")
action_examples = base_action_examples
# current_position, touch = "[0, 0]", "False"


# class Cerebellum:
#     def __init__(self):
#         pass

#     def move(self, command, velocity, stop):
#         print(command, False)
#         return (command, False)


# cerebellum = Cerebellum()


def speak(text):
    say(text)
    return None


def validate_action(action_str):
    """
    Parse action_str to validate it is a well formed command for
    the exec method
    """


while 1:

    with mic as source:
        print("Listening for commands")
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio = r.listen(source, phrase_time_limit=4)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # once we have exhausted the available calls
        # instead of `r.recognize_google(audio)`
        command = r.recognize_google(audio)
        # prompt = f"Did you meant to say: {command}? "
        # say(prompt)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )

    #command = input("State a command: ")

    actions, action_example = generate_action(
        command, current_position, touch, action_examples
    )
    if len(action_examples) > 5:
        action_examples.pop(0)
    action_examples.append(action_example)

    for action in actions.split("\n"):
        try:
            out = None
            exec_action = f"out = {action}"
            print(exec_action)
            exec(exec_action)
            if out and len(out) > 1:
                current_position, touch, mode = out
                if mode == "stop" and touch == 1:
                    say("Ooops, what's that doing here?")
                    break
            print(current_position, touch, mode)
        except Exception as e:
            speak(what_went_wrong(actions, e))
