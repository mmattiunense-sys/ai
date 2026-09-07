import streamlit as st
import requests

st.set_page_config(page_title="Sovereign AI Engine", page_icon="🤖", layout="centered")

st.title("🤖 Sovereign AI Engine v2.0")
st.caption("Il tuo sistema MoE privato e specializzato con memoria FAISS e Ollama")

# Configurazione API
SERVER_URL = "http://127.0.0.1:8000/v1/chat"
ADMIN_KEY = "sk-sovereign-admin-key-999"

HEADERS = {
    "X-API-Key": ADMIN_KEY,
    "Content-Type": "application/json"
}

# Inizializza la cronologia della chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostra i messaggi precedenti
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dell'utente
if prompt := st.chat_input("Scrivi un messaggio..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Invia la richiesta al tuo server_v2.py
    with st.chat_message("assistant"):
        with st.spinner("Elaborazione nel latent space & FAISS..."):
            try:
                response = requests.post(
                    SERVER_URL,
                    json={"prompt": prompt},
                    headers=HEADERS,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_reply = data["response"]
                    experts = ", ".join(data.get("active_experts", []))
                    
                    full_response = f"{ai_reply}\n\n---\n📌 *Nodi attivati: {experts}*"
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"Errore dal server: {response.status_code}")
            except Exception as e:
                st.error(f"Impossibile connettersi al server locale: {e}")