import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.title("TravelScale: RAG Travel Planner")
st.write("Multi-destination travel cost optimizer powered by RAG + Gemini agents.")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ Set GOOGLE_API_KEY in .env")
    st.stop()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7,api_key=api_key)


# Basic query interface
query = st.text_input("Enter travel query (e.g., 'Budget trip for 2 to SE Asia')")

if query:
    prompt = ChatPromptTemplate.from_template(
        "You are a travel cost optimizer. Answer: {query}"
    )
    chain = prompt | llm
    response = chain.invoke({"query": query})
    # Fix: Extract text from AIMessage object
    if hasattr(response, 'content'):
        if isinstance(response.content, list):
            # Handle list content (e.g. from multimodal models)
            text_parts = []
            for item in response.content:
                if isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
                elif isinstance(item, str):
                    text_parts.append(item)
            display_text = "\n".join(text_parts)
        else:
            display_text = response.content
    elif isinstance(response, dict) and 'content' in response:
        display_text = response['content']
    elif isinstance(response, list) and response and isinstance(response[0], dict):
        display_text = response[0].get('text', str(response[0]))
    else:
        display_text = str(response)

    st.success("✅ **Plan:**")
    st.write(display_text)
