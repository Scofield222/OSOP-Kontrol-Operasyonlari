## 1) Başlat-Durdur-Yeniden Başlat işlemleri
- Başlatmak içinsudo systemctl start servis_adı
- Durdur demek içinsudo systemctl stop servis_adı
- Yeniden başlatmak içinsudo systemctl restart servis_adı

 ## 2) Etkinleştir-Devre dışı bırakma ayarları
 - Etkinleştirmek içinsudo systemctl enable servis_adı
 - Devre dışı bırakmak içinsudo systemctl disable servis_adı
 
 ## 3) Servis şablonu (Unit Files) görüntüleme ve düzenleme
 - Görüntülemek içinsystemctl cat servis_adı
 - Düzenlemek içinsudo systemctl edit servis_adı
 - Tamamını düzenlemek içinsudo systemctl edit --full servis_adı
