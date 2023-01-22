import os
import random
import stat
import string

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

language = "en"


class InvalidCommandError(Exception):
    ...


def check_with_user(prompt, r, mic):
    """
    Asks the user to confirm a command based on the prompt
    """
    print("Checking with user")

    say(prompt)
    with mic as source:
        audio = r.listen(source, phrase_time_limit=4)

    audio_text = r.recognize_google(audio).lower()
    print(f"Confirmation was {audio_text}")
    if "yes" in audio_text:
        return True
    return False


def check_is_confirmation(audio_text):
    """
    Raises an InvalidCommandError if the audio text is not a valid text or
    if it does not contain at least one word in the SPECIAL_KEYWORDS list

    """
    SPECIAL_KEYWORDS = ["yes", "yeah", "yep", "yup"]
    if audio_text is None:
        return False
    if not isinstance(audio_text, str):
        return False
    if not any(word in audio_text for word in SPECIAL_KEYWORDS):
        return False
    return True


def check_is_command(audio_text):
    """
    Raises an InvalidCommandError if the audio text is not a valid text or
    if it does not contain at least one word in the SPECIAL_KEYWORDS list

    """
    SPECIAL_KEYWORDS = ["bubby", "baby", "bobby", "hey bobby"]
    if audio_text is None:
        return False
    if not isinstance(audio_text, str):
        return False
    if not any(word in audio_text for word in SPECIAL_KEYWORDS):
        return False
    return True


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def generate_random_tmp_folder_name():
    file_name = get_random_string(10)
    return f"/tmp/{file_name}.mp3"


def say(text):
    myobj = gTTS(text=text, lang=language, slow=False)
    temp_name = generate_random_tmp_folder_name()
    myobj.save(temp_name)
    print("prepping to play")
    file = AudioSegment.from_mp3(temp_name)
    print("playing")
    play(file)
