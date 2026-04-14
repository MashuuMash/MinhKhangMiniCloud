#!/bin/bash

# 1. Cập nhật hệ thống, giải phóng cổng 80 và cài đặt Docker
sudo apt-get update -y
sudo systemctl stop apache2 || true
sudo systemctl disable apache2 || true
sudo apt-get install -y docker.io docker-compose git-all

# 2. Khởi động Docker service
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Lấy Public IP của máy EC2 hiện tại
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
export PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)

echo "Hệ thống đang triển khai tại Public IP: $PUBLIC_IP"

# 4. Tải mã nguồn từ GitHub
cd /home/ubuntu
git clone -b minh-test https://github.com/MashuuMash/MinhKhangMiniCloud.git project
cd project

# 5. Khởi chạy toàn bộ hệ thống bằng Docker Compose
sudo PUBLIC_IP=$PUBLIC_IP docker-compose up -d

echo "================================================================="
echo "TRIỂN KHAI THÀNH CÔNG!"
echo "Truy cập Web: http://$PUBLIC_IP"
echo "Truy cập Grafana: http://$PUBLIC_IP:3000"
echo "Truy cập Prometheus: http://$PUBLIC_IP:9090"
echo "================================================================="
