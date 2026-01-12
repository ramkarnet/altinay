import streamlit as st
import google.generativeai as genai
import random

# Sayfa Ayarları
st.set_page_config(
    page_title="Altınay Anı Üretici v2.0",
    page_icon="🎭",
    layout="centered"
)

# Custom CSS - Uygulamayı şıklaştıralım
st.markdown("""
    <style>
    .ani-kart {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# API Anahtarı Yönetimi
# GitHub'a yükleyeceğimiz için anahtarı direkt koda yazmıyoruz, st.secrets kullanıyoruz.
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Streamlit Cloud ayarlarından GEMINI_API_KEY ekleyin.")

# Yan Panel (Sidebar)
with st.sidebar:
    st.title("📖 Nasıl Çalışır?")
    st.info("Altınay, her olayın merkezinde olan o efsane arkadaştır. Anahtar kelimeleri seçin ve onun inanılmaz geçmişine yolculuk yapın.")
    st.markdown("---")
    st.caption("v2.0 - Altınay Geliştirici Sürümü")

# Ana Ekran
st.title("🎭 ALTINAY ANI ÜRETİCİ")
st.subheader("Her şeyle anısı olan efsane arkadaşınız için...")

# Form Alanı
with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        kelimeler = st.text_input("🔑 Anahtar Kelimeler", placeholder="Örn: pizza, kedi, matematik, gizli servis")
    with col2:
        yil = st.number_input("📅 Yıl", min_value=1990, max_value=2024, value=2015)
    
    ton = st.select_slider(
        "🎭 Anı Tonu",
        options=["Dramatik", "Komik", "Nostaljik", "Epik", "Absürt"],
        value="Komik"
    )

    uret_btn = st.button("✨ Efsanevi Anıyı Üret", type="primary")

# Anı Üretme Fonksiyonu
def ani_uret(kelimeler, yil, ton):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Sen Altınay'ın yakın bir arkadaşısın ve onun hakkında bir anı anlatıyorsun. 
    Altınay gerçekten HER ŞEYLE anısı olan, inanılmaz deneyimleri olan birisidir.
    Kişilik: Altınay her zaman doğru zamanda yanlış yerde olan biridir.

    Şu anahtar kelimelerle ilgili {yil} yılında yaşanmış bir Altınay anısı üret: {kelimeler}
    Anı {ton} tonda olmalı.
    
    Kurallar:
    - Birinci şahıs (ben) perspektifinden anlat.
    - Anı gerçekçi detaylar içermeli ama Altınay'ın bu konudaki dehasını/şanssızlığını/absürtlüğünü vurgulamalı.
    - 200-300 kelime arası olsun.
    - Sadece anıyı yaz, giriş cümlesi (İşte anı vs.) ekleme.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Sonuç Ekranı
if uret_btn:
    if not kelimeler:
        st.warning("Lütfen birkaç anahtar kelime girin!")
    else:
        with st.spinner("🎭 Altınay arşivi taranıyor, anı canlanıyor..."):
            try:
                ani = ani_uret(kelimeler, yil, ton)
                st.session_state['son_ani'] = ani
                
                st.markdown(f"### 📖 Altınay'ın {yil} Anısı")
                st.markdown(f"**Etiketler:** `{kelimeler}` | **Ton:** `{ton}`")
                
                st.markdown(f'<div class="ani-kart"><i>{ani}</i></div>', unsafe_allow_html=True)
                
                # Etkileşim Butonları
                c1, c2, c3 = st.columns(3)
                if c1.button("👍 Harika!"):
                    st.balloons()
                if c2.button("😂 Çok Komik"):
                    st.snow()
                c3.link_button("🔄 Yeni Anı", "/")
                
            except Exception as e:

                st.error(f"Bir hata oluştu: {e}")
