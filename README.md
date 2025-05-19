# 🎯 Achievement Standards Recommender

An AI-powered tool that recommends **K-6 national curriculum achievement standards** based on your input teaching activity.  
Built with **Streamlit** and **OpenAI Embeddings**, this app allows you to quickly find the most relevant standards by **grade and subject**.

---

## 🔧 Features

- Dropdown selection for **grade** and **subject**
- Text input for classroom activities
- Recommends matching achievement standards
- Uses **LangChain** with **OpenAI Embeddings**
- JSON-based structured data
- Fast and accurate vector search with **Chroma**
- Displays similarity scores (Euclidean distance)

---

## 📁 Project Structure

achievement_recommender/
│
├── app.py                      # Streamlit main script
├── data/
│   └── achievement_standards.json  # JSON-structured standards
├── chroma_db/                 # Chroma vector database (auto-generated)
├── env/                       # Python virtual environment (.gitignored)
├── .gitignore
└── requirements.txt

---

## ▶️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/qjadmssk/achievement_recommender.git
cd achievement_recommender

2. Create and Activate Virtual Environment

python -m venv env
source env/bin/activate  # (Windows: .\env\Scripts\activate)

3. Install Dependencies

pip install -r requirements.txt

4. Add Your OpenAI API Key

Create a .env file and add the following line:

OPENAI_API_KEY=your_openai_api_key

5. Launch the App

streamlit run main.py


⸻

💡 Tech Stack
	•	Python 3.10+
	•	Streamlit – simple web UI
	•	OpenAI Embeddings (text-embedding-3-small)
	•	LangChain – vector-based document querying
	•	Chroma – local persistent vector database
	•	JSON – data management by grade and subject

⸻

🧠 How Similarity Works
	•	The user’s input activity is embedded using OpenAI’s model
	•	Only achievement standards that match the selected grade and subject are embedded and queried
	•	Results are returned based on Euclidean distance (L2 norm)
	•	Duplicates are filtered, and up to 5 best matches are displayed

⸻

📌 Notes
	•	env/ and chroma_db/ folders are excluded via .gitignore
	•	GPT-powered keyword extraction for teaching activities will be added soon

⸻

📬 Contact

Have questions or suggestions?
Feel free to open an issue or submit a pull request!
