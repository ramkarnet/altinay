import streamlit as st
import requests

# Anahtar koda yazılmıyor, gizli kasadan okunuyor
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Secrets kısmında GEMINI_API_KEY bulunamadı!")
    st.stop()

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir(kelimeler, yil, ton):
    # En sağlam v1beta yolunu kullanıyoruz
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Altınay adında bir karakter hakkında {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. Samimi ol."}]}]
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"🚨 Durum: Google hala onay bekliyor. (Hata Kodu: {response.status_code})"

st.title("🎭 Altınay Anı Üretici")
k = st.text_input("🔑 Anahtar Kelime")

if st.button("✨ Anıyı Hatırla"):
    if k:
        with st.spinner("Altınay uzaklara daldı..."):
            sonuc = aniyi_getir(k, 2020, "Komik")
            st.info(sonuc)
