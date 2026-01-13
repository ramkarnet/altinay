import streamlit as st
import requests

# 1. API ANAHTARIN (Görseldeki yeşil tikli olanı buraya yapıştır)
API_KEY = "BURAYA_YESIL_TIKLI_ANAHTARI_YAPISTIR"

def aniyi_getir(kelimeler, yil, ton):
    # En stabil 2 yolu da deniyoruz
    yollar = [
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    ]
    
    payload = {
        "contents": [{"parts": [{"text": f"Altınay adında her şeye bir anısı olan efsane bir karakter hakkında {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. 1. şahıs ağzından anlat."}]}]
    }

    for url in yollar:
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                res_json = response.json()
                return res_json['candidates'][0]['content']['parts'][0]['text']
        except:
            continue
    return "🚨 Şu an Google sunucularına bağlanılamıyor. Lütfen 5-10 dakika sonra tekrar deneyin, anahtarınız henüz aktifleşiyor olabilir."

# ARAYÜZ
st.title("🎭 Altınay Anı Üretici")
kelimeler = st.text_input("🔑 Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2018)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik"])

if st.button("✨ Anı Üret"):
    if kelimeler:
        with st.spinner("Altınay hafızasını zorluyor..."):
            sonuc = aniyi_getir(kelimeler, yil, ton)
            st.info(sonuc)
