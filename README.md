Markdown

# 🤖 SteamBot: Dinamik FPS Performans Asistanı

Bu proje, **Google Gemini** modelini ve **Steam API**'sini kullanarak oyunlar için
gerçek zamanlı FPS tahmini yapan Streamlit tabanlı bir chatbot'tur.

## 📋 Proje Hakkında

Bu asistan, kullanıcıların sistem özelliklerini (CPU, GPU, RAM) ve oynamak
istedikleri oyunun Steam mağaza linkini alarak bir performans analizi sunar.

Projenin temel amacı, statik ve zamanla eskiyen veri setlerinin aksine,
**canlı ve güncel verilerle** beslenen bir RAG (Retrieval-Augmented Generation)
mimarisi kurmaktır.

Bu sayede, oyunların sistem gereksinimleri güncellendiği anda botun analizleri de
otomatik olarak güncellenmiş olur.

## 🛠️ Kullanılan Teknolojiler

* **Streamlit**: Web arayüzü ve kullanıcı etkileşimi.
* **Google Gemini (gemini-2.5-flash)**: Yanıt ve analiz üretimi (LLM).
* **Requests**: Steam API'sinden anlık veri çekmek için.
* **BeautifulSoup4**: Steam'den gelen HTML verisini temizlemek için.
* **Python-dotenv**: API anahtarlarını güvenli saklamak için.

## 💡 Veri Akışı ve Mimarisi (Nasıl Çalışır?)

Bu proje, **Steam API'sini dinamik bir veri seti** olarak kullanır. Statik bir
vektör veritabanı yerine, her sorguda "Anlık Veri Çekme" yöntemini uygular:

**1. Giriş (Input)**
Kullanıcı, sistem özelliklerini (CPU, GPU, RAM) ve oyunun Steam mağaza
URL'ini sohbete girer.

**2. Kimlik Çıkarımı (ID Extraction)**
`extract_app_id` fonksiyonu, verilen URL'i analiz eder ve oyunun benzersiz
Steam App ID'sini çıkarır.

**3. Dinamik Veri Çekme (Retrieval)**
`fetch_steam_requirements` fonksiyonu, bu App ID'yi kullanarak o an Steam'in
resmi API'sine bir `GET` isteği atar.

**4. Veri İşleme (Processing)**
API'den dönen JSON yanıtının içindeki HTML'li gereksinim metinleri,
`parse_requirements` ve `BeautifulSoup` ile temizlenir.

**5. Bağlam Zenginleştirme (Augmentation)**
Çekilen bu güncel ve resmi sistem gereksinimleri, kullanıcının sistem
bilgileriyle birleştirilerek Gemini için zengin bir bağlam oluşturulur.

**6. Yanıt Üretimi (Generation)**
Gemini, bu zenginleştirilmiş bağlamı analiz ederek kullanıcıya mantıklı bir FPS
aralığı ve performans analizi sunar.

**7. Verimlilik**
Steam API yanıtları `st.cache_data`, Gemini bağlantısı ise
`st.cache_resource` ile önbelleğe alınarak performans optimize edilir.

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu Klonlama

```bash
git clone [https://github.com/caganirmakii/SteamBot.git](https://github.com/caganirmakii/SteamBot.git)
cd SteamBot
2. Gerekli Kütüphaneler
Proje için gerekli Python kütüphanelerini yükleyin:

Bash

pip install -r requirements.txt
3. API Anahtarlarını Ayarlama
Proje ana dizininde .env adında bir dosya oluşturun ve içine Google AI Studio üzerinden aldığınız API anahtarınızı ekleyin.

GOOGLE_API_KEY="AIzaSy...SİZİN-API-ANAHTARINIZ"
GEMINI_MODEL="gemini-2.5-flash"
4. Uygulamayı Başlatma
Streamlit uygulamasını yerel makinenizde başlatmak için:

Bash

streamlit run app.py
🎯 Örnek Kullanım
Bot açıldığında, aşağıdaki formata benzer bir soru sorabilirsiniz:

"Selam, sistemim Ryzen 7 5800X, ekran kartım RTX 4070 ve 32GB RAM var." "Sence bu oyunu 1080p'de kaç FPS alırım?" "httpsA://https://www.google.com/search?q=store.steampowered.com/app/1086940/Baldurs_Gate_3/"
