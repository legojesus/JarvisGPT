import speech_recognition   # Speech to text library
from logs import logger     # Logging

# Init Speech Recognition
try:
    logger.info('Initializing Speech-To-Text engine')
    listenbot = speech_recognition.Recognizer()
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
            listenbot.adjust_for_ambient_noise(source, duration=0.5)
             
            # Listens to the user's voice input
            print("Listening. Please talk now.")
            audio = listenbot.listen(source)
            
            logger.info('Converting user voice prompt to text via Google API')
            new_text = listenbot.recognize_google(audio)

            return new_text
             
    except speech_recognition.RequestError as e:
        logger.error(f"Could not process speech recognition request.\n {e}")
         
    except speech_recognition.UnknownValueError:
        logger.warning('Could not understand voice input. Either user didnt talk, wasnt clear, or theres a lot of background noise')
