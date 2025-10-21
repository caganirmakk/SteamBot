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
