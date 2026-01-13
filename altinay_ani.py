import streamlit as st
import requests
import json

# Sayfa Ayarları
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# CSS
st.markdown("""<style>.stApp { background-color: #f0f2f6; } .ani-kart { background-color: white; padding: 20px; border-radius: 15px; border-left: 8px solid #6c5ce7; color: black; }</style>""", unsafe_allow_html=True)

# API Ayarı
API_KEY = st.secrets.get("GEMINI_API_KEY")

def ani_uret_direct(kelimeler, yil, ton):
    # Kütüphane kullanmadan doğrudan v1 endpoint'ine istek atıyoruz (404 hatasını çözmek için)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt_text = f"Sen Altınay'ın en yakın arkadaşısın. Altınay her konuda efsanevi bir anısı olan biridir. {yil} yılında geçen, anahtar kelimeleri '{kelimeler}' olan {ton} bir anı anlat. Birinci şahıs ağzından anlat, 200 kelime olsun."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        # Yanıtı parse et
        if response.status_code == 200:
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Google Hatası ({response.status_code}): {res_json.get('error', {}).get('message', 'Bilinmeyen hata')}"
    except Exception as e:
        return f"Bağlantı Hatası: {str(e)}"

# Arayüz
st.title("🎭 ALTINAY ANI ÜRETİCİ")
st.write("Her şeyle anısı olan efsane arkadaş...")

kelimeler = st.text_input("🔑 Anahtar Kelimeler")
yil = st.slider("📅 Yıl", 1990, 2026, 2018)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik"])

if st.button("✨ Anı Üret"):
    if not API_KEY:
        st.error("API Key eksik!")
    elif kelimeler:
        with st.spinner("Altınay hatırlıyor..."):
            sonuc = ani_uret_direct(kelimeler, yil, ton)
            st.markdown("---")
            st.markdown(f'<div class="ani-kart">{sonuc}</div>', unsafe_allow_html=True)
            if "Hatası" not in sonuc:
                st.balloons()
    else:
        st.warning("Kelime girin!")
