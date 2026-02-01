import streamlit as st
import requests

# 1. Ayarlar ve Güvenlik
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🚨 Hata: Streamlit Secrets kısmına API anahtarı eklenmemiş!")
    st.stop()

# 2. Anı Üretme Fonksiyonu
def aniyi_getir(kelimeler, yil, ton):
    # 2026'da en stabil çalışan v1 yolu
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen Altınay'ın en yakın arkadaşısın. {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. Samimi ve akıcı olsun."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"🚨 Google Hatası: {response.status_code}. Lütfen anahtarın aktif olduğundan emin ol."
    except Exception as e:
        return f"🚨 Bağlantı Hatası: {str(e)}"

# 3. Arayüz
st.title("🎭 Altınay Anı Üretici")
st.write("Hoş geldin! Altınay'ın efsanevi anılarını yeniden canlandıralım.")

kelimeler = st.text_input("🔑 Hatırlatıcı Kelimeler (Örn: dondurma, uçak)")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Efsanevi", "Dramatik"])

if st.button("✨ Anıyı Hatırla", use_container_width=True):
    if kelimeler:
        with st.spinner("🌀 Altınay uzaklara daldı, hatırlamaya çalışıyor..."):
            sonuc = aniyi_getir(kelimeler, yil, ton)
            st.markdown("---")
            st.info(sonuc)
            if "🚨" not in sonuc: st.balloons()
    else:
        st.warning("Lütfen bir kelime gir ki Altınay hatırlasın!")