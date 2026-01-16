import streamlit as st
import requests

# 1. GÜVENLİK: Anahtarı Secrets (Gizli Kasa) üzerinden çekiyoruz
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🚨 Hata: Streamlit Secrets kısmına 'GEMINI_API_KEY' eklenmemiş!")
    st.stop()

# Sayfa Ayarları
st.set_page_config(page_title="Altınay Anı Üretici", page_icon="🎭")

def aniyi_getir_israrli(kelimeler, yil, ton):
    """
    404 hatalarını aşmak için farklı model isimlerini sırayla dener.
    """
    # Google'ın tanıdığı tüm olası model isimleri
    model_listesi = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]
    
    # API Sürümleri
    versiyonlar = ["v1beta", "v1"]
    
    prompt = f"Sen Altınay adında, her konuda efsanevi bir anısı olan bir karakterin arkadaşısın. {yil} yılında geçen, konusu '{kelimeler}' olan {ton} bir anı anlat. Birinci şahıs ağzından anlat, samimi ve etkileyici olsun."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    # Tüm kombinasyonları dene (En sağlam yolu bulana kadar)
    for ver in versiyonlar:
        for model in model_listesi:
            url = f"https://generativelanguage.googleapis.com/{ver}/models/{model}:generateContent?key={API_KEY}"
            try:
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    res_json = response.json()
                    return res_json['candidates'][0]['content']['parts'][0]['text'], model
            except:
                continue
    
    # Eğer her şey başarısız olursa son hata mesajını döndür
    return None, None

# --- ARAYÜZ ---
st.markdown("<h1 style='text-align: center;'>🎭 Altınay Anı Üretici</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)
with col1:
    kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: pizza, nasa, kedi")
with col2:
    ton = st.selectbox("🎭 Anı Tonu", ["Komik", "Absürt", "Epik", "Duygusal"])

yil = st.slider("📅 Yıl", 1990, 2026, 2020)

if st.button("✨ Efsanevi Anıyı Getir", use_container_width=True):
    if kelimeler:
        with st.spinner("🌀 Altınay hafızasını zorluyor, o günü hatırlamaya çalışıyor..."):
            sonuc, kullanilan_model = aniyi_getir_israrli(kelimeler, yil, ton)
            
            st.markdown("---")
            if sonuc:
                st.markdown(f"### 📖 {yil} Yılından Bir Hatıra")
                st.info(sonuc)
                st.caption(f"🚀 Sistem Notu: Bu anı {kullanilan_model} modeli ile başarıyla getirildi.")
                st.balloons()
            else:
                st.error("🚨 Google hala anahtarı onaylıyor veya model erişimi kısıtlı.")
                st.warning("Lütfen Cloud Console'da 'Don't restrict key' seçeneğinin işaretli ve kaydedilmiş olduğunu kontrol edin.")
    else:
        st.warning("Lütfen Altınay'a hatırlaması için bir kelime verin!")

# Alt Bilgi
st.markdown("---")
st.caption("Altınay Anı Projesi - 2026")
