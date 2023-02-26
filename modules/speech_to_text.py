import speech_recognition
from modules.logs import logger
import modules.environment

# Init Speech Recognition
try:
    logger.info('Initializing Speech-To-Text engine')
    listenbot = speech_recognition.Recognizer()
    listenbot.dynamic_energy_threshold = False
    listenbot.energy_threshold = 300
    logger.info('Speech-To-Text engine successfully initialized')
except Exception as e:
    logger.error(f'Failed to initilize Speech-To-Text engine. Make sure you have all required depdendencies of this app.\n {e}')


def get_prompt_from_user(voice=modules.environment.VOICE_MODE):
    """
    Records the user's voice via the device's microphone and translates it to a text string (speech-to-text).

        Parameters:
            None.

        Returns:
            new_text (string): The user's voice input converted to a string.
    """
    if voice == "TRUE":
        try:
            logger.info('Waiting for voice input from user')
            with speech_recognition.Microphone() as source:

                # Wait for a second to let the recognizer adjust the volume threshold based on the surrounding noise level
                #listenbot.adjust_for_ambient_noise(source, duration=0.5)

                # Listens to the user's voice input
                print("Listening. Please talk now.")
                audio = listenbot.listen(source, timeout=10)
                if audio is not None:
                    logger.info('Converting user voice prompt to text via Google API')
                    new_text = listenbot.recognize_google(audio)
                    logger.info(f'Converted voice to text: {new_text}')
                    print(f"Voice input: {new_text}. \n")

                    return new_text
                return None

        except speech_recognition.RequestError as e:
            logger.error(f"Could not process speech recognition request.\n {e}")


        except speech_recognition.UnknownValueError:
            logger.info('No voice input detected.')

        except Exception as e:
            logger.error(f"{e}")

    else:
        new_text = input("Talk to Jarvis: ")
        print("\n")
        return new_text



