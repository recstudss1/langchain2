from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_groq import ChatGroq

load_dotenv()


chat_history=[]
PROJECT_ID="langchainintro2"
SESSION_ID="new_user_session"
COLLECTION_NAME = chat_history
client=firestore.Client(project=PROJECT_ID)

