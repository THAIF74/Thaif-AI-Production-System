import os

import requests
import streamlit as st

st.set_page_config(
    page_title="Thaif AI Production System",
    page_icon="⚙️",
    layout="centered",
)

try:
    api_url = st.secrets.get("API_URL", "")
except Exception:
    api_url = ""

API_URL = (
    api_url or os.getenv("API_URL", "http://127.0.0.1:8000")
).rstrip("/")

st.title("⚙️ Thaif AI Production System")
st.caption("A monitored, validated text-processing API.")

if st.button("Check API health"):
    try:
        response = requests.get(f"{API_URL}/health", timeout=15)
        response.raise_for_status()
        st.success("API is healthy!")
        st.json(response.json())
    except requests.RequestException:
        st.error("Cannot connect to the API. Check that the backend is running.")

st.subheader("Text Processing")

with st.form("process_form"):
    text = st.text_area(
        "Enter text",
        placeholder="Type a sentence to process...",
        max_chars=5000,
    )
    submitted = st.form_submit_button("Process text", type="primary")

if submitted:
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/process",
                json={"text": text},
                timeout=15,
            )
            response.raise_for_status()
            result = response.json()

            st.success("Text processed successfully!")
            col1, col2 = st.columns(2)
            col1.metric("Word count", result["word_count"])
            col2.metric("Character count", result["character_count"])
            st.write("**Processed text:**")
            st.code(result["uppercase_text"])
            st.write("**Request ID:**", response.headers.get("X-Request-ID", "Unavailable"))
        except requests.HTTPError as exc:
            st.error(f"API rejected the request: {exc.response.status_code}")
        except requests.RequestException:
            st.error("Could not reach the API. Check the backend URL.")