from groq import Groq
from dotenv import load_dotenv
import os


# loading groq api and creaing client
load_dotenv()
GROQ_API_KEY =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# reading system prompt
file = open("system_prompt.txt","r")
system_prompt = file.read()
file.close()
# function to get code reviews and suggestions
def codeCritic(code:str) -> str:
    if not code:
        return "No code provided,please upload the code.."
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content": system_prompt
                },
                {
                    "role":"user",
                    "content":f"please review the following code:\n\n {code}"
                }
            ],
            model="qwen-2.5-coder-32b",
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occured during code review :{e}"