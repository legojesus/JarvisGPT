import pyttsx3
import subprocess
from modules.logs import logger
import modules.environment

# Init pyttsx3 (Py Text-To-Speech)
try:
    logger.info('Initializing Text-To-Speech engine')
    talkbot = pyttsx3.init()
    talkbot.setProperty('rate', 150)  # Setting the voice's talking speed
    talkbot.setProperty('volume', 1.0)  # Setting the volume level between 0 and 1
    voices = talkbot.getProperty('voices')  # Getting details of current voice
    talkbot.setProperty('voice', 0)  # 0 for male voice.
    logger.info('Text-To-Speech engine successfully initialized')
except Exception as e:
    logger.error(
        f'Failed to initialize Text-ToSpeech engine. Make sure you have all the required dependencies '
        f'to run this app. \n {e}')


def read_answer_to_user(answer, OS, voice=modules.environment.VOICE_MODE):
    """
    Reads ChatGPT's answer back to the user (text-to-speech).

        Parameters:
            answer (string): ChatGPT's answer to the user's prompt/question/request.

        Returns:
            None.
    """

    if voice == "TRUE":

        if OS == "Windows":
            try:
                logger.info(f'Reading answer to user (Windows TTS): {answer}')
                print(answer)
                talkbot.say(answer)
                talkbot.runAndWait()
                # talkbot.stop()

            except Exception as ex:
                logger.error(
                    f'Error in Windows Text-To-Speech engine. Make sure that you have all required dependencies '
                    f'for this app.\n {ex}')

        elif OS == "Linux":
            try:
                logger.info(f'Reading answer to use (Linux TTS): {answer}')
                print(answer)
                subprocess.run(f"espeak -v mb-en1 -s 140 '{answer}'", shell=True, universal_newlines=True,
                               capture_output=True, text=True)

            except Exception as ex:
                logger.error(
                    f'Error in Linux Text-To-Speech engine. Make sure that you have all required dependencies '
                    f'for this app. \n {ex}')

    else:
        print(f"Jarvis: {answer} \n")
