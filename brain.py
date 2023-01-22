import speech_recognition as sr

import cerebellum
from commands import (
    InvalidCommandError,
    check_is_command,
    check_is_confirmation,
    check_with_user,
    say,
)

r = sr.Recognizer()
mic = sr.Microphone()

cerebellum = cerebellum.Cerebellum()


commands = []
likely_commands = []

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
        audio_text = r.recognize_google(audio).lower()

        if likely_commands:
            command = likely_commands.pop()
            if check_is_confirmation(audio_text):
                say("Ok, let's do it")
                commands.append(command)
            else:
                say("Allright I am going to ignore that then")

        if check_is_command(audio_text):
            command = audio_text
            if not likely_commands:
                likely_commands.append(command)
                prompt = f"Did you meant to say: {command}? "
                say(prompt)

        # Add user friendliness
        # - Upon keyword - make the robot acknowledge
        # - Add buffer listening once we're in that mode ( people might take a
        # while to issue the command

    except InvalidCommandError:
        print("Ignoring text that is not a command")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )

    # wait for speech to text --> text

    # create prompt <-- text, current position, touch

    # ask LLM

    # exec output from LLM
    # speak
    # or motion

    # for loop over list of commands:

cerebellum.move([0, 1], 1, "continue")
current_postion, touch = cerebellum.move([0, 5], 1, "continue")
print("[brain] done", current_postion, touch)
current_postion, touch = cerebellum.move([0, 0], 5, "stop")
print("[brain] done", current_postion, touch)
