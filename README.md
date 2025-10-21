
# 🎮 SteamBot: Dinamik FPS Performans Asistanı

[![Open in Hugging Face Spaces](https://img.shields.io/badge/🚀%20Uygulamayı%20Aç-Click%20Here-blue?style=for-the-badge)](https://huggingface.co/spaces/caganirmak/SteamBot)

SteamBot, **Google Gemini** modeli ve **Steam API** desteğiyle çalışan,  
oyunlar için **gerçek zamanlı FPS tahmini** yapan yapay zeka tabanlı bir asistandır.  
Streamlit arayüzüyle, sade ve etkileşimli bir kullanıcı deneyimi sunar.

---

## 📘 Proje Özeti

Bu proje, kullanıcının sistem donanımını analiz ederek seçilen Steam oyununda  
**tahmini FPS performansı** üretir.  
Statik veri setleri yerine **anlık veri çekme (real-time retrieval)** yaparak  
her zaman güncel sistem gereksinimlerini kullanır.

---

## 🧠 Mimari Yapı (Nasıl Çalışır?)

1. **🎯 Giriş (Input):**  
   Kullanıcı sistem bilgilerini (CPU, GPU, RAM) ve oyunun Steam URL’sini girer.

2. **🔍 Kimlik Çıkarımı:**  
   `extract_app_id()` fonksiyonu, URL içinden oyun App ID’sini bulur.

3. **🌐 Dinamik Veri Çekme:**  
   `fetch_steam_requirements()` fonksiyonu, Steam API’ye sorgu atarak  
   oyunun güncel sistem gereksinimlerini çeker.  
   → `https://store.steampowered.com/api/appdetails`

4. **🧹 Veri İşleme:**  
   Dönen HTML formatlı metinler, `BeautifulSoup` yardımıyla temizlenir.

5. **⚙️ Bağlam Zenginleştirme (RAG):**  
   Steam verileri + Kullanıcı donanımı + Sistem prompt’u  
   → Google Gemini için anlamlı bir bağlama dönüştürülür.

6. **💬 Yanıt Üretimi:**  
   Gemini modeli, verileri analiz eder ve gerçek verilere dayalı FPS tahmini sunar.

---

## 🧩 Kullanılan Teknolojiler

| Teknoloji | Amaç |
|------------|-------|
| **Streamlit** | Web arayüzü oluşturma |
| **Google Gemini (gemini-2.5-flash)** | FPS tahmini üretimi |
| **Requests** | Steam API veri çekimi |
| **BeautifulSoup4** | HTML verisini temizleme |
| **Python-dotenv** | API anahtarlarını güvenli saklama |

---

## ⚙️ Kurulum Adımları

### 1️⃣ Depoyu Klonla
```bash
git clone https://github.com/caganirmakk/SteamBot
cd SteamBot

````markdown
# 🎮 SteamBot: Dinamik FPS Performans Asistanı

[![Open in Hugging Face Spaces](https://img.shields.io/badge/🚀%20Uygulamayı%20Aç-Click%20Here-blue?style=for-the-badge)](https://huggingface.co/spaces/caganirmak/SteamBot)

SteamBot, **Google Gemini** modeli ve **Steam API** desteğiyle çalışan,  
oyunlar için **gerçek zamanlı FPS tahmini** yapan yapay zeka tabanlı bir asistandır.  
Streamlit arayüzüyle, sade ve etkileşimli bir kullanıcı deneyimi sunar.

---

## 📘 Proje Özeti

Bu proje, kullanıcının sistem donanımını analiz ederek seçilen Steam oyununda  
**tahmini FPS performansı** üretir.  
Statik veri setleri yerine **anlık veri çekme (real-time retrieval)** yaparak  
her zaman güncel sistem gereksinimlerini kullanır.

---

## 🧠 Mimari Yapı (Nasıl Çalışır?)

1. **🎯 Giriş (Input):**  
   Kullanıcı sistem bilgilerini (CPU, GPU, RAM) ve oyunun Steam URL’sini girer.

2. **🔍 Kimlik Çıkarımı:**  
   `extract_app_id()` fonksiyonu, URL içinden oyun App ID’sini bulur.

3. **🌐 Dinamik Veri Çekme:**  
   `fetch_steam_requirements()` fonksiyonu, Steam API’ye sorgu atarak  
   oyunun güncel sistem gereksinimlerini çeker.  
   → `https://store.steampowered.com/api/appdetails`

4. **🧹 Veri İşleme:**  
   Dönen HTML formatlı metinler, `BeautifulSoup` yardımıyla temizlenir.

5. **⚙️ Bağlam Zenginleştirme (RAG):**  
   Steam verileri + Kullanıcı donanımı + Sistem prompt’u  
   → Google Gemini için anlamlı bir bağlama dönüştürülür.

6. **💬 Yanıt Üretimi:**  
   Gemini modeli, verileri analiz eder ve gerçek verilere dayalı FPS tahmini sunar.

---

## 🧩 Kullanılan Teknolojiler

| Teknoloji | Amaç |
|------------|-------|
| **Streamlit** | Web arayüzü oluşturma |
| **Google Gemini (gemini-2.5-flash)** | FPS tahmini üretimi |
| **Requests** | Steam API veri çekimi |
| **BeautifulSoup4** | HTML verisini temizleme |
| **Python-dotenv** | API anahtarlarını güvenli saklama |

---

## ⚙️ Kurulum Adımları

### 1️⃣ Depoyu Klonla
```bash
git clone https://github.com/caganirmakk/SteamBot
cd SteamBot
````

### 2️⃣ Gerekli Kütüphaneleri Yükle

```bash
pip install -r requirements.txt
```

### 3️⃣ API Anahtarını Ayarla

Proje dizinine `.env` dosyası oluştur ve içine şunu ekle:

```bash
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
GEMINI_MODEL="gemini-2.0-flash"
```

### 4️⃣ Uygulamayı Başlat

```bash
streamlit run app.py
```

---

## 💡 Kullanım Kılavuzu

Uygulama açıldığında şu bilgileri girmen yeterli:

* CPU, GPU ve RAM özelliklerin
* Steam oyun linki
  Örnek:

  ```
  https://store.steampowered.com/app/1086940/Baldurs_Gate_3/
  ```

### 🧠 Örnek Kullanım

```
Selam, sistemim Ryzen 7 5800X, ekran kartım RTX 4070 ve 32GB RAM var.
Sence bu oyunu 1080p'de kaç FPS alırım?
https://store.steampowered.com/app/1086940/Baldurs_Gate_3/
```

---

## 🌐 Canlı Demo

🎯 **Hemen Dene:**
👉 [SteamBot - Hugging Face Spaces](https://huggingface.co/spaces/caganirmak/SteamBot)

---

## 📊 Çalışma Akışı

```mermaid
flowchart TD
A[🔹 Kullanıcı Girdisi] --> B[🔍 App ID Çıkarımı]
B --> C[🌐 Steam API'den Veri Çekme]
C --> D[🧹 Gereksinimleri Temizleme]
D --> E[⚙️ Bağlam Oluşturma (RAG)]
E --> F[🤖 Gemini Analizi]
F --> G[📈 FPS Tahmini ve Performans Yorumu]
```

---



```
```
