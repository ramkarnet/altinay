import streamlit as st
import google.generativeai as genai

# 1. SAYFA AYARLARI
st.set_page_config(
    page_title="Altınay Anı Üretici v2.0",
    page_icon="🎭",
    layout="centered"
)

# 2. GÖRSEL TASARIM (CSS)
st.markdown("""
    <style>
    .ani-kart {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #ff4b4b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #31333F;
        font-style: italic;
        line-height: 1.6;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 25px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API YAPILANDIRMASI
# Streamlit Cloud'da "Settings > Secrets" kısmına GEMINI_API_KEY eklemeyi unutmayın!
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🔑 API anahtarı bulunamadı. Lütfen Secrets kısmına ekleyin.")
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# 4. ANI ÜRETME FONKSİYONU
def ani_uret(kelimeler, yil, ton):
    # Hata aldığın modelleri tek tek deneyen sağlam yapı
    modeller = ['gemini-1.5-flash', 'gemini-pro']
    
    prompt = f"""
    Sen Altınay'ın yakın bir arkadaşısın. Altınay HER ŞEYLE anısı olan, inanılmaz biridir.
    
    Şu anahtar kelimelerle ilgili {yil} yılında yaşanmış bir anı anlat: {kelimeler}
    Anı tonu: {ton}
    
    Kurallar:
    - Birinci şahıs (ben) ağzından anlat (Örn: "O gün Altınay'la beraber...")
    - 200-300 kelime arası olsun.
    - Sadece anıyı yaz, "Tabii ki işte anı" gibi girişler yapma.
    """

    for model_adi in modeller:
        try:
            model = genai.GenerativeModel(model_adi)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue # Bu model çalışmazsa sonrakine geç
    
    return "Maalesef şu an anı üretilemiyor. API anahtarınızı veya model erişiminizi kontrol edin."

# 5. ARAYÜZ TASARIMI
st.title("🎭 ALTINAY ANI ÜRETİCİ")
st.markdown("---")

with st.sidebar:
    st.header("📖 Hakkında")
    st.write("Altınay, dünyanın en çok anıya sahip insanıdır. Siz sadece konu verin, o mutlaka oradaydı!")
    st.divider()
    st.caption("v2.0 - GitHub Deploy Hazır")

# Giriş Alanları
col1, col2 = st.columns([3, 1])
with col1:
    kelimeler = st.text_input("🔑 Anahtar Kelimeler (Virgülle ayırın)", placeholder="Ekmek arası, uzay gemisi, halay")
with col2:
    yil = st.number_input("📅 Yıl", 1990, 2025, 2018)

ton = st.select_slider(
    "🎭 Anının Havası",
    options=["Dramatik", "Komik", "Nostaljik", "Epik", "Absürt"]
)

if st.button("✨ Efsanevi Anıyı Getir"):
    if kelimeler:
        with st.spinner("🌀 Altınay'ın hafızası taranıyor..."):
            ani_sonucu = ani_uret(kelimeler, yil, ton)
            
            st.markdown(f"### 📖 Altınay'ın {yil} Serüveni")
            st.markdown(f'<div class="ani-kart">{ani_sonucu}</div>', unsafe_allow_html=True)
            
            # Etkileşim
            st.write("---")
            c1, c2, c3 = st.columns(3)
            if c1.button("👍 Harika!"): st.balloons()
            if c2.button("😂 Sesli Güldüm"): st.snow()
            if c3.button("🔄 Yeni Anı"): st.rerun()
    else:
        st.warning("Altınay'ın bir şeyler hatırlaması için anahtar kelime girmelisin!")
