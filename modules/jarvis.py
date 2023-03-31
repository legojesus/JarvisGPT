from modules.speech_to_text import get_prompt_from_user
from modules.chatgpt import send_prompt_to_openai
from modules.text_to_speech import read_answer_to_user
from modules.logs import logger
import modules.environment
import subprocess


def run_jarvis(genesis_context, OS):
    """
    This is the function that does all the magic. It mediates between ChatGPT and the user's computer, parsing
    ChatGPT's responses and running the commands it replies with on the computer.

    Args:
        genesis_context: String. The core text block that provides ChatGPT the context on how to behave and reply like
                         Jarvis, explaining to it that it can run commands without explaining them so we can parse it.
        OS: String. The user's machine operating system.

    Returns: None.

    """

    logger.info('Started Jarvis in sleep mode')
    history = genesis_context  # Keeps all conversation history and send it to chatGPT with every user prompt
    conversation_count = 0  # Count amount of user prompts and summarize conversation when count hits 10
    no_user_input_count = 0  # Count idle time (user doesn't talk) and put Jarvis to sleep automatically if too long
    jarvis_sleeping = True  # Sleeping means only listening to the word "Jarvis". Not sleeping means fully active.

    if modules.environment.VOICE_MODE == "TRUE":
        start_sentence = "Welcome sir. Say the word Help to get more info on what you can do, or start a conversation now by calling my name - Jarvis."
    else:
        start_sentence = "Welcome sir. Type the word Help to get more info on what you can do, or type Jarvis to start a conversation now."

    help_sentence = "The available commands are: \n - Exit. \n - Mute. \n - Jarvis. \n - Reset. \n - Help. \n - About. \n \n Exit will shut me down completely.\n Mute will put me to sleep.\n Jarvis will wake me up.\n Reset will clear conversation history and start a fresh new conversation. \n Help will repeat these instructions. \n About will list the version and other info. \n" \
                    "Start a conversation by saying/typing Jarvis and wait for me to confirm.\n After that, speak/type freely and ask me anything you want. \n I can perform commands on your computer and I can answer any and all general questions. " \
                    "If at any point my replies get mixed up or are persistently wrong, say/type the word Reset and we'll start over."

    about_sentence = "JarvisGPT 0.3 Alpha. \n Created by Yaron Kachalon (https://www.linkedin.com/in/yaronka/). \n \n JarvisGPT is a ChatGPT powered app that allows you to have a JARVIS like virtual assistant on your computer, that can answer general questions but can also run any and all Windows/Linux commands! Use it wisely. \n"

    read_answer_to_user(start_sentence, OS)

    while jarvis_sleeping:

        user_text = get_prompt_from_user()

        if user_text is None:
            logger.info("No voice input detected in sleep loop, restarting loop")
            continue

        elif user_text == "exit" or user_text == "Exit":
            logger.info("User said the word exit, stopping program entirely")
            logger.info("\n########################## Exiting ###########################\n")
            read_answer_to_user("Goodbye sir.", OS)
            return

        elif "Jarvis" in user_text or "jarvis" in user_text:
            logger.info("User said the word jarvis, starting jarvis active function")
            jarvis_sleeping = False
            no_user_input_count = 0
            read_answer_to_user("Listening sir.", OS)

        elif user_text == "help" or user_text == "Help":
            logger.info("User said the word help, letting Jarvis explain all possible commands and useage")
            read_answer_to_user(help_sentence, OS)

        elif user_text == "about" or user_text == "About":
            logger.info("User said the word about, printing the About info of the app.")
            read_answer_to_user(about_sentence, OS)

        while jarvis_sleeping is False:
            logger.info(f'Conversation query #{conversation_count}. Waiting for user input')
            prompt = get_prompt_from_user()
            logger.info(f'User: {prompt}.')

            if prompt == 'exit' or prompt == "Exit":
                logger.info("\n########################## Exiting ###########################\n")
                read_answer_to_user("Goodbye sir.", OS)
                return

            elif prompt == 'reset' or prompt == "Reset":
                logger.warning("!!!Clearing history session, starting new conversation!!!")
                history = genesis_context
                read_answer_to_user("Conversation history reset. Starting a new conversation.", OS)
                continue

            elif prompt == 'mute' or prompt == "Mute":
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

            elif prompt == 'help' or prompt == "Help":
                logger.info("User said the word help, letting Jarvis explain all possible commands and useage")
                read_answer_to_user(help_sentence, OS)
                continue

            elif prompt == "about" or prompt == "About":
                logger.info("User said the word about, printing the About info of the app.")
                read_answer_to_user(about_sentence, OS)
                continue

            no_user_input_count = 0
            history += prompt + '\n'
            logger.info('Sending user query to ChatGPT')
            answer = send_prompt_to_openai(history)
            answer = str(answer.strip())
            logger.info(f'ChatGPT: {answer}.')
            # print("Jarvis: ", answer)
            history += answer + '\n'

            if answer.startswith('!'):
                logger.info('Jarvis: The reply is a command. I will take it from here. Executing...')
                try:
                    answer = answer.replace('!', '', )
                    print(answer + '\n')

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
                            history += 'Reply normally to the following command output without repeating this sentence and without starting your reply with "Answer:" or "Acknowledged" : ' + command.stdout + '\n'
                            logger.info('Sending command output back to ChatGPT')
                            answer = send_prompt_to_openai(history)
                            answer = str(answer.strip())
                            logger.info(f'ChatGPT: {answer}')
                            history += answer + '\n'
                            read_answer_to_user(answer, OS)

                        elif len(command.stderr) > 0:
                            logger.warning(f"Jarvis: {command.stderr}")
                            print("Command error: ", command.stderr)
                            history += 'Reply normally to the following Error output without repeating this sentence and without starting your reply with "Answer:" or "Acknowledged" : ' + command.stderr + '\n'
                            logger.info('Sending command error back to ChatGPT')
                            answer = send_prompt_to_openai(history)
                            answer = str(answer.strip())
                            logger.info(f'ChatGPT: {answer}')
                            history += answer + '\n'
                            read_answer_to_user(answer, OS)

                        else:
                            logger.info('Jarvis: Command executed successfully')
                            answer = "Done. \n"
                            read_answer_to_user(answer, OS)

                except Exception as e:
                    logger.error(f'{str(e)}')

            else:
                logger.info(f'Jarvis: {answer}')
                read_answer_to_user(answer, OS)

            conversation_count += 1

            if conversation_count >= 10:
                logger.warning('Conversation count is 10, summarizing conversation to make history shorter')
                history += 'Please summarize our conversation so far so that I can use it as a short context for you in the future.' \
                           'Make sure to include the commands used, paths created/visited and any other important info that I might ask you about later for reference.\n '
                logger.info('Asking ChatGPT to summarize conversation')
                print("Jarvis: Conversation too long, summarizing context internally. This can take a few seconds.")
                answer = send_prompt_to_openai(history)
                history = genesis_context + answer + '\n'
                conversation_count = 0
                logger.info(f"Summary successful. Conversation count reset to 0")
