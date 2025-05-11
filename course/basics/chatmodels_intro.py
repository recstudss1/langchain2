# from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

# llm = ChatOpenAI(model="gpt-3.5")

# result=llm.invoke("what is todays date")

# print(result)

# import getpass
# import os

# if not os.environ.get("GROQ_API_KEY"):
#   os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model

model = init_chat_model("llama3-8b-8192", model_provider="groq")

result=model.invoke("what is the date today?")

print(result)