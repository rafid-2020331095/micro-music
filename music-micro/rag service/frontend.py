import streamlit as st
import requests

st.set_page_config(page_title="Song Chatbot", page_icon="🎵")

st.title("🎵 Song Chatbot Test Interface")

# Input fields
song_id_input = st.text_input("Song ID (optional)", "")
query_input = st.text_area("Your Question", height=100)

if st.button("Ask"):
    if not query_input.strip():
        st.warning("Please enter a question!")
    else:
        # Prepare payload
        payload = {"query": query_input}
        
        # If you want to filter by song, append song_id
        if song_id_input.strip():
            endpoint = f"http://127.0.0.1:8001/songs/{song_id_input}/query"
        else:
            endpoint = "http://127.0.0.1:8001/songs/query"
        
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            
            st.subheader("Answer")
            st.write(data.get("answer", "No answer found."))
            
            st.subheader("Source Chunks")
            for chunk in data.get("source_chunks", []):
                st.json(chunk)
                
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
