import mysql.connector
from flask import Flask, jsonify, request, render_template_string, redirect, url_for
import time, requests, os, json
from jose import jwt

# Database credentials
DB_CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'relational-database-server',
    'database': 'studentdb'
}

# Các biến môi trường cho Auth Server (Keycloak)
ISSUER   = os.getenv("OIDC_ISSUER",   "http://localhost:8081/realms/realm_minicloud")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "account")
JWKS_URL = os.getenv("OIDC_JWKS_URL", "http://authentication-identity-server:8080/realms/realm_minicloud/protocol/openid-connect/certs")

_JWKS = None; _TS = 0
def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        try:
            _JWKS = requests.get(JWKS_URL, timeout=5).json()
            _TS = now
        except:
            return {}
    return _JWKS

app = Flask(__name__)

# CSS Chung cho các trang Dashboard
COMMON_STYLE = """
<style>
    :root {
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --primary: #10b981;
        --primary-hover: #059669;
        --danger: #ef4444;
        --text-main: #f8fafc;
        --text-secondary: #94a3b8;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
    body {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: var(--text-main);
        padding: 40px 20px;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .container {
        width: 100%;
        max-width: 1100px;
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 40px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 20px;
    }
    .header h1 { font-size: 2rem; color: var(--primary); font-weight: 800; letter-spacing: -0.025em; }
    
    /* Form Styles */
    .form-box {
        background: rgba(255, 255, 255, 0.03);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 30px;
        border: 1px dashed rgba(16, 185, 129, 0.3);
    }
    .form-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
    }
    input {
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 15px;
        border-radius: 8px;
        color: white;
        font-size: 0.9rem;
    }
    input:focus { outline: none; border-color: var(--primary); }
    .btn {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
        font-size: 0.9rem;
    }
    .btn-add { background: var(--primary); color: #000; }
    .btn-add:hover { background: var(--primary-hover); transform: translateY(-2px); }
    .btn-del { background: rgba(239, 68, 68, 0.1); color: var(--danger); border: 1px solid var(--danger); }
    .btn-del:hover { background: var(--danger); color: white; }
    .btn-edit { background: rgba(16, 185, 129, 0.1); color: var(--primary); border: 1px solid var(--primary); margin-right: 5px; }
    .btn-edit:hover { background: var(--primary); color: white; }

    /* Modal Styles */
    .modal {
        display: none;
        position: fixed;
        z-index: 2000;
        left: 0; top: 0; width: 100%; height: 100%;
        background-color: rgba(0,0,0,0.8);
        backdrop-filter: blur(5px);
    }
    .modal-content {
        background: var(--bg-color);
        margin: 10% auto;
        padding: 40px;
        border: 1px solid var(--primary);
        border-radius: 20px;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
    }
    .modal-header { margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; }
    .modal-header h2 { color: var(--primary); }
    .modal-body .form-grid { grid-template-columns: 1fr; gap: 20px; }
    .modal-footer { margin-top: 30px; display: flex; justify-content: flex-end; gap: 10px; }

    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { text-align: left; padding: 15px; color: var(--text-secondary); font-size: 0.85rem; text-transform: uppercase; }
    td { padding: 20px 15px; border-top: 1px solid rgba(255, 255, 255, 0.05); }
    .gpa-badge { background: var(--primary); color: #000; padding: 4px 10px; border-radius: 6px; font-weight: 700; }
</style>
"""

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.get("/hello")
def hello(): 
    return jsonify(message="Hello from App Server!", members=["Khang", "Minh"])

@app.route("/student", strict_slashes=False)
@app.route("/api/student", strict_slashes=False)
def get_students():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route cho MariaDB CRUD
@app.route("/api/students-db", methods=["GET"], strict_slashes=False)
def students_db_page():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        html_template = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8"><title>MariaDB CRUD - MyMiniCloud</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
            """ + COMMON_STYLE + """
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Quản lý Sinh viên (MariaDB)</h1>
                    <a href="/" style="color: var(--text-secondary); text-decoration: none;">← Quay lại</a>
                </div>

                <div class="form-box">
                    <form action="/api/students-db/add" method="POST" class="form-grid">
                        <input type="text" name="student_id" placeholder="MSSV" required>
                        <input type="text" name="full_name" placeholder="Họ và tên" required>
                        <input type="text" name="major" placeholder="Chuyên ngành" required>
                        <input type="number" step="0.01" name="gpa" placeholder="GPA" required>
                        <button type="submit" class="btn btn-add">Thêm sinh viên</button>
                    </form>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Mã SV</th><th>Họ và tên</th><th>Chuyên ngành</th><th>GPA</th><th>Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in students %}
                        <tr>
                            <td style="font-family: monospace; color: var(--primary); font-weight: 600;">{{ s.student_id }}</td>
                            <td>{{ s.full_name }}</td>
                            <td>{{ s.major }}</td>
                            <td><span class="gpa-badge">{{ s.gpa }}</span></td>
                            <td style="display: flex;">
                                <button class="btn btn-edit" onclick="openEditModal('{{ s.id }}', '{{ s.student_id }}', '{{ s.full_name }}', '{{ s.major }}', '{{ s.gpa }}')">Sửa</button>
                                <form action="/api/students-db/delete/{{ s.id }}" method="POST">
                                    <button type="submit" class="btn btn-del" onclick="return confirm('Bạn có chắc muốn xóa?')">Xóa</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <!-- Edit Modal -->
            <div id="editModal" class="modal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>Chỉnh sửa thông tin</h2>
                    </div>
                    <form id="editForm" method="POST">
                        <div class="modal-body">
                            <div class="form-grid">
                                <input type="text" id="edit-student-id" name="student_id" placeholder="MSSV" required>
                                <input type="text" id="edit-full-name" name="full_name" placeholder="Họ và tên" required>
                                <input type="text" id="edit-major" name="major" placeholder="Chuyên ngành" required>
                                <input type="number" step="0.01" id="edit-gpa" name="gpa" placeholder="GPA" required>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-del" onclick="closeEditModal()">Hủy</button>
                            <button type="submit" class="btn btn-add">Lưu thay đổi</button>
                        </div>
                    </form>
                </div>
            </div>

            <script>
                function openEditModal(id, stuid, name, major, gpa) {
                    document.getElementById('editForm').action = '/api/students-db/update/' + id;
                    document.getElementById('edit-student-id').value = stuid;
                    document.getElementById('edit-full-name').value = name;
                    document.getElementById('edit-major').value = major;
                    document.getElementById('edit-gpa').value = gpa;
                    document.getElementById('editModal').style.display = 'block';
                }
                function closeEditModal() {
                    document.getElementById('editModal').style.display = 'none';
                }
                window.onclick = function(event) {
                    if (event.target == document.getElementById('editModal')) closeEditModal();
                }
            </script>
        </body>
        </html>
        """
        return render_template_string(html_template, students=students)
    except Exception as e:
        return f"<h1 style='color:red'>Lỗi DB: {str(e)}</h1>", 500

@app.post("/api/students-db/add")
def add_student_db():
    try:
        data = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO students (student_id, full_name, major, gpa) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (data['student_id'], data['full_name'], data['major'], data['gpa']))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/api/students-db")
    except Exception as e:
        return f"Lỗi khi thêm: {str(e)}", 500

@app.post("/api/students-db/update/<int:id>")
def update_student_db(id):
    try:
        data = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE students SET student_id=%s, full_name=%s, major=%s, gpa=%s WHERE id=%s"
        cursor.execute(query, (data['student_id'], data['full_name'], data['major'], data['gpa'], id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/api/students-db")
    except Exception as e:
        return f"Lỗi khi cập nhật: {str(e)}", 500

@app.post("/api/students-db/delete/<int:id>")
def delete_student_db(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/api/students-db")
    except Exception as e:
        return f"Lỗi khi xóa: {str(e)}", 500

# Route cho JSON View
@app.get("/api/students-json", strict_slashes=False)
def students_json_page():
    try:
        with open("students.json", "r") as f:
            students = json.load(f)
        
        html_template = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8"><title>JSON View - MyMiniCloud</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
            """ + COMMON_STYLE + """
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Danh sách Sinh viên (Local JSON)</h1>
                    <a href="/" style="color: var(--text-secondary); text-decoration: none;">← Quay lại</a>
                </div>

                <p style="margin-bottom: 20px; color: var(--text-secondary);">Dữ liệu được đọc trực tiếp từ tệp <code>students.json</code> trong container.</p>

                <table>
                    <thead>
                        <tr>
                            <th>Mã SV</th><th>Họ và tên</th><th>Chuyên ngành</th><th>GPA</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in students %}
                        <tr>
                            <td style="font-family: monospace; color: var(--primary); font-weight: 600;">{{ s.student_id }}</td>
                            <td>{{ s.name }}</td>
                            <td>{{ s.major }}</td>
                            <td><span class="gpa-badge">{{ s.gpa }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, students=students)
    except Exception as e:
        return f"<h1 style='color:red'>Lỗi JSON: {str(e)}</h1>", 500

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Access Granted to Secure Cloud Resource", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
