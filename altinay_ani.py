import streamlit as st
import requests

# YENİ ANAHTARIN
API_KEY = "AIzaSyADgezoMbaavhLi0vac6lMUOkoRfKeh47w"

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def model_bul_ve_uret(kelimeler, yil, ton):
    # Denenecek tüm olası model varyasyonları
    modeller = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    # Denenecek tüm API sürümleri
    versiyonlar = ["v1beta", "v1"]
    
    prompt = f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, '{kelimeler}' konulu {ton} bir anı anlat. Samimi ol."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    for ver in versiyonlar:
        for m in modeller:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{m}:generateContent?key={API_KEY}"
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    res_json = response.json()
                    # Başarılı olursa anıyı ve kullanılan modeli döndür
                    return res_json['candidates'][0]['content']['parts'][0]['text'], m
            except:
                continue
    
    return None, None

# ARAYÜZ
st.title("🎭 Altınay Anı Üretici")
st.write("Hesabınızdaki en uygun model otomatik olarak seçilecektir.")

kelimeler = st.text_input("🔑 Anahtar Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Nostaljik"])

if st.button("✨ Anıyı Üret"):
    if kelimeler:
        with st.spinner("🌀 Altınay anılarını tarıyor..."):
            sonuc, aktif_model = model_bul_ve_uret(kelimeler, yil, ton)
            
            if sonuc:
                st.markdown("---")
                st.success(sonuc)
                st.caption(f"🚀 Kullanılan Model: {aktif_model}")
                st.balloons()
            else:
                st.error("🚨 Google hala anahtarı ve modelleri hesabınıza tanımlıyor.")
                st.info("İpucu: Google Cloud Console'da 'Generative Language API' servisini kapatıp açmak süreci hızlandırabilir.")
