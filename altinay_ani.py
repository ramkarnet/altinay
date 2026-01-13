import streamlit as st
import requests
import json

# Sayfa Ayarları
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

# Şıklaştıran CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .ani-kart {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 10px solid #ff4b4b;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a1a;
        font-family: 'Georgia', serif;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# API Ayarı - Secrets'tan alıyoruz
API_KEY = st.secrets.get("GEMINI_API_KEY")

def ani_uret_v1_stable(kelimeler, yil, ton):
    # Hata veren v1beta yerine doğrudan v1 (STABLE) adresini kullanıyoruz
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    prompt_text = (
        f"Sen Altınay'ın en yakın arkadaşısın. Altınay her konuda efsanevi bir anısı olan, "
        f"her ortamda tanıdığı olan çok özel biridir. {yil} yılında geçen, "
        f"anahtar kelimeleri '{kelimeler}' olan {ton} bir anı anlat. "
        f"Birinci şahıs (ben) ağzından anlat, samimi ol ve 200 kelime civarı olsun. "
        f"Sadece hikayeyi yaz."
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        
        if response.status_code == 200:
            # Başarılı yanıtı parse et
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Hata varsa detayını göster
            error_msg = res_json.get('error', {}).get('message', 'Bilinmeyen hata')
            return f"🚨 Google v1 Hatası: {error_msg}"
            
    except Exception as e:
        return f"🚨 Bağlantı Hatası: {str(e)}"

# Arayüz Tasarımı
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.write("---")

kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: pazar arabası, uzaylılar, lahmacun")

c1, c2 = st.columns(2)
with c1:
    yil = st.slider("📅 Yıl", 1990, 2026, 2015)
with c2:
    ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik", "Nostaljik"])

if st.button("✨ Efsanevi Anıyı Canlandır", use_container_width=True):
    if not API_KEY:
        st.error("API Anahtarı (GEMINI_API_KEY) Secrets kısmında bulunamadı!")
    elif not kelimeler:
        st.warning("Altınay'a bir ipucu verin (kelime girin)!")
    else:
        with st.spinner("🌀 Altınay'ın hatıraları taranıyor..."):
            sonuc = ani_uret_v1_stable(kelimeler, yil, ton)
            
            if "🚨" in sonuc:
                st.error(sonuc)
            else:
                st.markdown(f"### 📖 {yil} Yılından Bir Kare...")
                st.markdown(f'<div class="ani-kart"><i>"{sonuc}"</i></div>', unsafe_allow_html=True)
                st.balloons()

# Alt Bilgi
st.sidebar.title("📌 Teknik Bilgi")
st.sidebar.write("Bu uygulama Google Gemini v1 API (Stable) kullanmaktadır.")
