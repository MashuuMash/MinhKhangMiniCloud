# MyMiniCloud: Distributed Infrastructure Simulation

**MyMiniCloud** là một dự án mô phỏng hạ tầng điện toán đám mây (Cloud Infrastructure) được triển khai trên nền tảng Containerization. Hệ thống bao gồm 9 dịch vụ phối hợp đồng bộ, mô phỏng đầy đủ các thành phần cốt lõi của một hệ thống Cloud hiện đại như Load Balancing, Identity Management (SSO), Object Storage (S3), Internal DNS và hệ thống Observability toàn diện.

---

## 1. Kiến trúc Hệ thống (System Architecture)

Hệ thống được thiết kế theo cấu trục phân tầng nhằm đảm bảo tính sẵn sàng cao (High Availability) và bảo mật dữ liệu:

- **Tầng Gateway:** Nginx đóng vai trò Reverse Proxy và API Gateway, tiếp nhận và điều phối mọi luồng truy cập từ bên ngoài.
- **Cụm Frontend:** Gồm 3 Node Web Server (Node gốc, Node 1, Node 2) được cấu hình cân bằng tải để chia sẻ lưu lượng truy cập.
- **Tầng Dịch vụ:** 
    - Application Backend (Flask): Xử lý các logic nghiệp vụ và cung cấp RESTful API.
    - Identity Server (Keycloak): Quản lý định danh tập trung và thực hiện xác thực theo chuẩn OIDC.
- **Tầng Dữ liệu và Lưu trữ:**
    - Relational Database (MariaDB): Lưu trữ dữ liệu sinh viên có cấu trúc.
    - Object Storage (MinIO): Cung cấp dịch vụ lưu trữ tệp tin tương thích chuẩn S3.
- **Hạ tầng và Giám sát:**
    - Internal DNS (Bind9): Điều phối và ánh xạ tên miền nội bộ giữa các dịch vụ.
    - Prometheus & Grafana: Thu thập chỉ số hệ thống và hiển thị trực quan qua Dashboard giám sát.
    - Node Exporter: Thu thập các thông số phần cứng từ host và container.

---

## 2. Tính năng nổi bật và Các phần mở rộng đã thực hiện

- **Cân bằng tải High Availability:** Sử dụng Nginx với thuật toán Round Robin để phân phối tải qua cụm 3 server frontend.
- **Xác thực tập trung (SSO):** Triển khai Realm riêng trên Keycloak để quản lý người dùng và cấp phát Token JWT.
- **Tích hợp API và Database:** Backend hỗ trợ trả dữ liệu từ cả tệp JSON và truy vấn trực tiếp từ MariaDB.
- **Lưu trữ đối tượng (S3 Storage):** Cấu hình các Bucket chuyên dụng (profile-pics, documents) để quản lý tài nguyên tĩnh.
- **Định danh dịch vụ (Service Discovery):** Sử dụng hệ thống DNS nội bộ để các dịch vụ giao tiếp qua tên miền .cloud.local thay vì IP.
- **Giám sát hệ thống (Observability):** Dashboard Grafana tùy chỉnh để theo dõi các chỉ số CPU, RAM và Traffic mạng theo thời gian thực.

---

## 3. Công nghệ sử dụng (Tech Stack)

- **Cân bằng tải:** Nginx.
- **Backend:** Python (Flask).
- **Cơ sở dữ liệu:** MariaDB.
- **Bảo mật:** Keycloak.
- **Lưu trữ:** MinIO.
- **Hạ tầng mạng:** Bind9 DNS.
- **Giám sát:** Prometheus, Grafana, Node Exporter.
- **Nền tảng triển khai:** Docker, Docker Compose, AWS EC2.

---

## 4. Hướng dẫn Triển khai (Deployment Guide)

### Yêu cầu hệ thống
- Docker và Docker Compose v2 trở lên.
- Cấu hình Security Group trên máy chủ (mở các cổng: 80, 8081, 8085, 9000-9001, 3000, 9090).

### Các bước khởi chạy
1. Truy cập vào thư mục gốc của dự án.
2. Thiết lập biến môi trường IP Public (thay đại diện x.x.x.x bằng IP máy chủ của bạn):
   `export PUBLIC_IP=x.x.x.x`
3. Khởi chạy toàn bộ hệ thống bằng Docker Compose:
   `sudo docker compose up -d`
4. Kiểm tra trạng thái các container:
   `sudo docker compose ps`

---

## 5. Thành viên thực hiện (Contributors)

**Nhóm thực hiện: Khang & Minh**
- **Phạm Nguyễn Duy Khang - 523H0039:** Thiết kế hạ tầng Cloud, Docker Orchestration, Security (Keycloak), DNS.
- **Trần Vũ Nhật Minh - 523H0055:** Phát triển Backend API, Monitoring (Prometheus/Grafana), Web Frontend UI.
