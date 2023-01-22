import cerebellum
from llm_fns import *

cerebellum = cerebellum.Cerebellum()
current_position, touch = cerebellum.move([-5, -5], 1, "continue")
while 1:

    # wait for speech to text --> text
    command = input("State a command: ")

    # create prompt <-- text, current position, touch
    command_type = classify_action_or_speech(command)
    if command_type == "speech":
        answer = reply_to_speech(command, current_position, touch)
        # speak answer
        print(answer)
    elif command_type == "action":
        coords, velocity, sot = generate_action(
            command, current_position, touch, action_examples
        )
        print(coords, velocity)

    for coord in coords:
        current_position, touch = cerebellum.move(coord, velocity, sot)
        if touch:
            print(reply_to_speech("why did you stop?", current_position, touch))
            break

    if not touch:
        print("How should I move now?")

# current_postion, touch = cerebellum.move([0, 5], 1, "continue")
# print("[brain] done", current_postion, touch)
# current_postion, touch = cerebellum.move([0, 0], 5, "stop")
# print("[brain] done", current_postion, touch)
