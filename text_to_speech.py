import platform     # Figure out the OS of the user
import pyttsx3      # Text to speech synthesizer for Windows (can work on linux but voice sounds horrible).
import subprocess   # Manually activate espeak on linux as it sounds better than pyttsx3.


OS = platform.system()

# Init pyttsx3 (Py Text-To-Speech)
talkbot = pyttsx3.init()
talkbot.setProperty('rate', 130)        # Setting the voice's talking speed
talkbot.setProperty('volume', 1.0)      # Setting the volume level between 0 and 1
voices = talkbot.getProperty('voices')  # Getting details of current voice
talkbot.setProperty('voice', 0)         # 0 for male voice.


# for voice in voices:
#     talkbot.setProperty('voice', voice.id)
#     print(voice)
# talkbot.say('The quick brown fox jumped over the lazy dog.')
# talkbot.runAndWait()


def read_answer_to_user(answer):
    """
    Reads ChatGPT's answer back to the user (text-to-speech).

        Parameters:
            answer (string): ChatGPT's answer to the user's prompt/question/request.

        Returns:
            None.
    """
    if OS == "Windows":
        talkbot.say(answer)
        talkbot.runAndWait()
        talkbot.stop()
    elif OS == "Linux":
        subprocess.run(f"espeak -v mb-en1 -s 140 '{answer}'", shell=True,
                       universal_newlines=True,
                       capture_output=True,
                       text=True)
