#!/bin/bash

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Doruk Web Broadcasting Kurulum Başlıyor...${NC}"

# Sistem güncellemesi
echo -e "${YELLOW}Sistem güncelleniyor...${NC}"
sudo apt-get update
sudo apt-get upgrade -y

# Gerekli paketlerin kontrolü ve kurulumu
PACKAGES=(
    "python3-pip"
    "python3-tk"
    "python3-pil"
    "python3-vlc"
    "ffmpeg"
    "vlc"
    "chromium-browser"
    "python3-psutil"
    "git"
)

for package in "${PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package "; then
        echo -e "${YELLOW}$package kuruluyor...${NC}"
        sudo apt-get install -y "$package"
    else
        echo -e "${GREEN}$package zaten kurulu${NC}"
    fi
done

# Python paketlerinin kontrolü ve kurulumu
PYTHON_PACKAGES=(
    "flask"
    "pillow"
    "python-vlc"
    "psutil"
    "tkcalendar"
)

for package in "${PYTHON_PACKAGES[@]}"; do
    if ! pip3 list | grep -q "^$package "; then
        echo -e "${YELLOW}Python paketi $package kuruluyor...${NC}"
        pip3 install "$package"
    else
        echo -e "${GREEN}Python paketi $package zaten kurulu${NC}"
    fi
done

# Dizin yapısının oluşturulması
echo -e "${YELLOW}Dizin yapısı oluşturuluyor...${NC}"
mkdir -p /home/doruk/doruk_web_broadcaster
mkdir -p /media/doruk/KINGSTON
mkdir -p playlists
mkdir -p playlist_backups

# Dosya izinlerinin ayarlanması
echo -e "${YELLOW}Dosya izinleri ayarlanıyor...${NC}"
chmod +x src/stream.sh
chmod +x scripts/setup.sh

# Systemd servislerinin kurulumu
echo -e "${YELLOW}Sistem servisleri kuruluyor...${NC}"
sudo cp services/geri_sayim.service /etc/systemd/system/
sudo cp services/playlist-watchdog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable geri_sayim.service
sudo systemctl enable playlist-watchdog.service

# USB bellek kontrolü
echo -e "${YELLOW}USB bellek kontrol ediliyor...${NC}"
if [ ! -d "/media/doruk/KINGSTON" ]; then
    echo -e "${RED}UYARI: USB bellek mount noktası bulunamadı!${NC}"
    echo -e "${YELLOW}USB bellek mount noktası oluşturuluyor...${NC}"
    sudo mkdir -p /media/doruk/KINGSTON
fi

# Ağ ayarları kontrolü
echo -e "${YELLOW}Ağ ayarları kontrol ediliyor...${NC}"
if ! ip addr show | grep -q "192.168.1.49"; then
    echo -e "${RED}UYARI: IP adresi ayarlanmamış!${NC}"
    echo -e "${YELLOW}IP adresi ayarlanıyor...${NC}"
    # DHCP yerine statik IP ayarı
    cat << EOF | sudo tee /etc/dhcpcd.conf
interface eth0
static ip_address=192.168.1.49/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8
EOF
fi

# Güvenlik duvarı ayarları
echo -e "${YELLOW}Güvenlik duvarı ayarlanıyor...${NC}"
sudo ufw allow 5000/tcp
sudo ufw --force enable

# Kurulum tamamlandı
echo -e "${GREEN}Kurulum tamamlandı!${NC}"
