import streamlit as st
import google.generativeai as genai

# 1. SAYFA KONFİGÜRASYONU
st.set_page_config(
    page_title="Altınay Anı Üretici",
    page_icon="🎭",
    layout="centered"
)

# 2. ŞIK GÖRSEL TASARIM
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .ani-kutusu {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #6c5ce7;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: #1f1f1f;
        font-family: 'serif';
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .baslik { color: #6c5ce7; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. API YAPILANDIRMASI
# Streamlit Secrets'ta GEMINI_API_KEY tanımlı olmalıdır.
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🔑 API anahtarı Secrets kısmında bulunamadı!")
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# 4. ANI ÜRETME FONKSİYONU (404 HATASI ÖNLEYİCİ)
def ani_uret(kelimeler, yil, ton):
    # Senin hatanı çözmek için model ismini v1 standardına çekiyoruz
    # 'gemini-1.5-flash' yerine en temel 'gemini-pro' deniyoruz
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Sen Altınay'ın yakın bir arkadaşısın. Altınay'ın her konuda efsanevi bir anısı vardır.
        Şu anahtar kelimelerle ilgili {yil} yılında yaşanmış {ton} bir anı anlat: {kelimeler}
        
        Kurallar:
        - Birinci şahıs (ben) ağzından anlat.
        - Altınay'ın bu konudaki absürtlüğünü vurgula.
        - Yaklaşık 200 kelime olsun.
        - Direkt hikayeye başla.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Eğer yukarıdaki de hata verirse 1.5-flash sürümünü tam yol ile dene
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            return f"Üretim Hatası: {str(e2)}"

# 5. ARAYÜZ TASARIMI
st.markdown("<h1 class='baslik'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.write("---")

# Kullanıcı Girişleri
kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: helikopter, pazar tezgahı, kuantum fiziği")

col1, col2 = st.columns(2)
with col1:
    yil = st.number_input("📅 Yıl", 1990, 2026, 2018)
with col2:
    ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik", "Nostaljik"])

st.markdown("<br>", unsafe_allow_html=True)
if st.button("✨ Efsanevi Anıyı Getir", use_container_width=True):
    if kelimeler:
        with st.spinner("🌀 Altınay o günü hatırlıyor..."):
            sonuc = ani_uret(kelimeler, yil, ton)
            st.markdown(f"### 📖 Altınay'ın {yil} Serüveni")
            st.markdown(f'<div class="ani-kutusu">{sonuc}</div>', unsafe_allow_html=True)
            
            # Eğlence
            if "Hata" not in sonuc:
                st.balloons()
    else:
        st.warning("Lütfen birkaç kelime yazın.")

st.sidebar.title("📌 Not")
st.sidebar.info("Eğer 404 hatası almaya devam ederseniz, Google AI Studio'dan yeni bir API anahtarı alıp Secrets kısmını güncelleyin.")
