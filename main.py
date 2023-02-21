import environment              # Get environment vars
from logs import logger         # Logging
from jarvis import run_jarvis   # Main function to run Jarvis



OS = environment.OS             # Get the device's OS for context.
USERNAME = environment.USERNAME # Get the user's username in the OS so the bot will figure out the home folder's path and other user-related context.

logger.info('\n########################## STARTING NEW SESSION ##########################\n')
logger.info(f'Operating system = {OS}, Username = {USERNAME}')


# Initialize genesis context that contains the basic description for ChatGPT on how to act and respond to user's queries based on the device's OS.
genesis_context = None

if OS == "Linux":
    genesis_context = 'If I ask you to do something on my computer, only reply with the necessary linux bash command ' \
                  'to perform it, starting with the ! sign, unless I specifically ask you to answer normally without any commands. '\
                  f'For example, if I ask you to install something, reply with !apt-get install whatever I asked to install. My username in the OS is {USERNAME}. ' \
                  'If you reply with multiple commands, chain them together instead of separating them into new lines.' \
                  'Never use SUDO in commands unless I specifically ask you to do so.'\
                  'Any other question that is not related to my computer you can answer normally.' + '\n'
elif OS == "Windows":
    genesis_context = 'If I ask you to do something on my computer, only reply with the relevant Windows CMD command ' \
                  'to perform the task, starting with the ! sign, without any additional output, unless I specifically ask you to answer normally without any commands. '\
                  f'For example, If I ask you to create a new folder on my desktop, only reply with !mkdir C:\\Users\\{USERNAME}\\Desktop\\New Folder". ' \
                  'If you reply with multiple commands, chain them together instead of separating them into new lines.' \
                  'Any other question that is not related to my computer you can answer normally.' + '\n'


# Run Jarvis.
if genesis_context is not None:
    run_jarvis(genesis_context, OS)
else:
    logger.error("Unsupported operating system. Jarvis currently works with Linux and Windows only")




# Keep program running non-stop
# while True:
#     # Get prompt from user's voice and convert to text
#     prompt = get_voice_prompt_from_user()
#
#     # Send prompt to OpenAI and get answer
#     answer = send_prompt_to_openai(prompt)
#     # Read the answer back to the user
#     read_answer_to_user(answer)