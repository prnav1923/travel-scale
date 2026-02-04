# TravelScale: RAG Travel Planner 🌍✈️

TravelScale is an intelligent travel cost optimizer and itinerary planner powered by **Google Gemini** and **LangChain**. It helps users plan budget-friendly trips with detailed cost breakdowns, customized itineraries, and money-saving tips.

## 🚀 Features

*   **Smart Itinerary Generation**: Create 4-day (or more) travel plans optimized for your interest and budget.
*   **Cost Optimization**: Get a detailed breakdown of estimated costs for accommodation, food, transport, and activities.
*   **Leakage Minimization**: Practical tips to avoid "tourist taxes" and unnecessary expenses.
*   **Interactive UI**: Built with Streamlit for a clean, easy-to-use web interface.

## 🛠️ Tech Stack

*   **Python 3.10+**
*   **Streamlit**: Frontend UI
*   **LangChain**: Orchestration and RAG framework
*   **Google Gemini (GenAI)**: LLM for reasoning and content generation
*   **FAISS/Chroma** (Planned): For local vector storage of travel guides

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
    Create a `.env` file in the root directory and add your Google API Key:
    ```bash
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

## 🏃‍♂️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.
