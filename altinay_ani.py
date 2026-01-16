import streamlit as st
import requests

# 1. GÜVENLİK: Anahtarı mutlaka Secrets'tan çekin
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🚨 Hata: Streamlit Secrets kısmına 'GEMINI_API_KEY' eklenmemiş!")
    st.stop()

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir_2026(kelimeler, yil, ton):
    # Ocak 2026 itibarıyla en sağlam model hiyerarşisi
    # 'gemini-1.5-flash-latest' bazen 404 verebilir, 'gemini-1.5-flash' daha stabildir.
    modeller = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]
    
    payload = {
        "contents": [{"parts": [{"text": f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. Samimi ol."}]}]
    }

    for model in modeller:
        # v1beta yerine v1 kullanımı 2026'da daha yaygınlaştı
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={API_KEY}"
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                res_json = response.json()
                return res_json['candidates'][0]['content']['parts'][0]['text'], model
        except:
            continue
            
    return None, None

# --- ARAYÜZ ---
st.title("🎭 Altınay Anı Üretici")
st.write("2026 Ocak Güncel Sürüm")

k = st.text_input("🔑 Anahtar Kelimeler")
y = st.slider("📅 Yıl", 1990, 2026, 2020)

if st.button("✨ Anıyı Getir"):
    if k:
        with st.spinner("🌀 Altınay o günü hatırlıyor..."):
            sonuc, aktif_model = aniyi_getir_2026(k, y, "Komik")
            if sonuc:
                st.success(sonuc)
                st.caption(f"🚀 Çalışan Model: {aktif_model}")
            else:
                st.error("🚨 Google 404 Hatası: Model henüz hesabınızda aktif değil.")
                st.info("Çözüm: Google AI Studio'dan (aistudio.google.com) YEPYENİ bir anahtar oluşturup Secrets'a yapıştırın.")
