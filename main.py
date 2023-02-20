
from speech_to_text import get_voice_prompt_from_user
from chatgpt_bot import send_prompt_to_openai
from text_to_speech import read_answer_to_user


# Keep program running non-stop
# while True:
#     # Get prompt from user's voice and convert to text
#     prompt = get_voice_prompt_from_user()
#
#     # Send prompt to OpenAI and get answer
#     answer = send_prompt_to_openai(prompt)
#     # Read the answer back to the user
#     read_answer_to_user(answer)


import subprocess   # Running linux shell commands
import platform

OS = platform.system()
USERNAME = "\"Yaron Kachalon\""

genesis_context = ""

if OS == "Linux":
    genesis_context = 'If I ask you to do something on my computer, only reply with the necessary linux bash command ' \
                  'to perform it, starting with the ! sign, unless I specifically ask you to answer normally without any commands. '\
                  f'For example, if I ask you to install something, reply with !apt-get install whatever I asked to install. My username in the OS is {USERNAME}. ' \
                  'Never use SUDO in commands unless I specifically ask you to do so.'\
                  'Any other question that is not related to my computer you can answer normally.' + '\n'
elif OS == "Windows":
    genesis_context = 'If I ask you to do something on my computer, only reply with the relevant Windows CMD command ' \
                  'to perform the task, starting with the ! sign, without any additional output, unless I specifically ask you to answer normally without any commands. '\
                  f'For example, If I ask you to create a new folder on my desktop, only reply with !mkdir C:\\Users\\{USERNAME}\\Desktop\\New Folder". ' \
                  'Any other question that is not related to my computer you can answer normally.' + '\n'


history = genesis_context

while True:
    prompt = input("Talk to JARVIS: ")
    if prompt == 'exit':
        print("Exiting")
        break
    elif prompt == 'reset':
        print("Clearing history session, starting new conversation.")
        history = genesis_context
        continue

    history += prompt + '\n'
    answer = send_prompt_to_openai(history)
    answer = str(answer.strip())
    history += answer + '\n'

    if answer.startswith('!'):
        try:
            answer = answer.replace('!', '', )
            answer = answer.replace('\n', ' && ')
            command = subprocess.run(answer, shell=True,
                                     universal_newlines=True,
                                     capture_output=True,
                                     text=True)

            if len(command.stdout) > 0:
                print("Command's output:", command.stdout)
                history += 'This is the output of the command: ' + command.stdout + '\n' + "Answer normally according to this output." + '\n'
                answer = send_prompt_to_openai(history)
                answer = str(answer.strip())
                history += answer + '\n'
                #read_answer_to_user(answer)

            elif len(command.stderr) > 0:
                print("Command error:", command.stderr)
                history += 'The command failed. explain why using this output: ' + command.stdout + '\n'
                answer = send_prompt_to_openai(history)
                answer = str(answer.strip())
                history += answer + '\n'
                #read_answer_to_user(answer)

            else:
                answer = "Done."
                print("Done.")
                #read_answer_to_user(answer)

        except Exception as e:
            history += str(e)
            print("Error: ", e)

    #else:
        #read_answer_to_user(answer)
