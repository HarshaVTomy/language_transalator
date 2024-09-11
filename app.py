import streamlit as st
from googletrans import Translator, LANGUAGES
import time

# Initialize Google Translator
translator = Translator()

# Function to get language code from language name
def get_language_code(language_name):
    for lang_code, lang_name in LANGUAGES.items():
        if lang_name.lower() == language_name.lower():
            return lang_code
    return None

# Function to translate text with retry mechanism
def translate_text_with_retry(source_text, src_lang, dest_lang_code, retries=3):
    for i in range(retries):
        try:
            # Attempt translation
            translated_text = translator.translate(source_text, src=src_lang, dest=dest_lang_code).text
            return translated_text
        except AttributeError as e:
            # Retry in case of 'NoneType' error
            if 'NoneType' in str(e):
                time.sleep(1)  # Wait 1 second before retrying
            else:
                raise e
    return None  # Return None if all retries fail

# Custom CSS for styling the app
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput, .stTextArea, .stButton {
        font-size: 18px !important;
    }
    h1 {
        text-align: center;
        color: #333333;
    }
    h2 {
        text-align: center;
        color: #666666;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        padding: 12px 30px;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #007BFF;
        padding: 10px;
    }
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #007BFF;
        padding: 10px;
    }
    .stSelectbox select {
        border-radius: 8px;
        border: 1px solid #007BFF;
    }
    .stCheckbox > label {
        font-size: 16px;
        color: #007BFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI
st.title("🌐 Language Translator")

st.write("""
    Use this tool to translate text between various languages. Just enter your text, choose the source and target languages, and get instant translations.
""")

# Input text
source_text = st.text_area("📝 Enter the text you want to translate:", "", height=150)

# Input source language (fixed selection)
source_lang = st.selectbox("🔠 Select source language", ["en", "fr", "es", "de", "it"])

# Target language input (searchable by name)
target_language_search = st.text_input("🔍 Enter target language name (e.g., French, Spanish, German):", "")

# Translate button
if st.button("🔄 Translate"):
    # Check if source text is provided
    if not source_text:
        st.error("⚠️ Please enter some text to translate.")
    else:
        target_lang_code = get_language_code(target_language_search)
        
        if target_lang_code is None:
            st.error(f"⚠️ Error: '{target_language_search}' is not a valid language name. Please try again.")
        else:
            try:
                # Attempt translation with retries
                translated_text = translate_text_with_retry(source_text, src_lang=source_lang, dest_lang_code=target_lang_code)
                if translated_text:
                    st.success(f"*Translated Text*: {translated_text}")
                else:
                    st.error("⚠️ Translation failed after multiple attempts.")
            except Exception as e:
                st.error(f"⚠️ Translation failed. Error: {str(e)}")

# Show supported languages with better design
if st.checkbox("Show supported languages"):
    st.write("📋 Supported Languages:")
    st.write(", ".join([f"{lang_name.capitalize()} ({lang_code})" for lang_code, lang_name in LANGUAGES.items()]))
