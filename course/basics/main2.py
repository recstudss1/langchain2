from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq()


val=input("Ask a question...")

messages = [
    SystemMessage("You are a professional Mathematics mentor and you only answer questions related to mathematics correctly. Don't answer any questions or queries apart from mathematics."),
    HumanMessage(val)       
] 

result = llm.invoke(messages)

print(result)

