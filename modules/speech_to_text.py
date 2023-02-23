import speech_recognition
from modules.logs import logger

# Init Speech Recognition
try:
    logger.info('Initializing Speech-To-Text engine')
    listenbot = speech_recognition.Recognizer()
    listenbot.dynamic_energy_threshold = False
    listenbot.energy_threshold = 100
    logger.info('Speech-To-Text engine successfully initialized')
except Exception as e:
    logger.error(f'Failed to initilize Speech-To-Text engine. Make sure you have all required depdendencies of this app.\n {e}')


def get_voice_prompt_from_user():
    """
    Records the user's voice via the device's microphone and translates it to a text string (speech-to-text).

        Parameters:
            None.

        Returns:
            new_text (string): The user's voice input converted to a string.
    """

    try:
        logger.info('Waiting for voice input from user')
        with speech_recognition.Microphone() as source:
             
            # Wait for a second to let the recognizer adjust the volume threshold based on the surrounding noise level
            #listenbot.adjust_for_ambient_noise(source, duration=0.5)
             
            # Listens to the user's voice input
            print("Listening. Please talk now.")
            audio = listenbot.listen(source, timeout=9999)
            if audio is not None:
                logger.info('Converting user voice prompt to text via Google API')
                new_text = listenbot.recognize_google(audio)
                logger.info(f'Converted voice to text: {new_text}')
                print("Voice input: ", new_text)

                return new_text
            return None
             
    except speech_recognition.RequestError as e:
        logger.error(f"Could not process speech recognition request.\n {e}")

         
    except speech_recognition.UnknownValueError:
        logger.info('No voice input detected.')
    
    except Exception as e:
        logger.error(f"{e}")


# TEST:
# while True:
#     user_text = get_voice_prompt_from_user()
#     if user_text is not None:
#         print(user_text)

