import cerebellum
from llm_fns import *

cerebellum = cerebellum.Cerebellum()
current_position, touch = cerebellum.move([0, 0], 1, "stop")
command = "Trace out a small square quickly."
while 1:

    # wait for speech to text --> text

    # create prompt <-- text, current position, touch
    command_type = classify_action_or_speech(command)
    if command_type == "speech":
        answer = reply_to_speech(command, current_position, touch)
        # speak answer
        print(answer)
    elif command_type == "action":
        coords, velocity, _ = generate_action(
            command, current_position, touch, action_examples
        )

    for coord in coords:
        current_position, touch = cerebellum.move(coord, velocity, "continue")
