

````markdown
# 🤖 SteamBot: Dinamik FPS Performans Asistanı

Bu proje, Akbank Generative AI Giriş Bootcamp için geliştirilmiş, **Google Gemini** modelini ve **Steam API**'sini kullanarak oyunlar için gerçek zamanlı FPS tahmini yapan Streamlit tabanlı bir chatbot'tur.

## 📋 Proje Hakkında

Bu asistan, kullanıcıların sistem özelliklerini (CPU, GPU, RAM) ve oynamak istedikleri oyunun Steam mağaza linkini alarak bir performans analizi sunar.

Projenin temel amacı, statik ve zamanla eskiyen veri setlerinin aksine, **canlı ve güncel verilerle** beslenen bir RAG (Retrieval-Augmented Generation) mimarisi kurmaktır. Bu sayede, oyunların sistem gereksinimleri güncellendiği anda botun analizleri de otomatik olarak güncellenmiş olur.

## 🛠️ Kullanılan Teknolojiler

* **Streamlit**: Web arayüzü ve kullanıcı etkileşimi.
* **Google Gemini (gemini-2.5-flash)**: Zenginleştirilmiş bağlamı analiz etme ve yanıt üretme (LLM).
* **Requests**: Steam API'sine bağlanmak ve anlık veri çekmek için.
* **BeautifulSoup4**: Steam API'sinden gelen HTML formatındaki gereksinim verilerini temizlemek ve işlemek için.
* **Python-dotenv**: API anahtarlarını güvenli bir şekilde saklamak için.

## 💡 Veri Akışı ve Mimarisi (Nasıl Çalışır?)

Bu proje, mentor (Rumeysa Bakar) tavsiyesi doğrultusunda **Steam API'sini dinamik bir veri seti** olarak kullanır. Statik bir vektör veritabanı yerine, her sorguda "Anlık Veri Çekme" (Real-time Retrieval) yöntemini uygular:

1.  **Giriş (Input):** Kullanıcı, sistem özelliklerini (CPU, GPU, RAM) ve oyunun Steam mağaza URL'ini (`https://store.steampowered.com/app/...`) sohbete girer.
2.  **Kimlik Çıkarımı (ID Extraction):** `extract_app_id` fonksiyonu, verilen URL'i analiz eder ve oyunun benzersiz Steam App ID'sini çıkarır.
3.  **Dinamik Veri Çekme (Retrieval):** `fetch_steam_requirements` fonksiyonu, bu App ID'yi kullanarak o an Steam'in resmi API'sine (`store.steampowered.com/api/appdetails`) bir `GET` isteği atar.
4.  **Veri İşleme (Processing):** API'den dönen JSON yanıtının içindeki (HTML içeren) minimum ve önerilen sistem gereksinimleri metinleri, `parse_requirements` fonksiyonu ve `BeautifulSoup` kütüphanesi ile temizlenerek anlamlı bir metin bloğuna dönüştürülür.
5.  **Bağlam Zenginleştirme (Augmentation):** Çekilen bu **güncel ve resmi** sistem gereksinimleri, kullanıcının kendi sistem bilgileri ve `SYSTEM_PROMPT` ile birleştirilerek Google Gemini için zenginleştirilmiş bir bağlam (`augmented_content`) oluşturulur.
6.  **Yanıt Üretimi (Generation):** Gemini, bu zenginleştirilmiş bağlamı analiz eder. Bir "tahmin" yapmak yerine, elindeki *gerçek* verilere dayanarak kullanıcıya mantıklı bir FPS aralığı ve performans analizi sunar.
7.  **Verimlilik:** Steam API'sinden gelen yanıtlar `st.cache_data`, Gemini bağlantısı ise `st.cache_resource` ile önbelleğe alınarak performans optimize edilir.

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu Klonlama

```bash
git clone [https://github.com/caganirmakii/SteamBot.git](https://github.com/caganirmakii/SteamBot.git)
cd SteamBot
````

### 2\. Gerekli Kütüphaneler

Proje için gerekli Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt
```

### 3\. API Anahtarlarını Ayarlama

Proje ana dizininde `.env` adında bir dosya oluşturun ve içine [Google AI Studio](https://aistudio.google.com/app/apikey) üzerinden aldığınız API anahtarınızı ekleyin.

```
GOOGLE_API_KEY="AIzaSy...SİZİN-API-ANAHTARINIZ"
GEMINI_MODEL="gemini-2.0-flash"
```

### 4\. Uygulamayı Başlatma

Streamlit uygulamasını yerel makinenizde başlatmak için:

```bash
streamlit run app.py
```

## 🎯 Örnek Kullanım

Bot açıldığında, aşağıdaki formata benzer bir soru sorabilirsiniz:

> "Selam, sistemim Ryzen 7 5800X, ekran kartım RTX 4070 ve 32GB RAM var. Sence bu oyunu 1080p'de kaç FPS alırım? https://store.steampowered.com/app/1086940/Baldurs\_Gate\_3/"

```
```
