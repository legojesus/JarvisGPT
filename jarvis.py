from speech_to_text import get_voice_prompt_from_user
from chatgpt import send_prompt_to_openai
from text_to_speech import read_answer_to_user
from logs import logger
import subprocess   # For running Linux and Windows commands


def run_jarvis(genesis_context, OS):

    logger.info('Started Jarvis in sleep mode')
    history = genesis_context
    conversation_count = 0
    no_user_input_count = 0
    jarvis_sleeping = True

    start_sentence = "Jarvis systems activated. Start a new conversation by saying my name - Jarvis. Say the word 'Mute' when you'd like to stop the conversation, and the word 'Exit' to end the program."
    print(start_sentence)
    read_answer_to_user(start_sentence, OS)


    while jarvis_sleeping:

        user_text = get_voice_prompt_from_user()

        if user_text is None:
            logger.info("No voice input detected in main loop, restarting loop")
            continue
        if user_text == "exit" or user_text == "Exit":
            logger.info("User said the word exit, stopping program entirely")
            read_answer_to_user("Goodbye sir.", OS)
            exit()
        if "Jarvis" in user_text or "jarvis" in user_text:
            logger.info("User said the word jarvis, starting jarvis listening function")
            jarvis_sleeping = False
            read_answer_to_user("Yes sir?", OS)


        while jarvis_sleeping is False:
            logger.info(f'Conversation query #{conversation_count}. Waiting for user input')
            #prompt = input("Talk to JARVIS: ")     # Text input via terminal
            prompt = get_voice_prompt_from_user()   # Voice input via microphone
            logger.info(f'User: {prompt}.')

            if prompt == 'exit':
                logger.info("\n########################## Exiting ###########################\n")
                read_answer_to_user("Goodbye sir.", OS)
                exit()
            elif prompt == 'reset':
                logger.warning("!!!Clearing history session, starting new conversation!!!")
                history = genesis_context
                read_answer_to_user("Conversation history reset. Starting a new conversation.", OS)
                continue
            elif prompt == 'mute':
                logger.warning("User said the word mute, muting jarvis and exiting to main loop")
                read_answer_to_user("Muting.", OS)
                jarvis_sleeping = True
                break
            elif prompt == None:
                no_user_input_count += 1
                if no_user_input_count >= 30:
                    logger.info(f"User is inactive for too long, putting JARVIS to sleep. no_user_input_count = {no_user_input_count}")
                    read_answer_to_user("Going to sleep.", OS)
                    jarvis_sleeping = True
                    break
                else:
                    logger.info(f"No user input detected in inner function loop (count = {no_user_input_count}), restarting loop. ")
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
                    answer = answer.replace('\n', ' && ')   # This doesn't work in Windows powershell, only in CMD. Need to find an alternative to chain commands.

                    ### For Linux shell + Windows CMD:
                    command = subprocess.run(answer, shell=True, universal_newlines=True, capture_output=True, text=True)

                    ### For Windows powershell logic:
                    # if OS == "Linux":
                    #     command = subprocess.run(answer, shell=True, universal_newlines=True, capture_output=True, text=True)
                    # elif OS == "Windows":
                    #     command = subprocess.run(["powershell", "-Command", answer], universal_newlines=True, capture_output=True, text=True)

                    if len(command.stdout) > 0:
                        logger.info(f"Jarvis: {command.stdout}")
                        print("Command output: ", command.stdout)
                        history += 'I ran the command, here is the output:' + command.stdout + '\n' + 'Reply with relevant info according to this output.' + '\n'
                        logger.info('Sending command output back to ChatGPT')
                        answer = send_prompt_to_openai(history)
                        answer = str(answer.strip())
                        logger.info(f'ChatGPT: {answer}')
                        history += answer + '\n'
                        read_answer_to_user(answer, OS)

                    elif len(command.stderr) > 0:
                        logger.warning(f"Jarvis: {command.stderr}")
                        print("Command error: ", command.stderr)
                        history += 'I ran the command and there was an error. Error output: ' + command.stderr + '\n'
                        logger.info('Sending command error back to ChatGPT')
                        answer = send_prompt_to_openai(history)
                        answer = str(answer.strip())
                        logger.info(f'ChatGPT: {answer}')
                        history += answer + '\n'
                        read_answer_to_user(answer, OS)

                    else:
                        logger.info('Jarvis: Command executed successfully')
                        answer = "Done. \n"
                        print("Done. \n")
                        read_answer_to_user(answer, OS)

                except Exception as e:
                    logger.error(f'{str(e)}')

            else:
                logger.info(f'Jarvis: {answer}')
                read_answer_to_user(answer, OS)
            
            conversation_count += 1

            if conversation_count >= 10:
                logger.warning('Conversation count is 10, summarizing converation to make history shorter')
                history += 'Please summarize our conversation so far so that I can use it as a short context for you in the future.\n'
                logger.info('Asking ChatGPT to summarize conversation')
                answer = send_prompt_to_openai(history)
                history = genesis_context + answer + '\n'
                conversation_count = 0
                logger.info(f"Summary successful. Conversation count reset to 0")
        
    
    
    

