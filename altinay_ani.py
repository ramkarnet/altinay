import streamlit as st
import requests

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# API Ayarı
API_KEY = st.secrets.get("AIzaSyCcwB7zXrnJqTpdAjd4-NSSKVATE25D7Nk")

def ani_uret_v1(kelimeler, yil, ton):
    # En stabil çalışan kararlı v1 adresi
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, '{kelimeler}' konulu {ton} bir anı anlat. samimi ol."}]
        }]
    }

    try:
        response = requests.post(url, json=payload)
        res_json = response.json()
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚨 Hata: {res_json.get('error', {}).get('message', 'Bilinmeyen hata')}"
    except Exception as e:
        return f"🚨 Bağlantı hatası: {e}"

# Basit Arayüz
st.title("🎭 Altınay Anı Üretici")
kelimeler = st.text_input("Anahtar Kelimeler (Örn: kedi, pizza)")
yil = st.number_input("Yıl", 1990, 2026, 2015)
ton = st.selectbox("Ton", ["Komik", "Absürt", "Dramatik"])

if st.button("✨ Anı Üret"):
    if kelimeler and API_KEY:
        with st.spinner("Altınay hatırlıyor..."):
            sonuc = ani_uret_v1(kelimeler, yil, ton)
            st.markdown("---")
            st.write(sonuc)
            if "🚨" not in sonuc: st.balloons()
