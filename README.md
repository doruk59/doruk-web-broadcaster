# 📺 Doruk Web Broadcasting

Raspberry Pi 5 için otomatik YouTube canlı yayın sistemi.

## 🚀 Hızlı Kurulum

```bash
curl -sSL https://raw.githubusercontent.com/doruk59/doruk-web-broadcaster/main/scripts/install.sh | bash
```

## 📋 Özellikler

### Ana Özellikler
- ⏱️ Otomatik yayın başlatma (2 dakika geri sayım)
- 📝 Gelişmiş playlist yönetimi
- 🌐 Web tabanlı kontrol paneli
- 📊 Sistem monitörü
- 📅 Planlı yayın desteği

### Playlist Yönetimi
- 🎬 Video ekleme/silme/düzenleme
- 🔄 Döngüsel/tek sefer/karışık oynatma
- 📋 Planlı yayın takvimi
- 💾 Yedekleme ve geri yükleme
- 🎥 Video ön izleme

### Web Panel
- 📊 Sistem durumu izleme (CPU, RAM, Sıcaklık)
- 🎥 Canlı yayın embed görüntüleme
- 📝 Playlist durumu takibi

## ⚙️ Sistem Gereksinimleri

- Raspberry Pi 5 (8GB RAM)
- Raspberry Pi OS 64-bit
- 64GB USB Bellek (KINGSTON)
- İnternet bağlantısı
- HDMI monitör (ilk kurulum için)

## 📦 Kurulum Öncesi Hazırlık

1. USB Bellek İçeriği:
   - `background.png` (Geri sayım arka planı)
   - `music.mp3` (Geri sayım müziği)
   - `logo.png` (Yayın logosu)
   - `001.mp4` - `010.mp4` (Yayın videoları)

2. Ağ Ayarları:
   - Statik IP: 192.168.1.49
   - Port: 5000

## 🛠️ Manuel Kurulum

1. Repository'yi klonlayın:
```bash
cd /home/doruk
git clone https://github.com/doruk59/doruk-web-broadcaster.git
```

2. Kurulum betiklerini çalıştırılabilir yapın:
```bash
cd doruk-web-broadcaster
chmod +x scripts/*.sh
```

3. Kurulumu başlatın:
```bash
./scripts/setup.sh
```

## 📚 Kullanım

1. Sistem başlatıldığında:
   - 2 dakikalık geri sayım başlar
   - Playlist yöneticisi ile yayın içeriğini düzenleyebilirsiniz
   - "Yayına Hemen Gir" ile beklemeden başlatabilirsiniz

2. Web Panel:
   - http://192.168.1.49:5000 adresinden erişilebilir
   - Sistem durumunu gösterir
   - Yayını embed olarak gösterir

3. Playlist Yönetimi:
   - Videolar eklenebilir/silinebilir
   - Planlı yayınlar ayarlanabilir
   - Yedekleme yapılabilir

## 🔧 Sorun Giderme

1. Yayın Başlamıyorsa:
```bash
sudo systemctl status geri_sayim.service
sudo journalctl -u geri_sayim.service
```

2. Web Panel Erişilemiyorsa:
```bash
sudo netstat -tulpn | grep 5000
sudo systemctl restart geri_sayim.service
```

3. USB Bellek Sorunları:
```bash
lsblk  # USB belleği kontrol et
sudo mount -a  # Yeniden bağla
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Destek

Sorunlar için [Issues](https://github.com/doruk59/doruk-web-broadcaster/issues) sayfasını kullanabilirsiniz.
