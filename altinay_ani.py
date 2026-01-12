import streamlit as st
import google.generativeai as genai

# 1. SAYFA KONFİGÜRASYONU
st.set_page_config(
    page_title="Altınay Anı Üretici",
    page_icon="🎭",
    layout="centered"
)

# 2. ŞIK GÖRSEL TASARIM (CSS)
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

# 3. API YAPILANDIRMASI
# Streamlit Cloud panelinde Settings > Secrets kısmına GEMINI_API_KEY eklediğinizden emin olun!
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.warning("⚠️ API anahtarı Secrets kısmında bulunamadı!")
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# 4. ANI ÜRETME FONKSİYONU (HATA ÖNLEYİCİ)
def ani_uret(kelimeler, yil, ton):
    # En stabil modelleri sırayla dener
    modeller = ['models/gemini-1.5-flash', 'models/gemini-pro']
    
    prompt = f"""
    Sen Altınay'ın en yakın arkadaşısın. 
    Altınay: Her şeyle bir anısı olan, inanılmaz şanslı veya tuhaf olaylar yaşayan efsane biridir.
    
    Görev: {yil} yılında geçen, içinde şu anahtar kelimelerin olduğu bir anı anlat: {kelimeler}
    Anı Tonu: {ton}
    
    Kurallar:
    - Birinci şahıs (ben) ağzından anlat.
    - Altınay'ın bu konudaki absürt bir anısını detaylandır.
    - Yaklaşık 200-250 kelime olsun.
    - Sadece anıyı yaz, giriş/açıklama yapma.
    """

    last_error = ""
    for model_adi in modeller:
        try:
            model = genai.GenerativeModel(model_adi)
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = str(e)
            continue # Bu model hata verirse diğerini dene
            
    return f"Maalesef anı üretilemedi. Hata: {last_error}"

# 5. ARAYÜZ (UI) TASARIMI
st.markdown("<h1 class='main-title'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Her şeyle anısı olan o efsane arkadaş...</p>", unsafe_allow_html=True)

# Giriş Bölümü
with st.container():
    st.markdown("---")
    kelimeler = st.text_input("🔑 Anahtar Kelimeler (Örn: pizza, nasa, kedi, kutuplar)", placeholder="Neyle ilgili bir anı olsun?")
    
    col1, col2 = st.columns(2)
    with col1:
        yil = st.slider("📅 Hangi Yıldı?", 1990, 2026, 2018)
    with col2:
        ton = st.selectbox("🎭 Anının Havası", ["Komik", "Absürt", "Epik", "Dramatik", "Nostaljik"])

    st.markdown("<br>", unsafe_allow_html=True)
    uret_btn = st.button("✨ Efsanevi Anıyı Getir", use_container_width=True)

# Sonuç Ekranı
if uret_btn:
    if not kelimeler:
        st.warning("Altınay'ın hafızasını tazelemek için birkaç kelime yazmalısın!")
    else:
        with st.spinner("🌀 Altınay o günü hatırlamaya çalışıyor..."):
            ani_sonucu = ani_uret(kelimeler, yil, ton)
            
            st.markdown(f"### 📖 Altınay'ın {yil} Serüveni")
            st.markdown(f'<div class="ani-kart"><i>"{ani_sonucu}"</i></div>', unsafe_allow_html=True)
            
            # Alt Etkileşimler
            st.write("---")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("👍 Efsane!"): st.balloons()
            with c2:
                if st.button("😂 Sesli Güldüm"): st.snow()
            with c3:
                st.button("🔄 Yeni Anı") # Sayfayı otomatik yeniler

# Sidebar
st.sidebar.title("📌 İpucu")
st.sidebar.info("Altınay her şeyi bilir, her yerdedir. Ne kadar absürt kelimeler seçersen o kadar şaşırırsın!")
st.sidebar.caption("v2.0 - Billing & Model Fix")
