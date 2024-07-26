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
licenses = load_licenses(r"C:\Users\amiku\OneDrive\Desktop\licence-wizard\licence-list.txt")

# Load questions from the file
def load_questions(file_path):
    with open(file_path, 'r') as file:
        questions = json.load(file)
    return questions

# Load questions from the specified file
questions = load_questions(r"C:\Users\amiku\OneDrive\Desktop\licence-wizard\questions.txt")


def load_css(file_path):
    with open(file_path, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Use an absolute file path
load_css(r'C:\Users\amiku\OneDrive\Desktop\licence-wizard\style.css')

# Custom CSS for background color, stars, and background image
st.markdown("""
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

# The rest of your code remains the same
def get_user_preferences():
    preferences = {}
    st.markdown("<h1 style='text-align: left; font-family: \"Kalnia Glaze\", sans-serif;'>&#x1F52E Open Source License Wizard &#x1F9D9; </h1>", unsafe_allow_html=True)
    st.write("This wizard will help you choose the most appropriate open-source license for your project.")
    
    st.subheader("Please answer the following questions about your project:")
    
    for category, category_questions in questions:
        st.markdown(f"<h3>🧹 {category}</h3>", unsafe_allow_html=True)
        for question, key in category_questions:
            preferences[key] = st.checkbox(question, value=False, key=key)  # Checkboxes are initially unchecked
    
    return preferences

def score_licenses(preferences):
    scores = defaultdict(int)
    for license_name, features in licenses.items():
        for key, value in features.items():
            if key in preferences and preferences[key] == value:
                scores[license_name] += 1

        # Additional scoring logic based on user preferences
        if preferences.get('research', False) and features['permissive']:
            scores[license_name] += 1
        if preferences.get('commercial', False) and features['business_friendly']:
            scores[license_name] += 1
        if preferences.get('strong_community', False) and not features['permissive']:
            scores[license_name] += 1
        if preferences.get('patent_rights', False) and features['patent_protection']:
            scores[license_name] += 1
        if preferences.get('attribution', False) and features['business_friendly']:
            scores[license_name] += 1

    return scores

def recommend_licenses(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    st.header("Recommended licenses based on your preferences:")
    for license_name, score in sorted_scores[:5]:  # Show top 5 recommendations
        st.write(f"{license_name}: {score} points")
        st.write(f"Key features: {', '.join(k for k, v in licenses[license_name].items() if v)}")
        st.write("")

    st.write("Note: This list shows the top 5 recommendations. There may be other suitable licenses.")
    st.write("Remember to review the full text of any license before applying it to your project.")

def main():
    preferences = get_user_preferences()
    
    # Custom button styling using HTML
    if st.button("🧙‍♂️ Get Recommendations 🧙‍♀️", key="get_recommendations"):
        scores = score_licenses(preferences)
        recommend_licenses(scores)

    # Footer with notes
    st.markdown("---")
    st.markdown("### Disclaimer")
    st.markdown("This tool is intended to assist you in selecting an open-source license.")
    st.markdown("Always review the full text of any license and consult legal advice if necessary.")
    st.markdown("The recommendations are based on your preferences and may not cover all scenarios.")

if __name__ == "__main__":
    main()