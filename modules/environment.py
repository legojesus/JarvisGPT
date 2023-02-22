from dotenv import load_dotenv  # For getting variables from .env file into the environment
import os                       # For getting variables from environment into the code
import platform                 # Get the OS of the user's device


load_dotenv()

OS = platform.system()          # Get the device's OS
DEBUG = os.getenv("DEBUG")
USERNAME = os.getenv("USERNAME") # Get the user's username in the OS so the bot will figure out the home folder's path and other user-related context.



try:
    api_key = os.getenv("API_KEY")
except:
    print("Couldn't get OpenAI API key. Please make sure you have a .env file in this folder that contains the API key in the following format: API_KEY=\"xxxxxxx\"")
    exit()
