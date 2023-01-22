import speech_recognition as sr

import cerebellum
from commands import say

r = sr.Recognizer()
mic = sr.Microphone()

cerebellum = cerebellum.Cerebellum()


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
        prompt = f"Did you meant to say: {command}? "
        say(prompt)

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
