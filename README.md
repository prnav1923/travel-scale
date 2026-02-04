# TravelScale: RAG Travel Planner 🌍✈️

TravelScale is an intelligent travel cost optimizer and itinerary planner powered by **Google Gemini** and **LangChain**. It uses a **local Retrieval-Augmented Generation (RAG)** system to provide grounded, budget-conscious travel advice.

## 🚀 Features

*   **RAG Knowledge Base**: Uses local travel guides (in `data/`) to answer questions with specific facts.
*   **Vector Store Persistence**: Automatically saves the knowledge base to disk for instant startup.
*   **Cost Optimization**: Real-time estimates for accommodation, food, and transport based on guide data.
*   **Privacy-First**: Uses local embeddings (`all-MiniLM-L6-v2`) to process documents without external API calls for indexing.
*   **Interactive UI**: Streamlit interface with source citation.

## 🛠️ Tech Stack

*   **Python 3.10+**
*   **Streamlit**: Frontend UI
*   **LangChain**: RAG orchestration
*   **Google Gemini**: LLM for reasoning (via `langchain-google-genai`)
*   **FAISS**: Vector database for similarity search
*   **Sentence Transformers**: Local embeddings

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/prnav1923/travel-scale.git
    cd travel-scale
    ```

2.  **Create a virtual environment**
    ```bash
    python3 -m venv .travel
    source .travel/bin/activate  # On Windows: .travel\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirement.txt
    ```

4.  **Set up configuration**
    Create a `.env` file in the root directory:
    ```bash
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

## 🏃‍♂️ Usage

1.  **Start the App**
    ```bash
    streamlit run app.py
    ```

2.  **First Run**: The app will automatically ingest files from the `data/` directory and build the vector index. This takes a few seconds.

3.  **Subsequent Runs**: The app will load the saved index from `vector_store/` instantly.

4.  **Managing Data**:
    - Add new `.md` or `.txt` files to the `data/` folder.
    - Click **"🔄 Rebuild Index"** in the sidebar to update the knowledge base.

## 📂 Project Structure

- `app.py`: Main Streamlit application.
- `rag_engine.py`: Handles document loading, splitting, and FAISS indexing.
- `data/`: Folder for travel guide documents.
- `vector_store/`: Generated FAISS index (ignored by git).

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
