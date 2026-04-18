# MyMiniCloud: A Distributed Infrastructure Simulation

![Status](https://img.shields.io/badge/Status-Deployed-success?style=for-the-badge)
![Tech](https://img.shields.io/badge/Infrastructure-Docker--Compose-blue?style=for-the-badge&logo=docker)
![Cloud](https://img.shields.io/badge/Cloud-AWS--EC2-orange?style=for-the-badge&logo=amazon-aws)

**MyMiniCloud** là một dự án mô phỏng hệ thống hạ tầng điện toán đám mây thu nhỏ, được thiết kế và triển khai bởi **Minh & Khang**. Hệ thống bao gồm 10 dịch vụ (microservices) được đóng gói bằng Docker, tích hợp đầy đủ các tính năng của một nền tảng Cloud hiện đại: Xác thực (SSO), Giám sát (Monitoring), Cân bằng tải (Load Balancing) và Lưu trữ đối tượng (Object Storage).

---

## Kiến trúc Hệ thống (System Architecture)

Hệ thống được vận hành bởi 10 máy chủ (containers) phối hợp nhịp nhàng:

1.  **API Gateway (Nginx Proxy):** Cửa ngõ duy nhất tiếp nhận request, cân bằng tải và bảo mật hệ thống.
2.  **Identity Management (Keycloak):** Quản lý định danh và truy cập tập trung (Single Sign-On).
3.  **Web Frontend Server:** Giao diện điều khiển (Dashboard) hiện đại, trực quan.
4.  **Application Backend:** Xử lý logic nghiệp vụ, quản lý dữ liệu sinh viên.
5.  **Relational Database (MariaDB):** Lưu trữ dữ liệu có cấu trúc một cách an toàn.
6.  **Object Storage (MinIO):** Lưu trữ tệp tin và dữ liệu phi cấu trúc (S3 compatible).
7.  **Internal DNS Server (Bind9):** Điều phối tên miền nội bộ giữa các dịch vụ.
8.  **Monitoring (Prometheus):** Thu thập các chỉ số (metrics) hệ thống theo thời gian thực.
9.  **Visualization (Grafana):** Hệ thống Dashboard biểu diễn dữ liệu giám sát trực quan.
10. **Mail Server (FakeSMTP):** Mô phỏng dịch vụ gửi email thông báo.

---

## Tính năng nổi bật

- **Cloud Native:** Triển khai hoàn toàn trên nền tảng Containerization, sẵn sàng mở rộng.
- **Full-Stack Monitoring:** Theo dõi sức khỏe hệ thống (CPU, RAM, Network) qua Grafana Dashboard.
- **Enterprise Security:** Tích hợp Keycloak giúp bảo vệ API và dữ liệu người dùng.
- **High Availability (Simulation):** Cấu hình Load Balancing qua Nginx để phân phối tải hiệu quả.
- **One-Click Deploy:** Tự động hóa quá trình cài đặt trên AWS EC2 thông qua Script.

---

## Hướng dẫn Triển khai (Deployment Guide)

### 1. Chạy cục bộ (Local Environment)
Yêu cầu: Đã cài đặt Docker và Docker Compose.

```bash
# Clone dự án
git clone -b minh-test https://github.com/MashuuMash/MinhKhangMiniCloud.git project
cd project

# Khởi chạy hệ thống
export PUBLIC_IP=localhost
docker compose up -d
```

### 2. Triển khai trên AWS EC2 (Cloud Deployment)
Hệ thống đã được tối ưu hóa cho môi trường AWS:

1.  **Khởi tạo Instance:** Sử dụng Ubuntu 22.04 LTS hoặc 24.04 LTS.
2.  **Cấu hình Security Group:** Mở các cổng 22, 80, 8081, 8085, 9000-9001, 3000, 9090.
3.  **Sử dụng Script Tự động:** Copy nội dung setup-cloud.sh vào phần User Data khi Launch máy ảo.

**Lưu ý khi khởi động lại máy AWS:**
Do IP Public của AWS thay đổi mỗi khi khởi động, bạn cần cập nhật biến môi trường:
```bash
sudo PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4) docker-compose up -d
```

---

## Công nghệ sử dụng (Tech Stack)

- **Infrastructure:** Docker, Docker Compose, Nginx.
- **Backend:** Python (Flask), SQLAlchemy.
- **Frontend:** HTML5, CSS3 (Emerald Green UI), JavaScript.
- **Database:** MariaDB.
- **DevOps:** Prometheus, Grafana, Keycloak, MinIO, Bind9.
- **Cloud:** AWS (EC2).

---

## Thành viên thực hiện (Contributors)

| Thành viên | Vai trò |
| :--- | :--- |
| **Khang** | Hạ tầng Cloud, Docker, Security (Keycloak) |
| **Minh** | Backend Development, Monitoring (Prometheus/Grafana) |

---

## Tài liệu Tham khảo & Bản quyền
*Dự án được xây dựng cho mục tiêu học tập trong khuôn khổ môn học Điện toán đám mây.*

Copyright © 2026 Minh & Khang. All rights reserved.