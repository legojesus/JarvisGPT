### J.A.R.V.I.S AI in Python - A speech-to-text to ChatGPT to text-to-speech program. 
### Basically allows you to talk to ChatGPT and hear it talking back. 
# Author: Yaron K.
# Date: 2023-02-12

#from speech_to_text import get_voice_prompt_from_user
from chatgpt import send_prompt_to_openai
#from text_to_speech import read_answer_to_user


# Keep program running non-stop
#while True:
    # Get prompt from user's voice and convert to text
    #prompt = get_voice_prompt_from_user()

    # Send prompt to OpenAI and get answer
    #answer = send_prompt_to_openai(prompt)

    # Read the answer back to the user
    #read_answer_to_user(answer)

import subprocess

init_context = 'If I ask or request something about my computer, only reply with the necessary linux shell command to perform it, starting with the ! sign. Any other question that is not related to my computer you can answer regularly.\n'
history = init_context

while True:
    prompt = input("Talk to JARVIS: ")
    if prompt == 'exit':
        print("Exiting")
        break
    elif prompt == 'reset':
        print("Clearing history session, starting new conversation.")
        history = init_context
        continue

    history += prompt
    #query = context + history
    answer = send_prompt_to_openai(history)
    answer = str(answer.strip())
    #answer = "!pwd"
    history += answer

    if answer.startswith('!'):
        try:
            answer = answer.replace('!', '')
            command = subprocess.run(answer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print("output:", command.stdout)
            history += command.stdout
            if command.stderr:
                print("error:", command.stderr)
                history += command.stderr
        except Exception as e:
            history += str(e)
            print("Error: ", e)