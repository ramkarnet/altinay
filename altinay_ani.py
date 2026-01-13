import streamlit as st
import requests

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# 2. DOĞRUDAN API ANAHTARI
API_KEY = "AIzaSyCcwB7zXrnJqTpdAjd4-NSSKVATE25D7Nk"

# 3. GÖRSEL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .ani-kart {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #6c5ce7;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a1a;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. ÇALIŞAN MODELİ BULAN FONKSİYON
def aniyi_uret_ne_varsa(kelimeler, yil, ton):
    # Denenecek model isimleri
    modeller = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    
    prompt = f"Sen Altınay'ın arkadaşısın. {yil} yılında geçen, {kelimeler} konulu {ton} bir anı anlat. 1. şahıs ağzından anlat."
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    # Hangi sürümde (v1 veya v1beta) çalışacağını bulmak için tarıyoruz
    for ver in ["v1", "v1beta"]:
        for model in modeller:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={API_KEY}"
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    res_json = response.json()
                    return res_json['candidates'][0]['content']['parts'][0]['text'], model
            except:
                continue
    
    return None, None

# 5. ARAYÜZ
st.title("🎭 ALTINAY ANI ÜRETİCİ")

kelimeler = st.text_input("🔑 Anahtar Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2018)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik"])

if st.button("✨ Anıyı Getir"):
    if kelimeler:
        with st.spinner("Altınay'ın hafızası taranıyor..."):
            sonuc, aktif_model = aniyi_uret_ne_varsa(kelimeler, yil, ton)
            
            if sonuc:
                st.markdown(f"### 📖 Altınay'ın {yil} Serüveni")
                st.markdown(f'<div class="ani-kart">{sonuc}</div>', unsafe_allow_html=True)
                st.caption(f"Kullanılan Model: {aktif_model}")
                st.balloons()
            else:
                st.error("🚨 Hata: Hesabınızdaki hiçbir model henüz API üzerinden erişime açılmamış.")
                st.info("Google Cloud Console'da 'Generative Language API' hizmetinin aktif olduğundan ve anahtarın doğru olduğundan emin olun.")
