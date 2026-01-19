## 1) Başlat-Durdur-Yeniden Başlat işlemleri
- Başlat demek için  ``sudo systemctl start servis_adı``
- Durdur demek için  ``sudo systemctl stop servis_adı``
- Yeniden başlatma için  ``sudo systemctl restart servis_adı``

 ## 2) Etkinleştir-Devre dışı bırakma ayarları
 - Etkin yapmak için  ``sudo systemctl enable servis_adı``
 - Devre dışı bırakmak için  ``sudo systemctl disable servis_adı``
 
 ## 3) Servis şablonu (Unit Files) görüntüleme ve düzenleme
 - Görüntüleme için  ``systemctl cat servis_adı``
 - Düzenlemek için sudo  ``systemctl edit servis_adı``
 - Tamamını düzenleme için  ``sudo systemctl edit --full servis_adı``
