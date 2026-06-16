from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# AZURE PORTAL'DAN KOPYALADIĞIN BİLGİLERİ BURAYA YAPIŞTIR
ACCOUNT_ID = "44fbda0a-7e4e-4eb0-83e9-3bc63c98dc4e"
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJWZXJzaW9uIjoiMi4wLjAuMCIsIktleVZlcnNpb24iOiIxMzA5YTUxZDMwYzE0ODk2YjljNTUxOWQ2OWRmNDMxNiIsIkFjY291bnRJZCI6IjQ0ZmJkYTBhLTdlNGUtNGViMC04M2U5LTNiYzYzYzk4ZGM0ZSIsIkFjY291bnRUeXBlIjoiQXJtIiwiUGVybWlzc2lvbiI6IkNvbnRyaWJ1dG9yIiwiRXh0ZXJuYWxVc2VySWQiOiI0NTY0MUE5QTE0QjI0NEQzQkNDNkZGREU2RDgzMTZCNiIsIlVzZXJUeXBlIjoiTWljcm9zb2Z0Q29ycEFhZCIsIklzc3VlckxvY2F0aW9uIjoiZ2VybWFueXdlc3RjZW50cmFsIiwibmJmIjoxNzgxNjM5NDExLCJleHAiOjE3ODE2NDMzMTEsImlzcyI6Imh0dHBzOi8vYXBpLnZpZGVvaW5kZXhlci5haS8iLCJhdWQiOiJodHRwczovL2FwaS52aWRlb2luZGV4ZXIuYWkvIn0.ZzVV0iMK12vMFoWe5HtCYbi8LT8oDFdlXuiNI9w8aZnVkaKy_r2L6KgjXcvI6kg-PR6fytIhZvAUoz1038frDCw8NU0jsaT6P8f77QU-3vZk9mhNyD4aZSKlyuMDuspvFjde9vkxk_EjbSa8mj0z3wzDfd91f_EXPnX4elE6VEzPbVVtJtsGg_QjtmMGWWxc2TkZG9-vjnBq9FGfMavizlGNB3DCVPSsui1KVHcMKNvTRTwjs7WyDMC6ensGRvGBHtyLhTTBjf1REYfL8lBlZLhYrn-0x7a0_M-HoRWBrhIvw8QNsVJUNsQdiJ4jzI1RI37FrgEMMP78qcy8Te776g"
LOCATION = "germanywestcentral"  # Azure'u kurarken seçtiğin bölgeyi buraya yaz (örn: northeurope)

HTML_SAYFASI = """
<!DOCTYPE html>
<html>
<head>
    <title>Akıllı Video Analitiği</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="alert alert-primary text-center shadow-sm">
            <h2>🎥 Gerçek Zamanlı Azure Video Indexer API</h2>
            <p>Videonuzu yükleyin, asenkron bulut mimarisiyle gerçek yapay zeka analizini izleyin.</p>
        </div>
        <div class="card shadow p-4 mt-4 text-center">
            <form action="/analiz" method="post" enctype="multipart/form-data">
                <input type="file" name="video" class="form-control mb-3" accept="video/mp4" required>
                <button type="submit" class="btn btn-primary btn-lg">🚀 Azure Bulutuna Yükle</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def ana_sayfa():
    return render_template_string(HTML_SAYFASI)

@app.route('/analiz', methods=['POST'])
def analiz_yap():
    if 'video' not in request.files:
        return "Video bulunamadı!", 400
        
    video = request.files['video']
    
    # 1. Aşama: Videoyu GERÇEKTEN Azure sunucularına yüklüyoruz
    url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos?name=Proje6GercekTest&privacy=Private&accessToken={ACCESS_TOKEN}"
    
    # Videoyu multipart/form-data olarak Azure'a postalıyoruz
    response = requests.post(url, files={'file': (video.filename, video.stream, video.content_type)})
    
    if response.status_code != 200:
        return f"Yükleme sırasında Azure Hatası: {response.text}"
        
    # Azure'un bize verdiği Takip Numarasını (Video ID) alıyoruz
    video_id = response.json().get('id')
    
    return f"""
    <div style='text-align:center; margin-top:50px; font-family:sans-serif;'>
        <h2 style='color:green;'>✅ Video Azure Bulutuna Başarıyla Yüklendi!</h2>
        <p><b>Takip Numarası (Video ID):</b> {video_id}</p>
        <p>Yapay zeka şu an arka planda videonuzu kare kare inceliyor.</p>
        <br>
        <a href='/sonuc/{video_id}' style='padding:15px 30px; background:orange; color:white; text-decoration:none; border-radius:5px; font-size:18px;'>Analiz Durumunu Kontrol Et</a>
    </div>
    """

@app.route('/sonuc/<video_id>')
def sonuc_getir(video_id):
    # 2. Aşama: Azure'a "Bu ID'ye sahip videonun analizi bitti mi?" diye soruyoruz
    url = f"https://api.videoindexer.ai/{LOCATION}/Accounts/{ACCOUNT_ID}/Videos/{video_id}/Index?accessToken={ACCESS_TOKEN}"
    response = requests.get(url)
    data = response.json()
    
    state = data.get('state')
    
    # Video hala işleniyorsa hocayı ve kullanıcıyı bekletiyoruz
    if state == 'Processing' or state == 'Uploaded':
        return f"""
        <div style='text-align:center; margin-top:50px; font-family:sans-serif;'>
            <h2 style='color:blue;'>⏳ İşlem Devam Ediyor...</h2>
            <p>Azure yapay zekası çalışıyor. Sunucuyu yormamak için lütfen <b>30 saniye bekleyip</b> sayfayı yenileyin (F5).</p>
            <p>Mevcut Sistem Durumu: <b>{state}</b></p>
        </div>
        """
    
    # İşlem bittiyse gerçek JSON verisinden etiketleri ayrıştırıyoruz
    elif state == 'Processed':
        etiketler = []
        try:
            insights = data['videos'][0]['insights']
            if 'labels' in insights:
                for label in insights['labels']:
                    etiketler.append(label['name'])
        except:
            pass
            
        etiket_metni = ", ".join(etiketler) if etiketler else "Belirgin bir nesne bulunamadı."
        
        return f"""
        <div style='text-align:center; margin-top:50px; font-family:sans-serif;'>
            <h2 style='color:green;'>🎉 Gerçek Zamanlı Analiz Tamamlandı!</h2>
            <hr style='width:50%;'>
            <h3 style='color:darkblue;'>🤖 Videodan Çıkarılan Gerçek Veriler:</h3>
            <p style='font-size:18px;'><b>Tespit Edilen Etiketler / Nesneler / Kavramlar:</b></p>
            <p style='font-size:22px; color:darkred; max-width:800px; margin: 0 auto; line-height: 1.5;'>{etiket_metni}</p>
            <br><br>
            <a href='/' style='padding:10px 20px; background:blue; color:white; text-decoration:none; border-radius:5px;'>Yeni Video Yükle</a>
        </div>
        """
    else:
        return f"Beklenmeyen bir durum oluştu: {state}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)