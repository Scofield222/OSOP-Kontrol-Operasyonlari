## 1) Başlat-Durdur-Yeniden Başlat işlemleri
- Başlatmak için sudo systemctl start servis_adı
- Durdur demek için sudo systemctl stop servis_adı
- Yeniden başlatmak için sudo systemctl restart servis_adı

 ## 2) Etkinleştir-Devre dışı bırakma ayarları
 - Etkinleştirmek için sudo systemctl enable servis_adı
 - Devre dışı bırakmak için sudo systemctl disable servis_adı
 
 ## 3) Servis şablonu (Unit Files) görüntüleme ve düzenleme
 - Görüntülemek için systemctl cat servis_adı
 - Düzenlemek için sudo systemctl edit servis_adı
 - Tamamını düzenlemek için sudo systemctl edit --full servis_adı
 - 
