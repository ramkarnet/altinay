import streamlit as st
import requests

# Anahtarı kodun içine yazmıyoruz, Streamlit Secrets'tan çekiyoruz
API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir(kelimeler, yil, ton):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, {kelimeler} konulu {ton} bir anı anlat."}]}]}
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    return f"🚨 Hata: {response.status_code}. Google anahtarı doğrulamaya çalışıyor olabilir."

st.title("🎭 Altınay Anı Üretici")
k = st.text_input("Anahtar Kelimeler")
if st.button("✨ Anıyı Getir") and k:
    with st.spinner("Anı üretiliyor..."):
        st.write(aniyi_getir(k, 2020, "Komik"))
