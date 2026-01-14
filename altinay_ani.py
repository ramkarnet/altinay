import streamlit as st
import requests

# YENİ ANAHTARIN
API_KEY = "AIzaSyADgezoMbaavhLi0vac6lMUOkoRfKeh47w"

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir_v1(kelimeler, yil, ton):
    # Hata veren v1beta ve -latest yerine en kararlı v1 yolunu kullanıyoruz
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, '{kelimeler}' konulu {ton} bir anı anlat. Samimi ol."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Eğer gemini-pro da hata verirse, otomatik olarak flash'ı dene
            url_flash = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            resp_flash = requests.post(url_flash, json=payload, timeout=20)
            if resp_flash.status_code == 200:
                return resp_flash.json()['candidates'][0]['content']['parts'][0]['text']
            
            return f"🚨 Google hala hazır değil. Hata: {resp_flash.text}"
    except Exception as e:
        return f"🚨 Bağlantı sorunu: {str(e)}"

# ARAYÜZ
st.title("🎭 Altınay Anı Üretici")
kelimeler = st.text_input("🔑 Anahtar Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik"])

if st.button("✨ Anıyı Üret"):
    if kelimeler:
        with st.spinner("🌀 Altınay o günü hatırlıyor..."):
            sonuc = aniyi_getir_v1(kelimeler, yil, ton)
            st.markdown("---")
            if "🚨" in sonuc:
                st.error(sonuc)
            else:
                st.success(sonuc)
                st.balloons()
