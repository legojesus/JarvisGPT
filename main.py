import environment                                      # Get environment vars
from logs import logger                                 # Logging
from jarvis import run_jarvis                           # Main function to run Jarvis
from speech_to_text import get_voice_prompt_from_user   # Voice activation of functions



OS = environment.OS             # Get the device's OS for context.
USERNAME = environment.USERNAME # Get the user's username in the OS so the bot will figure out the home folder's path and other user-related context.

logger.info('\n########################## STARTING NEW SESSION ##########################\n')
logger.info(f'Operating system = {OS}, Username = {USERNAME}')


# Initialize genesis context that contains the basic description for ChatGPT on how to act and respond to user's queries based on the device's OS.
genesis_context = None

if OS == "Linux":
    genesis_context = 'Pretend you are JARVIS. If I ask you to do something on my computer, only reply with the necessary linux bash command ' \
                  'to perform it, starting with the ! sign, unless I specifically ask you to answer normally without any commands. '\
                  f'For example, if I ask you to install something, reply with !apt-get install whatever I asked to install. My username in the OS is {USERNAME}. ' \
                  'Never use SUDO in commands unless I specifically ask you to do so.'\
                  'Any other question that is not related to my computer you can answer normally.' + '\n'
elif OS == "Windows":
    genesis_context = 'Pretend you are JARVIS. If I ask you to do something on my computer or ask about anything that is related to my computer, only reply with the relevant Windows CMD command ' \
                  'to perform the task or answer the question, starting with the ! sign, without any additional output, unless I specifically ask you to answer normally without any commands. '\
                  'Any other question that is not related to my computer you can answer normally.' + '\n' \
                  f'Here are some examples: If I ask you to create a new folder on my desktop, only reply with !mkdir C:\\Users\\{USERNAME}\\Desktop\\"New Folder" - notice how the folder name is wrapped in quotes because there is a space in the name. ' \
                  f'If I ask you to delete a folder, only reply with !rmdir /S /Q C:\\Users\\{USERNAME}\\path-to-folder - notice the use of the /Q flag to auto-confirm deletion.'
                  




    
        

if __name__ == '__main__':
    if genesis_context is None:
        logger.error("Unsupported operating system. Jarvis currently works with Linux and Windows only")
        exit()
    
    run_jarvis(genesis_context, OS)

    