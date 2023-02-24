from modules.speech_to_text import get_voice_prompt_from_user
from modules.chatgpt import send_prompt_to_openai
from modules.text_to_speech import read_answer_to_user
from modules.logs import logger
import subprocess


def run_jarvis(genesis_context, OS):
    logger.info('Started Jarvis in sleep mode')
    history = genesis_context
    conversation_count = 0
    no_user_input_count = 0
    jarvis_sleeping = True

    start_sentence = "Welcome sir. Say the word Help to get more info on what you can do, or start a conversation now by calling my name - Jarvis."
    help_sentence = "The available commands are: Exit, Mute, Jarvis, Reset, and Help. Exit will shut me down completely. Mute will put me to sleep. Jarvis will wake me up. Reset will clear conversation history and start a fresh new conversation. Help will repeat these instructions. " \
                    "Start a conversation by saying Jarvis and wait for me to confirm. After that, speak freely and ask me anything you want. I can perform commands on your computer and I can answer any and all general questions. " \
                    "If at any point my replies get mixed up or are persistently wrong, say the word, Reset, and we'll start over."

    print(start_sentence)
    read_answer_to_user(start_sentence, OS)

    while jarvis_sleeping:

        user_text = get_voice_prompt_from_user()

        if user_text is None:
            logger.info("No voice input detected in sleep loop, restarting loop")
            continue
        elif user_text == "exit" or user_text == "Exit":
            logger.info("User said the word exit, stopping program entirely")
            read_answer_to_user("Goodbye sir.", OS)
            exit()
        elif "Jarvis" in user_text or "jarvis" in user_text:
            logger.info("User said the word jarvis, starting jarvis active function")
            jarvis_sleeping = False
            no_user_input_count = 0
            read_answer_to_user("Listening sir.", OS)
        elif user_text == "help" or user_text == "Help":
            logger.info("User said the word help, letting Jarvis explain all possible commands and useage")
            print(help_sentence)
            read_answer_to_user(help_sentence, OS)

        while jarvis_sleeping is False:
            logger.info(f'Conversation query #{conversation_count}. Waiting for user input')
            # prompt = input("Talk to JARVIS: ")     # Text input via terminal
            prompt = get_voice_prompt_from_user()  # Voice input via microphone
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
            elif prompt is None:
                no_user_input_count += 1
                if no_user_input_count >= 10:
                    logger.info(
                        f"no_user_input_count = {no_user_input_count}. User is inactive for too long, Going back to sleep loop for passive listening.")
                    read_answer_to_user("Going to sleep. Wake me up by calling my name Jarvis.", OS)
                    jarvis_sleeping = True
                    break
                else:
                    logger.info(
                        f"No user input detected in inner function loop (count = {no_user_input_count}), restarting loop. ")
                    continue
            elif prompt == 'help':
                logger.info("User said the word help, letting Jarvis explain all possible commands and useage")
                print(help_sentence)
                read_answer_to_user(help_sentence, OS)
                continue
            no_user_input_count = 0
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
                    # answer = answer.replace('\n', ' && ')

                    if answer.startswith("start"):
                        command = subprocess.Popen(answer, shell=True, universal_newlines=True,
                                                   text=True)  # To open programs but keep jarvis running.
                        logger.info(f"Jarvis: Opened program at user's request: {answer}")

                    else:
                        command = subprocess.run(answer, shell=True, universal_newlines=True, capture_output=True,
                                                 text=True)
                        if len(command.stdout) > 0:
                            logger.info(f"Jarvis: {command.stdout}")
                            print("Command output: ", command.stdout)
                            history += 'I ran the command, here is the output:' + command.stdout + '\n' + 'Reply with relevant info according to this output without repeating what I wrote.' + '\n'
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
                history += 'Please summarize our conversation so far so that I can use it as a short context for you in the future.' \
                           'Make sure to include the commands used, paths created/visited and any other important info that I might ask you about later for reference.\n '
                logger.info('Asking ChatGPT to summarize conversation')
                answer = send_prompt_to_openai(history)
                history = genesis_context + answer + '\n'
                conversation_count = 0
                logger.info(f"Summary successful. Conversation count reset to 0")





