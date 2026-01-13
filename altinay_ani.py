import streamlit as st
import requests
import json

# 1. Sayfa Ayarları
st.set_page_config(page_title="Altınay Anı Üretici v2.0", page_icon="🎭", layout="centered")

# 2. Görsel Tasarım (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .ani-kart {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border-left: 10px solid #6c5ce7;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        color: #2d3436;
        font-family: 'serif';
        font-size: 1.15rem;
        line-height: 1.8;
    }
    .main-title { color: #6c5ce7; text-align: center; font-weight: 800; font-size: 2.5rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Ayarı
API_KEY = st.secrets.get("GEMINI_API_KEY")

def ani_uret_final(kelimeler, yil, ton):
    # Denenecek model isimleri (Google bazen isimleri günceller, hepsini tarıyoruz)
    model_listesi = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro",
        "gemini-pro"
    ]
    
    # API versiyonları
    versions = ["v1", "v1beta"]
    
    prompt_text = (
        f"Sen Altınay'ın en yakın arkadaşısın. Altınay her olayla bir bağı olan, "
        f"dünyanın her yerinde tanıdığı olan efsane biridir. "
        f"{yil} yılında geçen, anahtar kelimeleri '{kelimeler}' olan {ton} bir anı anlat. "
        f"Birinci şahıs ağzından anlat, samimi ol ve 200 kelime civarı olsun."
    )
    
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    
    # Tüm kombinasyonları dene (Çalışan modeli bulana kadar)
    for ver in versions:
        for model_name in model_listesi:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model_name}:generateContent?key={API_KEY}"
            try:
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    res_json = response.json()
                    return res_json['candidates'][0]['content']['parts'][0]['text'], model_name
            except:
                continue
                
    return None, None

# 4. Arayüz
st.markdown("<h1 class='main-title'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.write("---")

kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: pizza, nasa, kedi")
c1, c2 = st.columns(2)
with c1:
    yil = st.slider("📅 Yıl", 1990, 2026, 2018)
with c2:
    ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik"])

if st.button("✨ Efsanevi Anıyı Getir", use_container_width=True):
    if not API_KEY:
        st.error("Secrets kısmına GEMINI_API_KEY eklenmemiş!")
    elif kelimeler:
        with st.spinner("🌀 Altınay o günü hatırlamaya çalışıyor..."):
            sonuc, calisan_model = ani_uret_final(kelimeler, yil, ton)
            
            if sonuc:
                st.markdown(f"### 📖 Altınay'ın {yil} Serüveni")
                st.markdown(f'<div class="ani-kart"><i>"{sonuc}"</i></div>', unsafe_allow_html=True)
                st.caption(f"Sistem tarafından kullanılan model: {calisan_model}")
                st.balloons()
            else:
                st.error("🚨 Hata: Hesabınızdaki modeller henüz API üzerinden erişime açılmamış olabilir. Birkaç dakika bekleyip tekrar deneyin.")
    else:
        st.warning("Altınay'a bir ipucu (kelime) verin!")
