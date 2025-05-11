import os
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from pytrends.request import TrendReq
import plotly.express as px

# Load environment variables from .env file
load_dotenv()

# Set up API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Initialize Google Trends API
google_trends = GoogleTrendsQueryRun(api_wrapper=GoogleTrendsAPIWrapper())

# Initialize Groq Chat Model
chat_model = ChatGroq(model="mixtral-8x7b-32768", temperature=0, max_tokens=None, max_retries=2)

# Initialize Pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Function to fetch real-time YouTube CPM data by niche
def fetch_youtube_cpm_data():
    try:
        url = "https://www.tubebuddy.com/blog/profitable-youtube-niches/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        data = {}
        for item in soup.find_all("li"):
            text = item.get_text()
            if "CPM of" in text:
                niche, cpm = text.split("CPM of")
                data[niche.strip()] = float(cpm.strip().replace("$", ""))
        return data
    except Exception as e:
        st.error(f"Error fetching CPM data: {e}")
        return {}

# Function to analyze Google Trends data
def get_trend_data(keyword):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
        data = pytrends.interest_over_time()
        if data.empty:
            return None
        data = data.reset_index()
        return data
    except Exception as e:
        st.error(f"Error fetching trend data: {e}")
        return None

# Function to fetch interest by region
def get_interest_by_region(keyword):
    try:
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
        region_data = pytrends.interest_by_region(resolution='country')
        region_data = region_data.reset_index()
        region_data = region_data.sort_values(by=keyword, ascending=False)
        return region_data
    except Exception as e:
        st.error(f"Error fetching interest by region: {e}")
        return None

# Function to generate niche questions dynamically
def generate_niche_questions(conversation_history):
    system_message = SystemMessage(content="Generate dynamic questions to find the best niche for content creation based on user responses.")
    response = chat_model.invoke([system_message] + conversation_history)
    return response.content.strip()

# Streamlit UI Configuration
st.set_page_config(page_title="Trend Analyzer & Niche Finder", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "💬 Chatbot", "🎯 Find My Niche"])

# Page 1: Dashboard
if page == "📊 Dashboard":
    st.title("📊 Trend & Business Idea Dashboard")
    
    # Keyword input
    keyword = st.text_input("Enter a keyword to analyze Google Trends:", "AI Technology")
    if st.button("Analyze Trends"):
        trend_data = get_trend_data(keyword)
        if trend_data is not None:
            st.subheader(f"Trend Over Time for '{keyword}'")
            fig = px.line(trend_data, x='date', y=keyword, title=f"Interest Over Time for '{keyword}'")
            st.plotly_chart(fig)
            
            st.subheader(f"Geographical Interest for '{keyword}'")
            region_data = get_interest_by_region(keyword)
            if region_data is not None:
                fig = px.choropleth(region_data, locations='geoName', locationmode='country names', color=keyword,
                                    title=f"Interest by Region for '{keyword}'", color_continuous_scale='Viridis')
                st.plotly_chart(fig)
        else:
            st.write("No trend data found for this keyword.")

# Page 2: Chatbot
elif page == "💬 Chatbot":
    st.title("💬 Google Trends Chatbot")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask about trends, niches, or business ideas:")
    if st.button("Ask"):
        if user_input:
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            response = chat_model.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(response)
            st.write(response.content)
        else:
            st.warning("Please enter a question.")

# Page 3: Find My Niche
elif page == "🎯 Find My Niche":
    st.title("🎯 Personalized Niche Finder")

    if 'niche_questions' not in st.session_state:
        st.session_state.niche_questions = [SystemMessage(content="Start niche-finding conversation.")]
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []

    current_question = generate_niche_questions(st.session_state.niche_questions)
    st.session_state.niche_questions.append(HumanMessage(content=current_question))
    
    user_response = st.text_input("Your Answer:")
    if st.button("Next Question"):
        if user_response:
            st.session_state.user_answers.append(user_response)
            next_question = generate_niche_questions(st.session_state.niche_questions + [HumanMessage(content=user_response)])
            st.session_state.niche_questions.append(HumanMessage(content=next_question))
            st.experimental_rerun()

    # Display previous responses
    if st.session_state.user_answers:
        st.subheader("Your Responses So Far:")
        for idx, ans in enumerate(st.session_state.user_answers, 1):
            st.write(f"{idx}. {ans}")

    # Fetch Real-Time CPM & RPM
    if len(st.session_state.user_answers) >= 5:  # After 5 questions, suggest niches
        st.subheader("Suggested Niches Based on Your Responses")
        cpm_data = fetch_youtube_cpm_data()
        sorted_cpm = sorted(cpm_data.items(), key=lambda x: x[1], reverse=True)
        for niche, cpm in sorted_cpm[:3]:
            st.write(f"📌 **{niche}** - Estimated CPM: **${cpm}**")

        st.subheader("Target Audience & Language Insights")
        trend_keyword = st.session_state.user_answers[0]  # Use the first answer as the main keyword
        audience_data = get_interest_by_region(trend_keyword)
        if audience_data is not None:
            fig = px.bar(audience_data, x='geoName', y=trend_keyword, title="Target Audience by Region")
            st.plotly_chart(fig)
