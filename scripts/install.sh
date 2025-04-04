#!/bin/bash

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Doruk Web Broadcasting Kurulum Başlıyor...${NC}"

# Repository'yi klonla
echo -e "${YELLOW}Repository indiriliyor...${NC}"
cd /home/doruk
git clone https://github.com/doruk59/doruk-web-broadcaster.git
cd doruk-web-broadcaster

# Kurulum betiğini çalıştırılabilir yap
chmod +x scripts/setup.sh

# Kurulum betiğini çalıştır
./scripts/setup.sh

# Kurulum tamamlandı
echo -e "${GREEN}Kurulum tamamlandı!${NC}"
echo -e "${YELLOW}Sistem yeniden başlatılacak...${NC}"
echo -e "${RED}5 saniye içinde Ctrl+C ile iptal edebilirsiniz.${NC}"
sleep 5
