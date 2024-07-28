import collections
import streamlit as st
from collections import defaultdict, OrderedDict
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


################################################################################
################################################################################

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')



# Load licenses from the file
def load_licenses(file_path):
    with open(file_path, 'r') as file:
        licenses = json.load(file)
    return licenses

# Load licenses from the specified file
licenses = load_licenses("licence-list.txt")

# Load questions from the file
def load_questions(file_path):
    with open(file_path, 'r') as file:
        questions = json.load(file)
    return questions

# Load questions from the specified file
questions = load_questions("questions.txt")


def load_css(file_path):
    with open(file_path, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Use an absolute file path
load_css('style.css')


################################################################################
################################################################################

# Custom CSS for background color, stars, and background image
st.markdown("""
<div class="main">
    <div class="moon"></div>
    <!-- Twinkling Stars -->
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="shooting-star" style="left: 20%; top: 20%; animation-delay: 1s;"></div>
    <div class="shooting-star" style="left: 80%; top: 60%; animation-delay: 2s;"></div>
    <div class="shooting-star" style="left: 10%; top: 80%; animation-delay: 3s;"></div>
    <div class="shooting-star" style="left: 30%; top: 40%; animation-delay: 4s;"></div>
    <div class="shooting-star" style="left: 60%; top: 70%; animation-delay: 5s;"></div>
    <div class="shooting-star" style="left: 90%; top: 10%; animation-delay: 6s;"></div>
    <div class="shooting-star" style="left: 75%; top: 90%; animation-delay: 7s;"></div>
    <div class="shooting-star" style="left: 50%; top: 50%; animation-delay: 8s;"></div>
    <div class="shooting-star" style="left: 40%; top: 20%; animation-delay: 9s;"></div>
    <div class="shooting-star" style="left: 25%; top: 80%; animation-delay: 10s;"></div>
    </div>
    """, unsafe_allow_html=True)



################################################################################
################################################################################
#"""This function uses NLTK for tokenization and stop word removal, and then applies
#    TF-IDF to extract the most important keywords from the project description."""


def extract_keywords(text):
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_tokens = [w for w in word_tokens if w not in stop_words and w.isalnum()]

    # Use TF-IDF to get important keywords
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(filtered_tokens)])
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top 15 keywords
    dense = tfidf_matrix.todense()
    episode = dense[0].tolist()[0]
    phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
    sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
    
    # Filter keywords relevant to open source licensing
    relevant_keywords = [
        'open source', 'license', 'commercial', 'distribution', 'modification',
        'patent', 'trademark', 'copyright', 'attribution', 'copyleft',
        'permissive', 'proprietary', 'software', 'code', 'share',
        'derivative', 'compatible', 'restrictive', 'royalty-free', 'public domain'
    ]
    
    keywords = [
        feature_names[word_id] for (word_id, score) in sorted_phrase_scores[:30]
        if any(rk in feature_names[word_id] for rk in relevant_keywords)
    ][:15]
    
    return keywords


#"""This function matches the extracted keywords to the questions in our
#    questionnaire, setting preferences based on keyword matches."""

def match_keywords_to_questions(keywords):
    keyword_preferences = {}
    for category, category_questions in questions:
        for question, key in category_questions:
            if any(keyword in question.lower() for keyword in keywords):
                keyword_preferences[key] = True
    return keyword_preferences





################################################################################
################################################################################


def sidebar_content():
    st.sidebar.header("Project Description")
    project_description = st.sidebar.text_area("Describe your project:", height=150)
    
    if st.sidebar.button("Extract Keywords", key="extract_keywords_button"):
        if project_description:
            extracted_keywords = extract_keywords(project_description)
            st.session_state.keywords = extracted_keywords
            if not extracted_keywords:
                st.sidebar.warning("No relevant keywords found. Please provide more details about your project and its licensing needs.")
        else:
            st.sidebar.warning("Please provide a project description.")

    st.sidebar.header("Keywords")
    if st.session_state.keywords:
        selected_keywords = st.sidebar.multiselect(
            "Select or deselect keywords:",
            options=st.session_state.keywords,
            default=st.session_state.keywords
        )
        
        new_keyword = st.sidebar.text_input("Add a new keyword:")
        if st.sidebar.button("Add Keyword", key="add_keyword_button"):
            if new_keyword and new_keyword not in selected_keywords:
                selected_keywords.append(new_keyword)
            elif new_keyword in selected_keywords:
                st.sidebar.warning("This keyword already exists.")
            else:
                st.sidebar.warning("Please enter a keyword.")
        
        st.session_state.keywords = selected_keywords
        
        if st.sidebar.button("Apply Keywords", key="apply_keywords_button"):
            keyword_preferences = match_keywords_to_questions(st.session_state.keywords)
            st.session_state.preferences.update(keyword_preferences)
            st.sidebar.success("Keywords applied to questionnaire!")
    else:
        st.sidebar.info("Extract keywords from your project description or add them manually.")




################################################################################
################################################################################


#*************Defining the Questinaire funcution****************#

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'preferences' not in st.session_state:
    st.session_state.preferences = {}
if 'keywords' not in st.session_state:
    st.session_state.keywords = []

def next_step():
    current_category = questions[st.session_state.step][0]
    if any(st.session_state.preferences.get(key, False) for _, key in questions[st.session_state.step][1]):
        st.session_state.step += 1
    else:
        st.error(f"Please select at least one option in the '{current_category}' category before proceeding.")

def score_licenses(preferences):
    scores = defaultdict(int)
    for license_name, features in licenses.items():
        for key, value in features.items():
            if key in preferences and preferences[key] == value:
                scores[license_name] += 1

        # Additional scoring logic
        if preferences.get('research', False) and features.get('permissive', False):
            scores[license_name] += 1
        if preferences.get('commercial', False) and features.get('business_friendly', False):
            scores[license_name] += 1
        if preferences.get('strong_community', False) and not features.get('permissive', True):
            scores[license_name] += 1
        if preferences.get('patent_rights', False) and features.get('patent_protection', False):
            scores[license_name] += 1
        if preferences.get('attribution', False) and features.get('business_friendly', False):
            scores[license_name] += 1

    # If no preferences were selected, give each license a base score
    if all(score == 0 for score in scores.values()):
        for license_name in licenses:
            scores[license_name] = 1

    return scores

def recommend_licenses(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    st.header("Recommended licenses based on your preferences:")
    for license_name, score in sorted_scores[:5]:  # Show top 5 recommendations
        st.write(f"{license_name}: {score} points")
        st.write(f"Key features: {', '.join(k for k, v in licenses[license_name].items() if v)}")
        st.write("")

    if all(score == 1 for _, score in sorted_scores):
        st.info("Note: As no specific preferences were selected, all licenses are given equal consideration. Please review each license carefully to determine which best suits your needs.")
    else:
        st.write("Note: This list shows the top 5 recommendations. There may be other suitable licenses.")
    
    st.write("Remember to review the full text of any license before applying it to your project.")





################################################################################
################################################################################


def main():
    st.markdown("""
    <div class="title-container">
        <h1 class="title">🔮 Open Source License Wizard 🧙</h1>
    </div>
    """, unsafe_allow_html=True)

    st.write("This wizard will help you choose the most appropriate open-source license for your project.")

    # Add sidebar content
    sidebar_content()


    # Debug information
    st.write("Debug: Current step", st.session_state.step)
    st.write("Debug: Number of question categories", len(questions))


    # Continue with the questionnaire
    if st.session_state.step < len(questions):
        category, category_questions = questions[st.session_state.step]
        st.markdown(f"<h3>🧹 {category}</h3>", unsafe_allow_html=True)
        
        for question, key in category_questions:
            st.session_state.preferences[key] = st.checkbox(question, value=st.session_state.preferences.get(key, False), key=key)
        
        if st.button("Next", key=f"next_button_{st.session_state.step}", on_click=next_step):
            pass
    else:
        if st.button("🧙‍♂️ Get Recommendations 🧙‍♀️", key="get_recommendations_button"):
            scores = score_licenses(st.session_state.preferences)
            recommend_licenses(scores)

    # Footer with notes
    st.markdown("---")
    st.markdown("### Disclaimer")
    st.markdown("This tool is intended to assist you in selecting an open-source license.")
    st.markdown("Always review the full text of any license and consult legal advice if necessary.")
    st.markdown("The recommendations are based on your preferences and may not cover all scenarios.")

if __name__ == "__main__":
    main()