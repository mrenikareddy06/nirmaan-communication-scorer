import streamlit as st

st.set_page_config(
    page_title="Communication Skills Scorer - Nirmaan AI",
    page_icon="🎤",
    layout="wide"
)

import re
from collections import Counter
import json

try:
    import language_tool_python
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    ADVANCED_NLP = True
except ImportError:
    ADVANCED_NLP = False
    st.warning("Advanced NLP libraries not installed. Using fallback methods. Run: pip install language-tool-python vaderSentiment")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .criterion-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .metric-box {
        background: #e0e7ff;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎤 AI Communication Skills Scorer</div>', unsafe_allow_html=True)
st.markdown("**Nirmaan Education - AI Intern Case Study | Rubric-Based Communication Analysis**")
st.markdown("---")

# Sample transcript (EXACT from the rubric document)
SAMPLE_TRANSCRIPT = """Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. 
I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father.
One special thing about my family is that they are very kind hearted to everyone and soft spoken. One thing I really enjoy is play, playing cricket and taking wickets.
A fun fact about me is that I see in mirror and talk by myself. One thing people don't know about me is that I once stole a toy from one of my cousin.
My favorite subject is science because it is very interesting. Through science I can explore the whole world and make the discoveries and improve the lives of others. 
Thank you for listening."""

if ADVANCED_NLP:
    try:
        tool = language_tool_python.LanguageTool('en-US')
        analyzer = SentimentIntensityAnalyzer()
    except:
        ADVANCED_NLP = False

def analyze_salutation(text):
    """Score salutation level (0-5 points) - EXACT rubric match"""
    text_lower = text.lower()
    text_start = text_lower.strip()[:50]  
    
    if any(phrase in text_start for phrase in ['i am excited to introduce', 'feeling great']):
        return 5, "Excellent - Enthusiastic introduction"
    
    elif any(phrase in text_start for phrase in ['good morning', 'good afternoon', 'good evening', 'good day', 'hello everyone']):
        return 4, "Good - Professional greeting"
    
    elif any(word in text_start for word in ['hi', 'hello']):
        return 2, "Normal - Basic greeting"
    
    else:
        return 0, "No salutation found"

def analyze_keywords(text):
    """
    Score keyword presence (0-30 points) - EXACT rubric match
    Must-have: 4 points each (max 20)
    Good-to-have: 2 points each (max 10)
    """
    text_lower = text.lower()
    
    must_have = {
        'Name': r'(my name is|myself|i am|i\'m)\s+[A-Z][a-z]+',
        'Age': r'(\d+\s*years?\s*old|age\s*\d+)',
        'School/Class': r'(school|class|grade|studying)',
        'Family': r'(family|mother|father|parents|siblings|brother|sister)',
        'Hobbies/Interest': r'(hobby|hobbies|enjoy|like|love|play|playing|interest|free time)'
    }
    
    good_to_have = {
        'About Family': r'(special thing about|my family is|kind|caring)',
        'Origin/Location': r'(from|live in|staying in|born in|parents are from)',
        'Ambition/Goal/Dream': r'(goal|dream|ambition|want to|aspire|improve|future)',
        'Fun fact/Unique thing': r'(fun fact|interesting|unique|special about me|don\'t know about me)',
        'Strengths/Achievements': r'(strength|achievement|good at|best at|proud of)'
    }
    
    must_have_found = []
    must_have_score = 0
    for key, pattern in must_have.items():
        if re.search(pattern, text, re.IGNORECASE):
            must_have_found.append(key)
            must_have_score += 4
    
    good_to_have_found = []
    good_to_have_score = 0
    for key, pattern in good_to_have.items():
        if re.search(pattern, text, re.IGNORECASE):
            good_to_have_found.append(key)
            good_to_have_score += 2
    
    must_have_score = min(must_have_score, 20)
    good_to_have_score = min(good_to_have_score, 10)
    
    total_score = must_have_score + good_to_have_score
    
    return total_score, must_have_found, good_to_have_found

def analyze_flow(text):
    """
    Score flow/structure (0-5 points) - EXACT rubric match
    Order: Salutation → Name → Mandatory details → Optional Details → Closing
    """
    text_lower = text.lower()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    has_opening = bool(re.match(r'^(hi|hello|good morning|good afternoon|good evening)', text_lower.strip()))
    has_closing = bool(re.search(r'(thank you|thanks|that\'s all|that is all)', text_lower))
    
    name_early = False
    if len(sentences) >= 1:
        first_two = ' '.join(sentences[:2]).lower()
        name_early = bool(re.search(r'(my name is|myself|i am|i\'m)\s+[A-Za-z]+', first_two, re.IGNORECASE))
    
    if has_opening and name_early and has_closing:
        return 5, "Excellent flow - Proper structure followed"
    else:
        return 0, "Flow not followed - Missing proper opening, name introduction, or closing"

def analyze_speech_rate(word_count, duration_sec):
    """
    Score speech rate (0-10 points) - EXACT rubric match
    Based on WPM (Words Per Minute)
    """
    wpm = (word_count / duration_sec) * 60
    
    if wpm > 161:
        return 2, wpm, "Too Fast"
    elif 141 <= wpm <= 160:
        return 6, wpm, "Fast (Good)"
    elif 111 <= wpm <= 140:
        return 10, wpm, "Ideal pace"
    elif 81 <= wpm <= 110:
        return 6, wpm, "Slow (Acceptable)"
    else:  
        return 2, wpm, "Too Slow"

def analyze_grammar_advanced(text, word_count):
    """
    Score grammar using LanguageTool (0-10 points) - EXACT rubric match
    Formula: Grammar Score = 1 - min(errors_per_100_words / 10, 1)
    """
    if not ADVANCED_NLP:
        return analyze_grammar_fallback(text, word_count)
    
    try:
        matches = tool.check(text)
        error_count = len(matches)
        
        errors_per_100 = (error_count / word_count) * 100
        
        grammar_ratio = 1 - min(errors_per_100 / 10, 1)
        
        if grammar_ratio >= 0.9:
            score = 10
        elif grammar_ratio >= 0.7:
            score = 8
        elif grammar_ratio >= 0.5:
            score = 6
        elif grammar_ratio >= 0.3:
            score = 4
        else:
            score = 2
        
        issues = [match.ruleId for match in matches[:3]]  # Top 3 issues
        
        return score, issues, grammar_ratio, error_count
    except:
        return analyze_grammar_fallback(text, word_count)

def analyze_grammar_fallback(text, word_count):
    """Fallback grammar check if LanguageTool not available"""
    issues = []
    
    if re.search(r'\bmyself\s+[A-Z]', text):
        issues.append("Use 'I am' instead of 'myself'")
    
    if re.search(r'\b(ain\'t|gonna|wanna|gotta)\b', text, re.IGNORECASE):
        issues.append("Informal contractions")
    
    if re.search(r'\bi\s+[a-z]', text):
        issues.append("'I' should be capitalized")
    
    if re.search(r'\s+[,.]', text):
        issues.append("Spacing issues")
    
    error_count = len(issues)
    errors_per_100 = (error_count / word_count) * 100
    grammar_ratio = 1 - min(errors_per_100 / 10, 1)
    
    if grammar_ratio >= 0.9:
        score = 10
    elif grammar_ratio >= 0.7:
        score = 8
    elif grammar_ratio >= 0.5:
        score = 6
    elif grammar_ratio >= 0.3:
        score = 4
    else:
        score = 2
    
    return score, issues, grammar_ratio, error_count

def analyze_vocabulary(words):
    """
    Score vocabulary richness using TTR (0-10 points) - EXACT rubric match
    TTR = Distinct words ÷ Total words
    """
    unique_words = set(w.lower() for w in words if w.isalpha())
    ttr = len(unique_words) / len(words)
    
    if ttr >= 0.9:
        score = 10
    elif ttr >= 0.7:
        score = 8
    elif ttr >= 0.5:
        score = 6
    elif ttr >= 0.3:
        score = 4
    else:
        score = 2
    
    return score, ttr, len(unique_words)

def analyze_clarity(text, word_count):
    """
    Score clarity based on filler words (0-15 points) - EXACT rubric match
    Filler words from rubric: um, uh, like, you know, so, actually, basically, right, i mean, well, kinda, sort of, okay, hmm, ah
    """
    filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 
                    'right', 'i mean', 'well', 'kinda', 'sort of', 'okay', 'hmm', 'ah']
    
    text_lower = text.lower()
    filler_count = 0
    
    for filler in filler_words:
        filler_count += len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
    
    filler_rate = (filler_count / word_count) * 100
    
    if filler_rate <= 3:
        score = 15
    elif filler_rate <= 6:
        score = 12
    elif filler_rate <= 9:
        score = 9
    elif filler_rate <= 12:
        score = 6
    else:  
        score = 3
    
    return score, filler_count, filler_rate

def analyze_engagement_advanced(text):
    """
    Score engagement using VADER sentiment (0-15 points) - EXACT rubric match
    Uses VADER to calculate positive sentiment probability (0 to 1)
    """
    if not ADVANCED_NLP:
        return analyze_engagement_fallback(text)
    
    try:
        scores = analyzer.polarity_scores(text)
        positive_score = scores['pos']  
        
        if positive_score >= 0.9:
            score = 15
        elif positive_score >= 0.7:
            score = 12
        elif positive_score >= 0.5:
            score = 9
        elif positive_score >= 0.3:
            score = 6
        else:
            score = 3
        
        return score, positive_score, scores['compound']
    except:
        return analyze_engagement_fallback(text)


def analyze_engagement_fallback(text):
    """Fallback engagement analysis if VADER not available"""
    positive_words = ['enjoy', 'love', 'like', 'interesting', 'excited', 'happy', 
                      'great', 'wonderful', 'amazing', 'fantastic', 'favorite', 
                      'special', 'kind', 'explore', 'improve', 'discover', 'grateful',
                      'good', 'best', 'thank', 'appreciate', 'enthusiastic', 'passionate',
                      'fun', 'awesome', 'excellent', 'beautiful', 'brilliant', 'perfect',
                      'nice', 'lovely', 'pleasant', 'delightful', 'marvelous']
    
    negative_words = ['hate', 'boring', 'bad', 'terrible', 'awful', 'dislike', 
                      'sad', 'angry', 'anxious', 'dull', 'stole', 'worst', 'horrible']
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
 
    positive_rate = (positive_count / len(words)) * 100
    
    if positive_rate >= 8:
        positive_score = 0.9
    elif positive_rate >= 6:
        positive_score = 0.7
    elif positive_rate >= 4:
        positive_score = 0.5
    elif positive_rate >= 2:
        positive_score = 0.3
    else:
        positive_score = 0.1
    
    if negative_count > 0:
        positive_score = max(positive_score - (negative_count * 0.1), 0.1)
    
    if positive_score >= 0.9:
        score = 15
    elif positive_score >= 0.7:
        score = 12
    elif positive_score >= 0.5:
        score = 9
    elif positive_score >= 0.3:
        score = 6
    else:
        score = 3
    
    return score, positive_score, positive_count

def score_transcript(text, duration_sec=None):
    """
    Main scoring function - EXACT rubric implementation
    """
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    if duration_sec is None:
        duration_sec = word_count / 2.58
    
    duration_sec = max(duration_sec, 1)  
    
    sal_score, sal_detail = analyze_salutation(text)
    key_score, must_have, good_to_have = analyze_keywords(text)
    flow_score, flow_detail = analyze_flow(text)
    content_score = sal_score + key_score + flow_score
    
    speech_score, wpm, speech_detail = analyze_speech_rate(word_count, duration_sec)
    
    if ADVANCED_NLP:
        grammar_score, grammar_issues, grammar_ratio, error_count = analyze_grammar_advanced(text, word_count)
    else:
        grammar_score, grammar_issues, grammar_ratio, error_count = analyze_grammar_fallback(text, word_count)
    
    vocab_score, ttr, unique_word_count = analyze_vocabulary(words)
    language_score = grammar_score + vocab_score
    
    clarity_score, filler_count, filler_rate = analyze_clarity(text, word_count)
    
    if ADVANCED_NLP:
        engagement_score, sentiment_score, compound = analyze_engagement_advanced(text)
    else:
        engagement_score, sentiment_score, sentiment_detail = analyze_engagement_fallback(text)
    
    total_score = content_score + speech_score + language_score + clarity_score + engagement_score
    
    return {
        'overall_score': round(total_score, 1),
        'word_count': word_count,
        'sentence_count': sentence_count,
        'duration': round(duration_sec, 1),
        'wpm': round(wpm, 1),
        'criteria': [
            {
                'name': 'Content & Structure',
                'score': content_score,
                'max': 40,
                'weight': 40,
                'details': [
                    f" Salutation: {sal_score}/5 - {sal_detail}",
                    f" Keywords: {key_score}/30 (Must-have: {len(must_have)}/5 [{', '.join(must_have) if must_have else 'None'}] | Good-to-have: {len(good_to_have)}/5 [{', '.join(good_to_have) if good_to_have else 'None'}])",
                    f" Flow: {flow_score}/5 - {flow_detail}"
                ]
            },
            {
                'name': 'Speech Rate',
                'score': speech_score,
                'max': 10,
                'weight': 10,
                'details': [
                    f" WPM: {round(wpm, 1)} words/minute",
                    f" Assessment: {speech_detail}",
                    f" Ideal range: 111-140 WPM"
                ]
            },
            {
                'name': 'Language & Grammar',
                'score': language_score,
                'max': 20,
                'weight': 20,
                'details': [
                    f" Grammar: {grammar_score}/10 (Errors: {error_count}, Ratio: {grammar_ratio:.2f})",
                    f" Vocabulary (TTR): {vocab_score}/10 (TTR: {ttr:.2f}, Unique: {unique_word_count}/{word_count})",
                    f" Issues: {', '.join(str(i) for i in grammar_issues[:3]) if grammar_issues else 'None detected'}"
                ]
            },
            {
                'name': 'Clarity',
                'score': clarity_score,
                'max': 15,
                'weight': 15,
                'details': [
                    f" Filler words: {filler_count} occurrences",
                    f" Filler rate: {filler_rate:.2f}%",
                    f" Assessment: {'Excellent clarity' if filler_rate <= 3 else 'Good' if filler_rate <= 6 else 'Needs improvement'}"
                ]
            },
            {
                'name': 'Engagement',
                'score': engagement_score,
                'max': 15,
                'weight': 15,
                'details': [
                    f" Sentiment score: {sentiment_score:.3f}",
                    f" Method: {'VADER (advanced)' if ADVANCED_NLP else 'Word-based (fallback)'}",
                    f" Assessment: {'Very engaging' if engagement_score >= 12 else 'Moderately engaging' if engagement_score >= 9 else 'Could be more enthusiastic'}"
                ]
            }
        ]
    }


# ----------------- STREAMLIT UI -------------------

with st.sidebar:
    st.markdown("### i) About This Tool")
    st.markdown("""
    **Rubric-Based Scoring:**
    - Content & Structure: 40%
    - Speech Rate: 10%
    - Language & Grammar: 20%
    - Clarity: 15%
    - Engagement: 15%
    
    **NLP Methods:**
    - Rule-based keyword matching
    - LanguageTool grammar check
    - VADER sentiment analysis
    - TTR vocabulary richness
    """)
    
    if ADVANCED_NLP:
        st.success(" Advanced NLP enabled")
    else:
        st.warning(" Using fallback methods")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(" Input Transcript")
    
    transcript = st.text_area(
        "Paste the transcript here:",
        height=250,
        placeholder="Enter or paste the student's self-introduction transcript..."
    )
    
    duration_input = st.number_input(
        "Duration in seconds (optional - leave 0 for auto-estimate):",
        min_value=0,
        max_value=300,
        value=0,
        help="If you know the actual speech duration, enter it here. Otherwise, it will be estimated."
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        analyze_btn = st.button(" Score Transcript", type="primary", use_container_width=True)
    with col_btn2:
        if st.button(" Load Sample (Expected: 86/100)", use_container_width=True):
            transcript = SAMPLE_TRANSCRIPT
            st.rerun()

with col2:
    st.subheader(" Results")
    
    if analyze_btn and transcript:
        with st.spinner("Analyzing transcript with rubric-based scoring..."):
            duration = duration_input if duration_input > 0 else None
            results = score_transcript(transcript, duration)
        
        st.markdown(f"""
        <div class="score-card">
            <h2 style="margin:0; font-size: 1.2rem; opacity: 0.9;">Overall Score</h2>
            <h1 style="margin:0.5rem 0; font-size: 3.5rem; font-weight: 700;">{results['overall_score']}/100</h1>
            <p style="margin:0; opacity: 0.8;">Sample expected: 86/100</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f'<div class="metric-box"><h3 style="margin:0;">{results["word_count"]}</h3><p style="margin:0; font-size:0.9rem;">Words</p></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown(f'<div class="metric-box"><h3 style="margin:0;">{results["wpm"]}</h3><p style="margin:0; font-size:0.9rem;">WPM</p></div>', unsafe_allow_html=True)
        with col_m3:
            st.markdown(f'<div class="metric-box"><h3 style="margin:0;">{results["duration"]}s</h3><p style="margin:0; font-size:0.9rem;">Duration</p></div>', unsafe_allow_html=True)
        
        st.session_state['results'] = results
    
    elif 'results' in st.session_state:
        results = st.session_state['results']
        st.markdown(f"""
        <div class="score-card">
            <h2 style="margin:0; font-size: 1.2rem; opacity: 0.9;">Overall Score</h2>
            <h1 style="margin:0.5rem 0; font-size: 3.5rem; font-weight: 700;">{results['overall_score']}/100</h1>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info(" Enter a transcript and click 'Score Transcript' to see results")

if 'results' in st.session_state:
    json_results = json.dumps(st.session_state['results'], indent=2)
    st.download_button(
        label=" Download Results (JSON)",
        data=json_results,
        file_name="communication_score.json",
        mime="application/json",
        use_container_width=True
    )

if 'results' in st.session_state:
    results = st.session_state['results']
    st.markdown("---")
    st.subheader(" Detailed Criterion-wise Breakdown")
    
    for criterion in results['criteria']:
        percentage = (criterion['score'] / criterion['max']) * 100
        
        if percentage >= 80:
            color = "#10b981"
            bar_color = "success"
        elif percentage >= 60:
            color = "#f59e0b"
            bar_color = "warning"
        else:
            color = "#ef4444"
            bar_color = "error"
        
        with st.container():
            col_name, col_score = st.columns([3, 1])
            
            with col_name:
                st.markdown(f"**{criterion['name']}**")
            
            with col_score:
                st.markdown(f"<h3 style='text-align: right; color: {color}; margin: 0;'>{criterion['score']}/{criterion['max']}</h3>", unsafe_allow_html=True)
                st.caption(f"Weight: {criterion['weight']}%")
            
            st.progress(percentage / 100)
            
            for detail in criterion['details']:
                st.markdown(f"&nbsp;&nbsp;&nbsp;{detail}")
            
            st.markdown("")

st.markdown("---")
st.caption("Built for Nirmaan Education AI Internship Case Study | Scoring based on provided rubric")