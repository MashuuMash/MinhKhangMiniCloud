# 🏆 MASTER GUIDE: DEMO QUY TRÌNH NÂNG CAO - MYMINICLOUD

Tài liệu này ánh xạ 1:1 với kịch bản `demo.txt` của bạn, nhưng bổ sung chi tiết các **Hành động (Action)** và **Câu lệnh (Command)** để bạn thực hiện trực tiếp trước giảng viên.

---

## PHẦN 1: MỞ ĐẦU & GIỚI THIỆU HẠ TẦNG (12 CONTAINERS)

**Hành động:**
1. Mở Terminal EC2.
2. Dán lệnh sau để hiện bảng danh sách container chuyên nghiệp:
   ```bash
   sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
   ```

**Lời thoại:**
> "Kính chào thầy và các bạn. Em tên là Minh Khang, hôm nay em xin trình bày phần Demo báo cáo dự án cuối kỳ môn Điện toán đám mây. Đề tài của dự án là xây dựng hệ thống mô phỏng hạ tầng MyMiniCloud.
> 
> Như thầy có thể thấy trên màn hình Terminal, hệ thống của em không chỉ dừng lại ở 9 server cơ bản theo yêu cầu mà đã được em tối ưu và mở rộng lên quy mô **12 containers** hoạt động đồng bộ. Trong đó, em đã triển khai cụm 3 Node Web Frontend để đáp ứng bài toán High Availability, cùng với các dịch vụ bảo mật Keycloak, lưu trữ MinIO, DNS nội bộ và hệ thống giám sát Prometheus - Grafana."

---

## PHẦN 2: TÍNH NĂNG MỞ RỘNG - WEB & LOAD BALANCING

**Hành động:**
1. **Terminal 1:** Chạy lệnh xem log Gateway (Nginx):
   ```bash
   sudo docker logs -f --tail 0 api-gateway-proxy-server
   ```
2. **Terminal 2:** Chạy lệnh giả lập 20 lượt truy cập:
   ```bash
   for i in {1..20}; do curl -s http://localhost/ > /dev/null && echo "Request $i: OK"; done
   ```

**Lời thoại:**
> "Đến với phần tính năng mở rộng đầu tiên, em đã triển khai hệ thống nội dung tĩnh gồm các bài viết Blog cá nhân được phục vụ qua Nginx.
> 
> Tuy nhiên, điểm đặc biệt nhất nằm ở khả năng chịu tải. Em đã cấu hình Nginx sử dụng thuật toán **Round Robin**. Thầy hãy quan sát log của Gateway ở bên trái: khi em thực hiện tải liên tục, các yêu cầu truy cập được điều phối luân phiên qua 3 thực thể là `web-frontend-server`, `web-frontend-server1` và `web-frontend-server2`. Điều này mô phỏng chính xác cơ chế Elastic Load Balancing của AWS."

---

## PHẦN 3: TÍNH NĂNG MỞ RỘNG - BACKEND API & DATABASE NÂNG CAO

**Hành động:**
1. **Tab 1:** Truy cập: `http://<IP_CỦA_BẠN>/api/students-json` (Hiện bảng Web hoặc JSON thô).
2. **Tab 2:** Truy cập: `http://<IP_CỦA_BẠN>/api/students-db` (Hiện giao diện quản lý MariaDB).

**Lời thoại:**
> "Tiếp theo là phần mở rộng cho lớp ứng dụng và dữ liệu. Thay vì một API chào hỏi đơn giản, em đã xây dựng hệ thống API lấy dữ liệu sinh viên từ 2 nguồn: một là tập tin JSON tĩnh được lưu trữ nội bộ, và hai là truy vấn trực tiếp từ cơ sở dữ liệu `studentdb` mà em đã thiết kế riêng trong MariaDB. Điều này minh chứng cho khả năng xử lý logic phức tạp và kết nối cơ sở dữ liệu bền vững của Backend."

---

## PHẦN 4: TÍNH NĂNG MỞ RỘNG - IDENTITY & ACCESS MANAGEMENT (SSO)

**Hành động:**
1. Truy cập: `http://<IP_CỦA_BẠN>:8081` -> Click **Administration Console**.
2. Đăng nhập: `admin` / `admin`.
3. Chỉ vào Realm `realm_minicloud` (góc trên bên trái).
4. Menu trái chọn **Users** -> Click **View all users** để hiện `sv01`, `sv02`.

**Lời thoại:**
> "Về phần bảo mật, em đã cấu hình một Identity Provider chuyên nghiệp bằng Keycloak. Em đã tạo riêng một Realm là `realm_minicloud`, thiết lập Client `flask-app` và các tài khoản người dùng `sv01`, `sv02`. Hệ thống này cho phép bảo vệ các tài nguyên nhạy cảm của Cloud, chỉ cho phép người dùng có Token hợp lệ được phép truy cập."

---

## PHẦN 5: TÍNH NĂNG MỞ RỘNG - OBJECT STORAGE & INTERNAL DNS

**Hành động MinIO:**
1. Truy cập: `http://<IP_CỦA_BẠN>:9001` (User: `minioadmin` / PW: `minioadmin`).
2. Chọn **Buckets** -> Chỉ vào `profile-pics` và `documents`.

**Hành động DNS (Terminal):**
1. Chạy các lệnh kiểm tra tên miền nội bộ:
   ```bash
   dig @localhost -p 1053 app-backend.cloud.local +short
   dig @localhost -p 1053 minio.cloud.local +short
   ```

**Lời thoại:**
> "Trong một hạ tầng Cloud, quản lý tài nguyên và định danh dịch vụ là cực kỳ quan trọng. Em đã thiết lập MinIO để lưu trữ ảnh đại diện và hồ sơ sinh viên, tương tự như dịch vụ Amazon S3.
> 
> Bên cạnh đó, hệ thống DNS nội bộ Bind9 đã được em nâng cấp. Các container giờ đây có thể tự tìm thấy nhau thông qua các tên miền nội bộ chuyên biệt như `app-backend.cloud.local` thay vì phụ thuộc vào địa chỉ IP động."

---

## PHẦN 6: TÍNH NĂNG MỞ RỘNG - GIÁM SÁT TOÀN DIỆN (OBSERVABILITY)

**Hành động:**
1. Truy cập: `http://<IP_CỦA_BẠN>:3000` (User: `admin` / PW: `admin`).
2. Menu trái chọn **Dashboards** -> Mở Dashboard đã tạo.

**Lời thoại:**
> "Cuối cùng, để quản lý hạ tầng phức tạp này, em đã xây dựng Dashboard giám sát trên Grafana. Em cấu hình Prometheus để thu thập mã metric từ các Node Exporter và chính Web Server.
> 
> Như thầy thấy, Dashboard này cung cấp cái nhìn thời gian thực về hiệu năng CPU, RAM và băng thông mạng. Đây là công cụ đắc lực giúp quản trị viên đưa ra các quyết định mở rộng hệ thống kịp thời."

---

## PHẦN 7: KẾT LUẬN

**Hành động:** Quay lại màn hình Terminal có đủ 12 container đang chạy.

**Lời thoại:**
> "Tổng kết lại, dự án MyMiniCloud của em đã giải quyết thành công các bài toán cốt lõi từ tầng hạ tầng mạng đến tầng ứng dụng và bảo mật. Toàn bộ các yêu cầu mở rộng đều đã được triển khai và kiểm thử thành công trên môi trường AWS thực tế.
> 
> Em xin cảm ơn thầy đã chú ý theo dõi phần demo của em."

---

> [!IMPORTANT]
> **Lưu ý:** Trước khi demo, hãy đảm bảo bạn đã chạy `docker-compose up -d` và các container đều ở trạng thái `Up`.
