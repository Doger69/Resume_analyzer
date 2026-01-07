📄 Resume–Job Match Analyzer

A professional web application that analyzes how well a resume matches a job description using **Natural Language Processing (NLP)**. The system computes a match score and provides clear visual feedback to help job seekers optimize their resumes.

🚀 Features

* Upload resume in **PDF format**
* Paste any **job description**
* Calculates match score using **TF-IDF + Cosine Similarity**
* Modern progress bar visualization
* Clear feedback: Low / Moderate / Excellent match
* Clean, professional UI built with **Streamlit**
* Lightweight and fast (no external APIs)

🛠️ Tech Stack

* **Frontend:** Streamlit, Custom CSS
* **Backend / NLP:** Python, Scikit-learn, NLTK
* **PDF Processing:** PyPDF2
* **Algorithm:** TF-IDF, Cosine Similarity

📁 Project Structure

```
resume_matcher/
│
├── app.py              # Frontend (UI + layout)
├── utils.py            # Backend logic (text processing & similarity)
├── requirements.txt    # Dependencies
└── README.md
```

⚙️ Installation & Setup

1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/resume-job-match-analyzer.git
cd resume-job-match-analyzer
```

2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

3️⃣ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

📊 How It Works

1. Resume text is extracted from the uploaded PDF
2. Job description text is cleaned and preprocessed
3. Both texts are converted into **TF-IDF vectors**
4. **Cosine similarity** is calculated between them
5. A match percentage is displayed with visual feedback

🧠 Algorithm Used

* **TF-IDF (Term Frequency–Inverse Document Frequency)**
* **Cosine Similarity**

These techniques are commonly used in:
* Applicant Tracking Systems (ATS)
* Resume screening tools
* Text similarity analysis

🎯 Use Cases

* Students and fresh graduates
* Job seekers optimizing resumes
* Learning NLP and text similarity
* Portfolio project for software or data roles

🔮 Future Enhancements

* Keyword gap analysis
* Resume improvement suggestions
* ATS-style scoring
* Export results as PDF
* Deployment to Streamlit Cloud

