import streamlit as st
import requests

# 1. YENİ VERDİĞİN ANAHTARI BURAYA EKLEDİM
API_KEY = "AIzaSyADgezoMbaavhLi0vac6lMUOkoRfKeh47w"

st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir_final(kelimeler, yil, ton):
    # En kapsayıcı ve en yeni model ismini kullanıyoruz
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": f"Sen Altınay'ın arkadaşısın. Altınay her konuda efsanevi bir anısı olan biridir. {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. Birinci şahıs ağzından anlat, samimi olsun."}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        
        if response.status_code == 200:
            res_json = response.json()
            # Yanıtı ekrana basıyoruz
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            # Hata varsa sebebini net görelim
            return f"🚨 Google Hatası ({response.status_code}): {response.text}"
            
    except Exception as e:
        return f"🚨 Bağlantı Hatası: {str(e)}"

# ARAYÜZ TASARIMI
st.markdown("<h1 style='text-align: center;'>🎭 Altınay Anı Üretici</h1>", unsafe_allow_html=True)
st.write("---")

kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: nasa, lahmacun, pazar arabası")
yil = st.slider("📅 Yıl", 1990, 2026, 2020)
ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Nostaljik"])

if st.button("✨ Efsanevi Anıyı Getir", use_container_width=True):
    if kelimeler:
        with st.spinner("🌀 Altınay o günü hatırlamaya çalışıyor..."):
            sonuc = aniyi_getir_final(kelimeler, yil, ton)
            
            st.markdown("---")
            if "🚨" in sonuc:
                st.error(sonuc)
                st.info("İpucu: Eğer 403 hatası gelirse Google Cloud'da Billing (Ödeme) kısmını kontrol etmelisin.")
            else:
                st.markdown(f"### 📖 {yil} Yılından Bir Kare")
                st.success(sonuc)
                st.balloons()
    else:
        st.warning("Lütfen Altınay'a bir ipucu (kelime) verin!")
