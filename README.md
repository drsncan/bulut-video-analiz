# 🎥 Bulut Bilişim Proje 6: Bulut Tabanlı Yapay Zeka ile Asenkron Video Analitiği

Bu proje, Ankara Üniversitesi Bilgisayar Mühendisliği bölümü "Bulut Bilişim" dersi final değerlendirmesi kapsamında geliştirilmiştir. Projenin temel amacı, bulut tabanlı Bilişsel Servislerin (Cognitive Services) harici bir web uygulamasına API tabanlı entegrasyonunu sağlamak ve asenkron (eşzamansız) büyük veri işleme süreçlerini tecrübe etmektir.

## 🎥 Proje Sunumu ve Canlı Demo

Azure Video Indexer API'sinin Python arka ucu ile nasıl haberleştiğini, videonun buluta asenkron olarak fırlatılıp Takip Numarası (Video ID) alınmasını ve yapay zekanın (nesne, kavram ve etiket) analiz sonuçlarını gerçek zamanlı olarak arayüze nasıl yansıttığını aşağıdaki bağlantıdan izleyebilirsiniz:

[![Proje 6 Demo Videosu](https://img.youtube.com/vi/ZzrPCuEuffE/hqdefault.jpg)](https://youtu.be/ZzrPCuEuffE)

**[👉 Canlı Demo ve Sistem Analizi Videosunu İzlemek İçin Tıklayın](https://youtu.be/ZzrPCuEuffE)**

---

## 🚀 Proje Özeti ve Mimari Kararlar

Büyük boyutlu multimedya dosyalarının yapay zeka tarafından işlenmesi zaman alan bir operasyon olduğundan, sunucuyu ve kullanıcı tarayıcısını kilitlememek adına mimari tamamen **asenkron (asynchronous)** olarak tasarlanmıştır.

Sistem üzerinde uygulanan yapılandırmalar:
* **Arka Uç (Backend):** Python ve Flask Framework
* **Bilişsel Servis:** Azure Video Indexer (Bölge: `germanywestcentral`)
* **Depolama Katmanı:** Azure StorageV2 (Blob Storage)
* **Kimlik Yönetimi ve Güvenlik:** Mimari içerisinde güvenlik açığı yaratmamak adına statik API şifreleri yerine kısa ömürlü (1 saat) **Access Token** kullanılmıştır. Ayrıca Video Indexer ile Storage hesapları arasında güvenli veri transferi için **Managed Identity (Yönetilen Kimlik)** altyapısı kurularak *Storage Blob Data Contributor* rol ataması yapılmıştır.

## ⚙️ Asenkron İş Akışı (Workflow)

Sistem mimarisi 3 ana aşamadan oluşmaktadır:

1. **Yükleme (POST İşlemi):** Kullanıcı arayüzünden seçilen video, Azure sunucularına iletilir. Sistem videoyu kuyruğa alır ve anında bize benzersiz bir **Video ID** döndürür.
2. **Durum Sorgulama (Polling):** Arayüzümüz, video işlenirken arka planda Azure'a düzenli `GET` istekleri atarak işlemin durumunu (`Processing` / `Uploaded`) denetler.
3. **İçgörü Ayrıştırma (JSON Parsing):** İşlem `Processed` (Tamamlandı) durumuna geçtiği an, Azure'dan dönen devasa JSON dosyası içindeki `labels` ve `insights` (örn: *headphones, computer, indoor*) dizileri ayrıştırılarak kullanıcı arayüzünde şık bir şekilde görselleştirilir.

