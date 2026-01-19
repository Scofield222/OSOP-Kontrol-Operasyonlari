from flask import Flask, request, jsonify, render_template_string # pyright: ignore[reportMissingImports]
import subprocess
import os

app = Flask(__name__)

# --- SİSTEM KOMUTLARI (İŞİN MUTFAĞI) ---

def calistir(komut):
    """Sistem komutlarını güvenli bir şekilde çalıştırır."""
    try:
        # sudo ile komutu terminalde çalıştırıyoruz
        sonuc = subprocess.run(["sudo"] + komut, capture_output=True, text=True)
        if sonuc.returncode == 0:
            return True, sonuc.stdout if sonuc.stdout else "İşlem başarılı."
        else:
            return False, sonuc.stderr
    except Exception as e:
        return False, str(e)

# --- SAYFA ROTALARI (BAĞLANTILAR) ---

@app.route('/')
def ana_sayfa():
    return render_template_string(HTML_TASARIM)

@app.route('/islem', methods=['POST'])
def servis_islemi():
    # Başlat, Durdur, Restart, Enable, Disable işlemleri
    veri = request.json
    basari, mesaj = calistir(["systemctl", veri['islem'], veri['servis']])
    return jsonify({"basari": basari, "mesaj": mesaj})

@app.route('/dosya-oku/<servis>', methods=['GET'])
def dosya_oku(servis):
    # Servis dosyasının (unit file) yolunu bul ve içeriğini oku
    basari, yol = calistir(["systemctl", "show", "-p", "FragmentPath", servis])
    yol = yol.strip().replace("FragmentPath=", "")
    
    if yol and os.path.exists(yol):
        with open(yol, 'r') as f:
            return jsonify({"icerik": f.read(), "yol": yol})
    return jsonify({"hata": "Dosya bulunamadı."}), 404

@app.route('/dosya-kaydet', methods=['POST'])
def dosya_kaydet():
    # Düzenlenen içeriği dosyaya yazar
    veri = request.json
    yol = veri['yol']
    icerik = veri['icerik']
    
    try:
        # Geçici bir dosyaya yazıp sudo ile asıl yerine taşıyoruz (güvenli yöntem)
        with open("/tmp/gecici_servis", "w") as f:
            f.write(icerik)
        calistir(["mv", "/tmp/gecici_servis", yol])
        calistir(["systemctl", "daemon-reload"]) # Sistemi haberdar et
        return jsonify({"basari": True, "mesaj": "Kaydedildi ve sistem yenilendi!"})
    except Exception as e:
        return jsonify({"basari": False, "mesaj": str(e)})

# --- GÖRSEL TASARIM (ARAYÜZ) ---

HTML_TASARIM = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Servis Kontrol Paneli</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 20px; }
        .konteynir { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        input[type="text"] { width: 70%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        .buton-grubu { margin: 20px 0; display: flex; flex-wrap: wrap; gap: 10px; }
        button { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-baslat { background: #28a745; color: white; }
        .btn-durdur { background: #dc3545; color: white; }
        .btn-mavi { background: #007bff; color: white; }
        .btn-gri { background: #6c757d; color: white; }
        button:hover { opacity: 0.8; }
        textarea { width: 100%; height: 250px; margin-top: 15px; font-family: monospace; border: 1px solid #ccc; padding: 10px; background: #fafafa; }
        #log { margin-top: 20px; padding: 15px; background: #333; color: #0f0; border-radius: 5px; font-size: 14px; min-height: 40px; }
    </style>
</head>
<body>
    <div class="konteynir">
        <h1>⚙️ Servis Yöneticisi</h1>
        
        <p>Yönetmek istediğiniz servis adını yazın:</p>
        <input type="text" id="servisAdi" placeholder="Örn: nginx, docker, bluetooth">
        
        <div class="buton-grubu">
            <button class="btn-baslat" onclick="islemYap('start')">Başlat</button>
            <button class="btn-durdur" onclick="islemYap('stop')">Durdur</button>
            <button class="btn-mavi" onclick="islemYap('restart')">Yeniden Başlat</button>
            <button class="btn-gri" onclick="islemYap('enable')">Otomatik Başlat (Aç)</button>
            <button class="btn-gri" onclick="islemYap('disable')">Otomatik Başlat (Kapat)</button>
        </div>

        <hr>
        
        <h3>📝 Servis Şablonu (Unit File)</h3>
        <button class="btn-mavi" onclick="dosyaYukle()">Dosyayı Görüntüle / Düzenle</button>
        <textarea id="editor" placeholder="Servis içeriği burada görünecek..."></textarea>
        <input type="hidden" id="dosyaYolu">
        <button class="btn-baslat" style="margin-top:10px;" onclick="dosyaKaydet()">Değişiklikleri Kaydet</button>

        <div id="log">Sistem hazır.</div>
    </div>

    <script>
        function logYaz(mesaj) {
            document.getElementById('log').innerText = mesaj;
        }

        async function islemYap(tip) {
            const servis = document.getElementById('servisAdi').value;
            if(!servis) return alert("Servis adı boş olamaz!");
            
            logYaz("Komut gönderiliyor...");
            const cevap = await fetch('/islem', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({islem: tip, servis: servis})
            });
            const veri = await cevap.json();
            logYaz(veri.mesaj);
        }

        async function dosyaYukle() {
            const servis = document.getElementById('servisAdi').value;
            logYaz("Dosya okunuyor...");
            try {
                const cevap = await fetch('/dosya-oku/' + servis);
                const veri = await cevap.json();
                document.getElementById('editor').value = veri.icerik;
                document.getElementById('dosyaYolu').value = veri.yol;
                logYaz("Dosya yüklendi: " + veri.yol);
            } catch { logYaz("Hata: Servis dosyası bulunamadı."); }
        }

        async function dosyaKaydet() {
            const yol = document.getElementById('dosyaYolu').value;
            const icerik = document.getElementById('editor').value;
            if(!yol) return alert("Önce bir dosya yüklemelisiniz!");

            logYaz("Kaydediliyor...");
            const cevap = await fetch('/dosya-kaydet', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({yol: yol, icerik: icerik})
            });
            const veri = await cevap.json();
            logYaz(veri.mesaj);
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    # sudo ile çalıştırmayı unutmayın
    app.run(host='0.0.0.0', port=5000, debug=True)
  
