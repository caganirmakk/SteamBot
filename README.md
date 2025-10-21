

# 🤖 SteamBot: Dinamik FPS Performans Asistanı

**[<-- UYGULAMAYI AÇMAK İÇİN BURAYA TIKLAYIN -->](https://huggingface.co/spaces/caganirmak/SteamBot)**

Bu proje, **Google Gemini** modelini ve **Steam API**'sini kullanarak oyunlar için
gerçek zamanlı FPS tahmini yapan Streamlit tabanlı bir chatbot'tur.

---

## 📋 Proje Hakkında

Bu asistan, kullanıcıların oynamak istedikleri Steam oyunları için
sistemlerinin yeterli olup olmadığını analiz eden ve bir FPS
(saniyedeki kare sayısı) tahmini sunan bir yapay zeka asistanıdır.

Projenin temel amacı, statik ve zamanla eskiyen veri setlerinin aksine,
**canlı ve güncel verilerle** beslenen bir RAG (Retrieval-Augmented Generation)
mimarisi kurmaktır.

Bu sayede, oyunların sistem gereksinimleri güncellendiği anda botun analizleri de
otomatik olarak güncellenmiş olur.

## 💡 Veri Seti ve Mimari (Nasıl Çalışır?)

Bu proje, **Steam API'sini dinamik bir veri seti** olarak kullanır.
Statik bir vektör veritabanı yerine, her sorguda
"Anlık Veri Çekme" (Real-time Retrieval) yöntemini uygular:

1.  **Giriş (Input):**
    Kullanıcı, sistem özelliklerini (CPU, GPU, RAM) ve oyunun Steam mağaza
    URL'ini (`https://store.steampowered.com/app/...`) sohbete girer.

2.  **Kimlik Çıkarımı (ID Extraction):**
    `extract_app_id` fonksiyonu, verilen URL'i analiz eder ve oyunun benzersiz
    Steam App ID'sini çıkarır.

3.  **Dinamik Veri Çekme (Retrieval):**
    `fetch_steam_requirements` fonksiyonu, bu App ID'yi kullanarak o an Steam'in
    resmi API'sine (`store.steampowered.com/api/appdetails`) bir `GET` isteği atar.

4.  **Veri İşleme (Processing):**
    API'den dönen JSON yanıtının içindeki (HTML içeren) minimum ve önerilen
    sistem gereksinimleri metinleri, `parse_requirements` fonksiyonu ve
    `BeautifulSoup` kütüphanesi ile temizlenerek anlamlı bir metin bloğuna
    dönüştürülür.

5.  **Bağlam Zenginleştirme (Augmentation):**
    Çekilen bu **güncel ve resmi** sistem gereksinimleri, kullanıcının kendi sistem
    bilgileriyle ve `SYSTEM_PROMPT` ile birleştirilerek Google Gemini için
    zenginleştirilmiş bir bağlam (`augmented_content`) oluşturulur.

6.  **Yanıt Üretimi (Generation):**
    Gemini, bu zenginleştirilmiş bağlamı analiz eder. Bir "tahmin" yapmak yerine,
    elindeki *gerçek* verilere dayanarak kullanıcıya mantıklı bir FPS aralığı ve
    performans analizi sunar.

## 🛠️ Kullanılan Teknolojiler

* **Streamlit**: Web arayüzü.
* **Google Gemini (gemini-2.5-flash)**: Yanıt ve analiz üretimi (Generation Model).
* **Requests**: Steam API'sinden anlık veri çekmek için.
* **BeautifulSoup4**: Veri işleme ve temizleme.
* **Python-dotenv**: API anahtarlarını güvenli saklamak için.

## 🚀 Çalıştırma Kılavuzu (Kurulum)

### 1. Depoyu Klonlama

```bash
git clone [https://github.com/caganirmakii/SteamBot.git](https://github.com/caganirmakii/SteamBot.git)
cd SteamBot
2. Gerekli Kütüphaneler
Proje için gerekli Python kütüphanelerini yükleyin (Virtual environment kullanmanız önerilir):

Bash

pip install -r requirements.txt
3. API Anahtarlarını Ayarlama
Proje ana dizininde .env adında bir dosya oluşturun ve içine Google AI Studio üzerinden aldığınız API anahtarınızı ekleyin.

GOOGLE_API_KEY="AIzaSy...SİZİN-API-ANAHTARINIZ"
GEMINI_MODEL="gemini-2.0-flash"
4. Uygulamayı Başlatma
Streamlit uygulamasını yerel makinenizde başlatmak için:

Bash

streamlit run app.py
🎯 Ürün Kılavuzu ve Sonuçlar
Deploy Linki: https://huggingface.co/spaces/caganirmak/SteamBot

Çalışma Akışı: Web arayüzü açıldığında, asistana sistem özelliklerinizi (CPU, GPU, RAM) ve analiz edilmesini istediğiniz oyunun Steam mağaza linkini vermeniz yeterlidir.

Sonuç: Bot, Steam API'sinden çektiği güncel verilere dayanarak size bir FPS tahmini ve performans analizi sunacaktır.

Örnek Soru:

"Selam, sistemim Ryzen 7 5800X, ekran kartım RTX 4070 ve 32GB RAM var." "Sence bu oyunu 1080p'de kaç FPS alırım?" "httpsA://https://www.google.com/search?q=store.steampowered.com/app/1086940/Baldurs_Gate_3/"
