from groq import Groq
from dotenv import load_dotenv
import os


# loading groq api and creaing client
load_dotenv()
GROQ_API_KEY =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)