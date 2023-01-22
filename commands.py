import os
import random
import stat
import string

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

language = "en"


def validate_command(command):
    # check if command is valid
    # return True or False
    pass


def check_is_command(audio_text):
    SPECIAL_KEYWORDS = ["lilly", "lil", "lily", "smelly"]
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
    myobj = gTTS(text=text, lang=language, slow=False, tld="com.au")
    temp_name = generate_random_tmp_folder_name()
    myobj.save(temp_name)
    print("prepping to play")
    song = AudioSegment.from_mp3(temp_name)
    print("playing")
    play(song)
