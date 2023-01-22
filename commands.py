import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

while 1:

    with mic as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio = r.listen(source, phrase_time_limit=4)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # once we have exhausted the available calls
        # instead of `r.recognize_google(audio)`
        command = r.recognize_google(audio)
        validate_command(command)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(
                e
            )
        )
