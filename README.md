# 🛡️ FakeShield — AI Fake Review Detector

An AI-powered tool to detect fake reviews in e-commerce using machine learning.

---

## 📁 Files

| File | Description |
|---|---|
| `frontend.py` | Streamlit UI (cyberpunk-themed) |
| `backend.py` | ML model, feature engineering, prediction logic |
| `requirements.txt` | Python dependencies |

---

## 🚀 How to Run

### 1. Install Python
Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run frontend.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## 🧠 How It Works

1. Paste any e-commerce review into the text box
2. Select the star rating and purchase type
3. Click **⚡ ANALYSE**
4. The AI returns:
   - ✅ **GENUINE** or 🚨 **FAKE** verdict
   - Fake probability score (gauge chart)
   - 7 risk signal bars

---

## ⚙️ Tech Stack

- **Python** — Core language
- **scikit-learn** — Random Forest classifier (200 trees)
- **Streamlit** — Web UI framework
- **Plotly** — Interactive charts
- **TextBlob** — Sentiment & subjectivity analysis

---

## 📊 Detection Signals

The model analyses 11 features including:
- ALL-CAPS usage ratio
- Excessive exclamation marks
- Low vocabulary variety
- High subjectivity score
- Unverified purchase
- Extreme star ratings (1★ or 5★)
- Emoji overuse
- Review text length

---

## 👨‍💻 Author

Built as a Data Science project for fake review detection in e-commerce.
