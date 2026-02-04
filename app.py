import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from rag_engine import RagEngine

load_dotenv()

st.title("TravelScale: RAG Travel Planner")
st.write("Multi-destination travel cost optimizer powered by RAG + Gemini agents.")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ Set GOOGLE_API_KEY in .env")
    st.stop()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0.7, api_key=api_key)

# Initialize RAG Engine
if 'rag' not in st.session_state:
    st.session_state.rag = RagEngine(api_key)

def load_knowledge_base(force_rebuild=False):
    rag = st.session_state.rag
    if force_rebuild or not rag.load_index():
        with st.spinner("Building knowledge base from files..."):
            rag.ingest("data")
            rag.build_index()
            rag.save_index()
            st.success("Knowledge base built and saved!")

# Load on startup
if not st.session_state.rag.vector_store:
    load_knowledge_base()

# Sidebar Status
with st.sidebar:
    st.header("Knowledge Base 📚")
    # Show status (approximation based on loaded docs if available, or just success tick)
    if st.session_state.rag.vector_store:
        st.success("Index Loaded ✅")
    else:
        st.warning("Index Not Loaded")
        
    if st.button("🔄 Rebuild Index"):
        load_knowledge_base(force_rebuild=True)
        st.rerun()

# Basic query interface
query = st.text_input("Enter travel query (e.g., 'Budget trip for 2 to SE Asia')")

if query:
    # 1. Retrieve Context
    context_text = ""
    if 'rag' in st.session_state:
        docs = st.session_state.rag.query(query)
        context_text = "\n\n".join([d.page_content for d in docs])
    
    # 2. Augmented Prompt
    prompt = ChatPromptTemplate.from_template(
        """You are a travel cost optimizer. Use the following context to answer the user's question. 
        If the context doesn't contain the answer, use your general knowledge but prioritize specific prices/details from context.
        
        Context:
        {context}
        
        Question: {query}"""
    )
    chain = prompt | llm
    response = chain.invoke({"query": query, "context": context_text})
    
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
    st.markdown(display_text)
    
    # Show sources in expander
    if context_text:
        with st.expander("View Retrieved Sources"):
            st.markdown(context_text)
