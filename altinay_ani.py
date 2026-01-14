import streamlit as st
import requests
import json

# 1. DOĞRUDAN API ANAHTARIN (Yeşil tikli olan)
API_KEY = "AIzaSyADgezoMbaavhLi0vac6lMUOkoRfKeh47w"

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir_israrli(kelimeler, yil, ton):
    # Denenecek tüm yollar (En güncelden en garantiye)
    kombinasyonlar = [
        ("v1beta", "gemini-1.5-flash"),
        ("v1", "gemini-1.5-flash"),
        ("v1beta", "gemini-pro"),
        ("v1", "gemini-pro")
    ]
    
    payload = {
        "contents": [{"parts": [{"text": f"Altınay adında her şeye anısı olan biri hakkında {yil} yılında geçen, {kelimeler} konulu {ton} bir anı anlat. 1. şahıs ağzından."}]}]
    }

    for ver, model in kombinasyonlar:
        url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={API_KEY}"
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                return res_json['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
            
    return None

# ARAYÜZ
st.title("🎭 Altınay Anı Üretici")
kelimeler = st.text_input("🔑 Anahtar Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik"])

if st.button("✨ Anıyı Üret"):
    if kelimeler:
        with st.spinner("🌀 Altınay hafızasını zorluyor..."):
            sonuc = aniyi_getir_israrli(kelimeler, yil, ton)
            if sonuc:
                st.info(sonuc)
                st.balloons()
            else:
                st.error("🚨 Google hala anahtarı onaylıyor. Lütfen 15 dakika bekleyip tekrar deneyin.")

