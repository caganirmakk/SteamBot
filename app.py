# Gerekli kütüphaneleri içe aktarıyoruz
import os
import re
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai  

# -------------------------------------------------------
# .env dosyasındaki ortam değişkenlerini yüklüyorum.
# -------------------------------------------------------
load_dotenv()

#Google API anahtarı ve Gemini modelini kullanıyorum
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
# 'gemini-1.5-flash' kullanıyoruz.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash") 

# Sisteme verceğim promptu yazıyorum.
SYSTEM_PROMPT = (
""" Sen bir oyun performans asistanısın. Genel kurallar:
Her zaman nazik, kibar ve kısa-öz cevaplar ver.
Uydurma yapma. Emin olmadığın verileri açıkça “varsayım” olarak belirt.
Önce kullanıcıyla normal sohbet isterse kısa ve doğal cevap ver; bu durumda oyunla ilgili sorular sorma.
Veri Kaynağın ve Görevin (Çok Önemli!):
1.  Senin (Gemini) Steam API'sine veya internete doğrudan erişimin YOKTUR. Web kazıma (web scraping) yapamazsın.
2.  Kullanıcı bir Steam App ID veya URL'i mesajına eklediğinde, seni çalıştıran uygulama (kod), o oyunun güncel minimum ve önerilen sistem gereksinimlerini Steam API'sinden çeker.
3.  Bu resmi veriler, sana "--- ANALİZ İÇİN EK BİLGİ (Steam API'den Alındı): ---" başlığı altında, kullanıcının mesajıyla birlikte sunulacaktır.
4.  Senin görevin, tahmin yaparken KESİNLİKLE bu sana sunulan "ANALİZ İÇİN EK BİLGİ" bloğundaki verileri kullanmaktır. Bu veriler senin birincil gerçeğindir.
5.  Eğer sana bu "ANALİZ İÇİN EK BİLGİ" bloğu sunulmadıysa (kullanıcı henüz oyun linki/ID'si vermediyse), tahmin yapma ve eksik bilgileri (özellikle oyunun Steam linkini) iste.
Bilgi Toplama (mutlaka alınması gerekenler):
FPS tahmini yapmadan önce KESİNLİKLE şu dört bilgiyi al:
1. CPU (tam model adı, ör. "Intel i7-9700K")
2. GPU (tam model adı, ör. "RTX 3070")
3. RAM (GB cinsinden, ör. "16 GB")
4. Oyun (Kullanıcıdan Steam App ID veya Steam mağaza URL'i isteyerek. Bu bilgi gelince kod sana "ANALİZ İÇİN EK BİLGİ" bloğunu sağlayacak.)
Eğer bu bilgiler eksikse tahmin yapma. Eksik bilgileri nazikçe sırayla sor.
Tahmin Mantığı ve Çıktı Formatı:
1.  Öncelikle kaç FPS alacağını tek satırda söyle (örneğin: "Tahmini: 45–60 FPS (1080p, Medium)").
2.  Kısa analiz: Sana sunulan Steam verilerine dayanarak hangi bileşenin sınırlayıcı olduğunu (bottleneck) ve çözünürlük/ayarlara göre nasıl değişeceğini 1-3 cümlede açıkla.
3.  Varsayımlar: Tahmini hangi varsayımlara dayandırdığını kısa maddeler halinde yaz (ör. sürücü güncel, ray tracing kapalı).
4.  Güven puanı: Tahmine ilişkin basit bir güven seviyesi ver (Yüksek/Orta/Düşük) ve nedenini tek cümlede belirt (örn: "Güven: Yüksek - Çünkü Steam'den alınan resmi verilere göre analiz yapıyorum.").
5.  Öneri (opsiyonel): Eğer performans düşükse pratik öneriler sun.
Format Örneği (asistanın çıktı şablonu):
Tahmini: <numara veya aralık> FPS (çözünürlük, grafik ön ayarı)
Kısa analiz: <1–3 cümle, Steam verilerine göre>
Varsayımlar: - <madde>
Güven: <Yüksek/Orta/Düşük> — <kısa neden>
Öneri: - <1–2 kısa öneri> (isteğe bağlı detay)
"""
)

# -------------------------------------------------------
# YENİ: Google Gemini Yapılandırması ve Client
# -------------------------------------------------------
@st.cache_resource
def configure_gemini():
    """
    Google Gemini API'sini yapılandırır.
    """
    if not GEMINI_API_KEY:
        st.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanıza ekleyin.")
        st.stop()
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"Google Gemini yapılandırılamadı: {e}")
        st.stop()

def gemini_generate_reply(history):
    """
    Gemini modelini kullanarak sohbet geçmişine dayalı bir yanıt üretir.
    Streamlit'in session_state formatını Gemini'nin beklediği formata dönüştürür.
    """
    # Streamlit'in 'st.session_state' içinde tutmuş olduğu mesaj geçmişini Google apisinin kabul etmiş olduğu formata dönüştürüyoruz.
    gemini_history = []
    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    
    # Son mesajı geçmişten çıkarıyoruz çünkü onu ayrıca göndereceğiz.
    last_message = gemini_history.pop()
    
    try:
        # Modeli sistem talimatıyla başlatıyoruz.
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
        
        # Sohbeti geçmişle başlatıp yeni mesajı gönderiyoruz.
        chat_session = model.start_chat(history=gemini_history) # mesaj geçmişiyle birlikte gönderilir.
        response = chat_session.send_message(last_message["parts"]) # Son mesajı geçmişten çıkartmıştık onu burada ayrıca gönderiyoruz.
        
        return response.text
        
    except Exception as e:
        st.error(f"Gemini API hatası: {e}")
        return "Üzgünüm, bir hata oluştu ve yanıt üretemedim."


# -------------------------------------------------------
# Steam Gereksinimleri Yardımcıları
# -------------------------------------------------------
@st.cache_data(ttl=3600) # Steam verisini 1 saatliğine önbelleğe al
def fetch_steam_requirements(app_id: str) -> dict:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=us&l=en"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        node = data.get(str(app_id), {})
        if node.get("success") and "data" in node:
            return node["data"].get("pc_requirements", {}) or {}
    except Exception as e:
        st.error(f"Steam API hatası: {e}")
    return {}

def parse_requirements(html_text: str) -> str:
    if not html_text:
        return ""
    # BeautifulSoup kullanarak HTML'i temiz metne dönüştür
    soup = BeautifulSoup(html_text, "html.parser")
    # Daha temiz bir çıktı için listeleri ve paragrafları düzgünce ayır
    text = soup.get_text(separator="\n").strip()
    # Birden fazla boş satırı tek satıra indir
    return re.sub(r'\n\s*\n', '\n', text)


def extract_app_id(text: str):
    if not text:
        return None
    s = text.strip()
    if s.isdigit():
        return s
    # Steam URL'lerinden App ID'yi bulan regex
    m = re.search(r"/app/(\d+)", s)
    return m.group(1) if m else None

# -------------------------------------------------------
# Streamlit Uygulaması (Ana Mantık)
# -------------------------------------------------------
def main():
    st.set_page_config(page_title="🎮 SteamBot", layout="centered")
    st.title("🤖 SteamBot")
    st.caption("Steam verisi ve Gemini AI ile FPS tahmini yapalım!") 

    
    configure_gemini() # geminiyi konuşmaya hazır hale getirdim.

    # Sohbeti direkt olarak başlatan bir chatbot tasarladım.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Selam! Hangi oyunun FPS analizini yapmamı istersin? (Steam URL'i veya App ID belirtebilirsin)"}
        ]

    # Sohbet geçmişini ekranda gösterir
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Kullanıcıdan yeni giriş al
    if user_input := st.chat_input("Mesajınızı yazın..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # YENİ: Steam Veri Çekme ve Zenginleştirme Mantığı
        steam_context_str = None
        app_id = extract_app_id(user_input)
        
        # Eğer kullanıcı mesajı bir App ID veya Steam URL'i içeriyorsa...
        if app_id:
            with st.spinner(f"Steam'den App ID {app_id} için gereksinimler alınıyor..."):
                reqs = fetch_steam_requirements(app_id)
                if reqs:
                    # Gelen HTML'i temiz metne dönüştür
                    min_reqs = parse_requirements(reqs.get("minimum", ""))
                    rec_reqs = parse_requirements(reqs.get("recommended", ""))
                    
                    if min_reqs or rec_reqs:
                        # Gemini'ye göndermek için bir "bağlam" metni oluştur
                        steam_context_str = f"""
                        ---
                        ANALİZ İÇİN EK BİLGİ (Steam API'den Alındı):
                        Oyun App ID: {app_id}
                        
                        Minimum Gereksinimler:
                        {min_reqs if min_reqs else 'Belirtilmemiş'}
                        
                        Önerilen Gereksinimler:
                        {rec_reqs if rec_reqs else 'Belirtilmemiş'}
                        ---
                        Lütfen FPS tahminini bu resmi verilere ve kullanıcının sistemine göre yap.
                        """
        
        # Gemini'ye göndereceğimiz sohbet geçmişini hazırlıyoruz
        history_for_gemini = list(st.session_state.messages)
        
        if steam_context_str:
            # Eğer Steam'den veri çektiysek, bu veriyi son kullanıcı mesajına ekliyoruz.
            # Böylece Gemini, kullanıcının sorusunu bu ek bağlamla birlikte analiz eder.
            last_user_message = history_for_gemini.pop()
            augmented_content = f"""
            {steam_context_str}
            
            ---
            Kullanıcının Orijinal Mesajı:
            {last_user_message['content']}
            """
            history_for_gemini.append({"role": "user", "content": augmented_content})
        

        # DEĞİŞTİ: Gemini'den yanıt al
        with st.chat_message("assistant"):
            spinner_text = f"Gemini düşünüyor... ({GEMINI_MODEL})"
            if app_id and steam_context_str:
                spinner_text = f"Steam verisi analiz ediliyor... ({GEMINI_MODEL})"
            
            with st.spinner(spinner_text):
                # Gemini'ye (potansiyel olarak zenginleştirilmiş) sohbet geçmişini gönder
                reply = gemini_generate_reply(history_for_gemini) 
            
            st.markdown(reply)
        
        # Gelen yanıtı sohbet geçmişinde kalır (Orijinal, zenginleştirilmemiş haliyle).
        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":

    main()
