import collections
import streamlit as st
from collections import defaultdict, OrderedDict
import json

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

# Defining the Questinaire funcution


# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.preferences = {}

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



def main():

# Title on one line, left-aligned
    st.markdown("""
    <div class="title-container">
        <h1 class="title">🔮 Open Source License Wizard 🧙</h1>
    </div>
    """, unsafe_allow_html=True)

    st.write("This wizard will help you choose the most appropriate open-source license for your project.")


    # Debug information
    st.write("Debug: Current step", st.session_state.step)
    st.write("Debug: Number of question categories", len(questions))


    if st.session_state.step < len(questions):
        category, category_questions = questions[st.session_state.step]
        st.markdown(f"<h3>🧹 {category}</h3>", unsafe_allow_html=True)
        
        for question, key in category_questions:
            st.session_state.preferences[key] = st.checkbox(question, value=st.session_state.preferences.get(key, False), key=key)
        
        if st.button("Next", on_click=next_step):
            pass
    else:
        if st.button("🧙‍♂️ Get Recommendations 🧙‍♀️", key="get_recommendations"):
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
    
