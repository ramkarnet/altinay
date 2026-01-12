import streamlit as st
import google.generativeai as genai

# 1. Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Altınay Anı Üretici v2.0",
    page_icon="🎭",
    layout="centered"
)

# 2. Şık Arayüz Tasarımı (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .ani-kart {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        border-right: 10px solid #6c5ce7;
        border-left: 10px solid #6c5ce7;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        color: #2d3436;
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    .main-title { color: #6c5ce7; text-align: center; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. API Yapılandırması
try:
    # Streamlit Secrets'tan anahtarı alıyoruz
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ API anahtarı Secrets kısmına eklenmemiş!")

# 4. Anı Üretme Fonksiyonu
def ani_uret(kelimeler, yil, ton):
    # Billing tanımlı olduğu için doğrudan en iyi modeli kullanıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Sen Altınay'ın en yakın arkadaşısın. Altınay dünyayı gezmiş, her türlü tuhaf işe bulaşmış, 
    her konuda bir 'tanıdığı' olan ve her olaydan sağ çıkmayı başaran efsanevi bir karakterdir.
    
    Görev: {yil} yılında geçen, içinde şu anahtar kelimelerin olduğu bir anı anlat: {kelimeler}
    Anı Tonu: {ton}
    
    Kurallar:
    - Anlatıcı 'ben' olmalı (Sanki bir masada oturmuş anlatıyorsun).
    - Altınay'ın bu konudaki uzmanlığını veya şansını vurgula.
    - 250 kelime civarı olsun.
    - Direkt anıya başla, giriş/sunuş yapma.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Üretim sırasında bir hata oluştu: {str(e)}"

# 5. Arayüz
st.markdown("<h1 class='main-title'>🎭 ALTINAY ANI ÜRETİCİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Efsane arkadaşınız Altınay'ın bitmek bilmeyen anıları...</p>", unsafe_allow_html=True)

# Form Alanları
with st.expander("🛠️ Anı Parametrelerini Ayarla", expanded=True):
    kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: gizli ajanlar, lahmacun, jet ski")
    c1, c2 = st.columns(2)
    with c1:
        yil = st.slider("📅 Yıl", 1990, 2025, 2015)
    with c2:
        ton = st.selectbox("🎭 Ton", ["Komik", "Absürt", "Epik", "Dramatik", "Nostaljik"])

if st.button("✨ Efsaneyi Canlandır"):
    if kelimeler:
        with st.spinner("🌀 Altınay'ın tozlu arşivi açılıyor..."):
            ani = ani_uret(kelimeler, yil, ton)
            st.markdown("### 📖 İşte O Unutulmaz Anı...")
            st.markdown(f'<div class="ani-kart"><i>"{ani}"</i></div>', unsafe_allow_html=True)
            
            # Animasyonlar
            if ton == "Komik" or ton == "Absürt":
                st.balloons()
            else:
                st.snow()
    else:
        st.warning("Lütfen Altınay'ın hatırlayabilmesi için bir şeyler (kelime) girin!")

# Alt Bilgi
st.sidebar.markdown("---")
st.sidebar.write("💡 **İpucu:** Ne kadar alakasız kelimeler girerseniz Altınay o kadar yaratıcı olur!")
