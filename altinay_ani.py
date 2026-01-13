import streamlit as st
import requests
import json

# 1. SAYFA AYARLARI
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# 2. DOĞRUDAN API ANAHTARI (Verdiğin 2. Key)
# Not: Normalde Secrets kullanılır ama çalışması için buraya sabitliyoruz.
API_KEY = "AIzaSyCcwB7zXrnJqTpdAjd4-NSSKVATE25D7Nk"

# 3. GÖRSEL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .ani-kart {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #6c5ce7;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a1a;
        font-family: 'Georgia', serif;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. ANI ÜRETME FONKSİYONU
def ani_uret_v1(kelimeler, yil, ton):
    # En garantici v1 endpoint
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    prompt_text = (
        f"Sen Altınay'ın en yakın arkadaşısın. Altınay her konuda efsanevi bir anısı olan biridir. "
        f"{yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. "
        f"Birinci şahıs (ben) ağzından anlat, samimi ol ve 150 kelime civarı olsun."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
        res_json = response.json()
        
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            error_message = res_json.get('error', {}).get('message', 'Bilinmeyen Hata')
            return f"🚨 Google Hatası: {error_message}"
    except Exception as e:
        return f"🚨 Bağlantı Hatası: {str(e)}"

# 5. ARAYÜZ
st.markdown("<h1 style='text-align: center; color: #6c5ce7;'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.write("---")

kelimeler = st.text_input("🔑 Anahtar Kelimeler (Örn: uzay yolu, dondurma)")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik"])

if st.button("✨ Efsanevi Anıyı Getir", use_container_width=True):
    if not kelimeler:
        st.warning("Lütfen bir anahtar kelime girin!")
    else:
        with st.spinner("🌀 Altınay o günü hatırlıyor..."):
            sonuc = ani_uret_v1(kelimeler, yil, ton)
            
            if "🚨" in sonuc:
                st.error(sonuc)
            else:
                st.markdown(f"### 📖 {yil} Yılından Bir Kare")
                st.markdown(f'<div class="ani-kart">{sonuc}</div>', unsafe_allow_html=True)
                st.balloons()

st.sidebar.caption("v2.1 - API Key Hardcoded")
