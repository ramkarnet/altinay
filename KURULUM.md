# 🚀 KURULUM REHBERİ

## 3 ADIM - 5 DAKİKA

---

## ADIM 1: API ANAHTARI AL

1. https://openrouter.ai/keys adresine git
2. **Sign in** tıkla (Google ile giriş yapabilirsin)
3. **Create Key** tıkla
4. İsim ver: `altinay-ani`
5. **Create** tıkla
6. Anahtarı KOPYALA: `sk-or-v1-xxxxxxxxxx`

🎁 İlk kayıtta $1 bedava kredi!

---

## ADIM 2: GITHUB'A YÜKLE

1. https://github.com → Giriş yap

2. **New repository** tıkla

3. **Repository name:** `altinay-ani-uretici`

4. **Public** seç

5. **"uploading an existing file"** tıkla

6. Bu dosyaları sürükle:
   - altinay_ani.py
   - requirements.txt
   - README.md
   - KURULUM.md

7. **Commit changes** tıkla

---

## ADIM 3: STREAMLIT CLOUD

1. https://share.streamlit.io/ adresine git

2. **Sign up** → **Continue with GitHub**

3. **New app** tıkla

4. Ayarlar:
   - Repository: `altinay-ani-uretici`
   - Branch: `main`
   - Main file: `altinay_ani.py`

5. **Advanced settings** tıkla

6. **Secrets** kısmına yaz:
```
OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxx"
```
(Kendi anahtarını yapıştır)

7. **Deploy!** tıkla

8. 2 dakika bekle...

9. ✅ AÇILDI!

---

## 🎉 BİTTİ!

Uygulama linkin:
```
https://altinay-ani.streamlit.app
```

Bu linki arkadaşlarına gönder!

---

## 📱 ARKADAŞLARINA MESAJ

```
🎭 ALTINAY ANI ÜRETİCİ

AI anı üreteci - Bedava! 😂

Link: https://altinay-ani.streamlit.app

Kullan:
1. Link aç
2. Kelime gir
3. Gül!

✨ Tamamen bedava!
```

---

## 🐛 SORUN GİDERME

### "API key not found"
→ Streamlit Cloud → Settings → Secrets
→ Anahtarı kontrol et

### "Rate limit"
→ Birkaç dakika bekle

### "Model not found"
→ Kod doğru, endişelenme

---

**HEPSI BU KADAR!** 🎉
