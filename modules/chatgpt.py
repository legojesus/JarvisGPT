import openai  # OpenAI API for processing text and reply like a human.
from modules.logs import logger
from modules import environment

# Init OpenAI
logger.info('Initializing OpenAI/ChatGPT backend')
openai.api_key = environment.api_key

model_engine = "text-davinci-003"  # The OpenAI GPT-3 model version.
# Reference: https://platform.openai.com/docs/models/gpt-3
logger.info(f'Model engine is: {model_engine}')


def send_prompt_to_openai(prompt):
    """
    Sends a text prompt to OpenAI API and returns an answer from ChatGPT.

        Parameters:
            prompt (string): A string of a qustion or request to be sent to OpenAI's ChatGPT.

        Returns:
            reply (string): The answer received from ChatGPT.
    """
    # Reference: https://platform.openai.com/docs/api-reference/completions/create
    completion = None

    try:
        completion = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=2000,
                                              n=1, stop=None, temperature=0.5)
        logger.info(f"Answer received from ChatGPT: {completion}")  # Provide data on the api call, with tokens count.
    except Exception as e:
        print("Error: ", e)
        logger.error(f'ChatGPT error: {e}')
        # exit()

    # Get the first reply
    if completion is not None:
        reply = completion.choices[0].text
        # print(reply)
        # print("\n")
        return reply

    logger.warning(
        'Received blank answer from ChatGPT. Either user prompt was empty or something went wrong when '
        'sending query to ChatGPT')
    return "Received blank answer."
