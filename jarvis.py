from speech_to_text import get_voice_prompt_from_user
from chatgpt import send_prompt_to_openai
from text_to_speech import read_answer_to_user
from logs import logger # Logging
import subprocess       # For running Linux and Windows commands



def run_jarvis(genesis_context, OS):

    logger.info('Started Jarvis')
    history = genesis_context
    conversation_count = 0

    while True:
        
        logger.info(f'Conversation query #{conversation_count}. Waiting for user input')
        prompt = input("Talk to JARVIS: ")
        logger.info(f'User: {prompt}.')

        if prompt == 'exit':
            logger.info("\n########################## Exiting ###########################\n")
            break
        elif prompt == 'reset':
            logger.warning("!!!Clearing history session, starting new conversation!!!")
            history = genesis_context
            continue

        history += prompt + '\n'
        logger.info('Sending user query to ChatGPT')
        answer = send_prompt_to_openai(history)
        answer = str(answer.strip())
        logger.info(f'ChatGPT: {answer}.')
        history += answer + '\n'

        if answer.startswith('!'):
            logger.info('Jarvis: The reply is a command. I will take it from here. Executing...')
            try:
                answer = answer.replace('!', '', )
                #answer = answer.replace('\n', ' && ')   # This doesn't work in Windows powershell, need to find an alternative to chain commands.

                ### For Linux shell + Windows CMD:
                command = subprocess.run(answer, shell=True, universal_newlines=True, capture_output=True, text=True)

                ### For Windows powershell logic:
                # if OS == "Linux":
                #     command = subprocess.run(answer, shell=True, universal_newlines=True, capture_output=True, text=True)
                # elif OS == "Windows":
                #     command = subprocess.run(["powershell", "-Command", answer], universal_newlines=True, capture_output=True, text=True)

                if len(command.stdout) > 0:
                    logger.info(f"Jarvis: {command.stdout}")
                    history += command.stdout + '\n'
                    logger.info('Sending command output back to ChatGPT')
                    answer = send_prompt_to_openai(history)
                    answer = str(answer.strip())
                    logger.info(f'ChatGPT: {answer}')
                    history += answer + '\n'
                    #read_answer_to_user(answer, OS)

                elif len(command.stderr) > 0:
                    logger.warning(f"Jarvis: {command.stderr}")
                    history += 'Error output: ' + command.stderr + '\n'
                    logger.info('Sending command error back to ChatGPT')
                    answer = send_prompt_to_openai(history)
                    answer = str(answer.strip())
                    logger.info(f'ChatGPT: {answer}')
                    history += answer + '\n'
                    #read_answer_to_user(answer, OS)

                else:
                    logger.info('Jarvis: Command executed successfully')
                    answer = "Done. \n"
                    print("Done. \n")
                    #read_answer_to_user(answer, OS)

            except Exception as e:
                logger.error(f'{str(e)}')

        #else:
            #logger.info(f'Jarvis: {answer}') 
            #read_answer_to_user(answer, OS)
        
        conversation_count += 1

        if conversation_count >= 5:
            logger.warning('Conversation count is 5, summarizing converation to make history shorter')
            history += 'Please summarize our conversation so far so that I can use it as a short context for you in the future.\n'
            logger.info('Asking ChatGPT to summarize conversation')
            answer = send_prompt_to_openai(history)
            history = genesis_context + answer + '\n'
            conversation_count = 0
            logger.info(f"Summary successful. Conversation count reset to 0")
        
    
    
    

