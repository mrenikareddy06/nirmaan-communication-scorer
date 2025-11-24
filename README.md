#  AI Communication Skills Scorer

**Nirmaan Education AI Internship Case Study Submission**

An AI-powered tool that analyzes and scores student self-introductions based on a comprehensive rubric covering content, speech rate, grammar, clarity, and engagement.

---

##  Project Overview

This tool evaluates spoken communication transcripts using:
- **Rule-based scoring**: Keyword detection, word counts, structure analysis
- **NLP-based scoring**: Sentiment analysis, vocabulary richness
- **Rubric-driven weighting**: 5 criteria with specific weights (total 100 points)

### Scoring Criteria
1. **Content & Structure (40%)**: Salutation, keywords (name, age, school, family, hobbies), flow
2. **Speech Rate (10%)**: Words per minute analysis
3. **Language & Grammar (20%)**: Grammar errors, vocabulary richness (TTR)
4. **Clarity (15%)**: Filler word detection
5. **Engagement (15%)**: Sentiment/positivity analysis

**Expected Score on Sample:** 86/100  
**Actual Score:** 83/100 (97% accurate)

---

##  Quick Start

### Run Locally
```bash
# Clone the repository
git clone https://github.com/mrenikareddy06/nirmaan-communication-scorer.git
cd nirmaan-communication-scorer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

##  Project Structure
```
nirmaan-communication-scorer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── sample_transcript.txt       # Sample input data
```

---

##  Scoring Methodology

### 1. Content & Structure (40 points)
- **Salutation (5pts)**: Detects greeting quality
- **Keywords (30pts)**: Must-have + Good-to-have keywords
- **Flow (5pts)**: Proper opening → content → closing structure

### 2. Speech Rate (10 points)
- Calculates WPM based on transcript length
- Ideal: 111-140 WPM

### 3. Language & Grammar (20 points)
- **Grammar (10pts)**: Error detection
- **Vocabulary (10pts)**: Type-Token Ratio (TTR)

### 4. Clarity (15 points)
- Counts filler words (um, uh, like, etc.)
- Score based on filler percentage

### 5. Engagement (15 points)
- Sentiment analysis using positive/negative word detection
- Maps to engagement score

---

##  Key Design Decisions

### Why Streamlit?
- **Simplicity**: Single Python file, no separate frontend/backend
- **Speed**: Faster development and deployment
- **Free hosting**: Streamlit Cloud provides free deployment
- **Built for AI**: Perfect for ML/data science applications

### Technology Stack
- **Python 3.8+**: Core language
- **Streamlit**: Web framework
- **RegEx**: Keyword matching
- **TTR**: Vocabulary metric
- **Sentiment Analysis**: Custom word-based approach

---

## Sample Output
```json
{
  "overall_score": 83,
  "word_count": 134,
  "criteria": [
    {
      "name": "Content & Structure",
      "score": 37,
      "max": 40
    }
  ]
}
```

---

## Demo

[https://drive.google.com/drive/folders/1JX-zn_Z6lHr6pi7KdA1_5uE9Iyg8pZP3?usp=sharing]

---

##  Acknowledgments

Built for Nirmaan Education AI Internship Case Study.

---

##  Contact

For questions: mrenikareddy@gmail.com
```

---
