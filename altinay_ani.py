import streamlit as st
import requests
import json

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# API Ayarı
API_KEY = st.secrets.get("GEMINI_API_KEY")

def ani_uret_debug(kelimeler, yil, ton):
    # Denenecek tüm kombinasyonlar
    endpoints = [
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ]
    
    prompt_text = f"Altınay hakkında {yil} yılında geçen, {kelimeler} konulu, {ton} bir anı anlat. 200 kelime."
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    
    last_error = ""
    for url in endpoints:
        try:
            full_url = f"{url}?key={API_KEY}"
            response = requests.post(full_url, json=payload, timeout=10)
            res_json = response.json()
            
            if response.status_code == 200:
                # BAŞARILI!
                return res_json['candidates'][0]['content']['parts'][0]['text'], url.split('/')[-1].split(':')[0]
            else:
                last_error = f"{url.split('/')[-2]} sürümü {res_json.get('error', {}).get('message', 'Bilinmeyen Hata')}"
        except Exception as e:
            last_error = str(e)
            continue
            
    return None, last_error

# UI
st.title("🎭 Altınay Anı Üretici")
st.write("Eğer yine hata alırsak, hata mesajını buraya kopyala, sorunu kökten çözelim.")

kelimeler = st.text_input("Anahtar Kelimeler")
yil = st.slider("Yıl", 1990, 2026, 2018)
ton = st.selectbox("Ton", ["Komik", "Absürt", "Epik", "Dramatik"])

if st.button("✨ Anıyı Üret"):
    if not API_KEY:
        st.error("Secrets'ta anahtar yok!")
    elif kelimeler:
        with st.spinner("Modeller taranıyor ve anı üretiliyor..."):
            sonuc, debug_info = ani_uret_debug(kelimeler, yil, ton)
            if sonuc:
                st.success(f"Başarılı! (Kullanılan Model: {debug_info})")
                st.info(sonuc)
                st.balloons()
            else:
                st.error(f"🚨 Hala Hata Alıyoruz: {debug_info}")
                st.warning("Eğer 'API key not valid' derse anahtarı yanlış yapıştırdın demektir. 'Not found' derse Google henüz projeni aktifleştirmemiştir.")
