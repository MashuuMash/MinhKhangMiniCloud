# 🏛️ Tổng hợp Hệ thống MyMiniCloud - Khang & Minh

Tài liệu này giúp các thành viên trong nhóm hiểu rõ kiến trúc, những gì đã làm và những gì cần hoàn thiện để đạt điểm tối đa (10 điểm).

---

## 1. Tổng quan hệ thống
Chúng ta đang xây dựng một **Hệ thống Cloud thu nhỏ (MyMiniCloud)**. Thay vì thuê server của AWS hay Google, chúng ta tự dựng 9 loại máy chủ khác nhau chạy trong các "hộp" riêng biệt (gọi là **Container**) bằng công nghệ **Docker**.

### Mạng nội bộ: `cloud-net`
Tất cả 9 server này được cắm chung vào một "switch ảo" tên là `cloud-net`. Chúng có thể gọi nhau bằng tên (ví dụ: `app` gọi `db`) thay vì dùng địa chỉ IP phức tạp.

---

## 2. Danh sách 9 Máy chủ (Servers)
| STT | Tên Server | Vai trò thực tế | Công nghệ sử dụng |
| :--- | :--- | :--- | :--- |
| 1 | **Web Frontend** | Nơi chứa trang web giao diện (HTML/CSS) | Nginx |
| 2 | **App Backend** | Nơi xử lý logic và API (xử lý dữ liệu) | Python (Flask) |
| 3 | **Database** | Nơi lưu trữ dữ liệu bền vững | MariaDB (SQL) |
| 4 | **Authentication** | Hệ thống đăng nhập, cấp quyền (IdP) | Keycloak |
| 5 | **Object Storage** | Lưu trữ file, ảnh (giống Amazon S3) | MinIO |
| 6 | **DNS Server** | Danh bạ nội bộ (biến tên miền thành IP) | Bind9 |
| 7 | **Monitoring** | Giám sát "sức khỏe" (CPU, RAM) các server | Prometheus |
| 8 | **Logging/Visual** | Vẽ biểu đồ giám sát đẹp mắt | Grafana |
| 9 | **Reverse Proxy** | Cổng bảo vệ, điều phối truy cập (Gateway) | Nginx |

---

## 3. Những gì đã thực hiện
*   **Cấu trúc thư mục:** Đã tạo đủ 9 thư mục cho 9 server.
*   **Hệ thống lõi:** Đã viết file `docker-compose.yml` để khởi động cả 10 container (9 server + 1 node-exporter) cùng lúc.
*   **Thông mạng:** Đã kiểm tra các server "thấy" nhau bằng lệnh `ping` (Kết quả đạt 100%).
*   **DNS & Gateway:** Đã cấu hình để server DNS nhận diện được các máy chủ và Gateway định tuyến đúng yêu cầu từ Web vào App.

## 5. Cách chạy hệ thống
Mọi thứ đều nằm trong file `docker-compose.yml`. Để khởi động, chỉ cần gõ 1 lệnh duy nhất tại thư mục gốc:
```powershell
docker compose up -d
```
Muốn xóa hết làm lại từ đầu (reset dữ liệu):
```powershell
docker compose down -v
```

---

**Ghi chú:** Đừng ngần ngại hỏi Antigravity (AI) bất cứ khi nào bạn gặp lỗi hoặc không hiểu dòng code nào. Chúng ta đang làm một hệ thống Cloud thực thụ! 🚀
