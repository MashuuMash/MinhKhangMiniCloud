import mysql.connector
from flask import Flask, jsonify, request, render_template_string
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
ISSUER   = os.getenv("OIDC_ISSUER",   "http://authentication-identity-server:8080/realms/master")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

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

@app.get("/hello")
def hello(): 
    return jsonify(message="Hello from App Server!", members=["Khang", "Minh"])

# Helper to get DB connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.get("/student")
def get_students():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/api/students-db")
def students_db_page():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        # Emerald Green Dashboard Template
        html_template = """
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Student Management - MariaDB</title>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {
                    --bg-color: #121212;
                    --card-bg: rgba(255, 255, 255, 0.05);
                    --primary: #10b981;
                    --primary-hover: #059669;
                    --text-main: #f3f4f6;
                    --text-secondary: #9ca3af;
                }
                * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
                body {
                    background-color: var(--bg-color);
                    color: var(--text-main);
                    padding: 40px 20px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    min-height: 100vh;
                }
                .container {
                    width: 100%;
                    max-width: 1000px;
                    background: var(--card-bg);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    border-radius: 16px;
                    padding: 30px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    padding-bottom: 20px;
                }
                .header h1 { font-size: 1.8rem; color: var(--primary); font-weight: 700; }
                .status-badge {
                    background: rgba(16, 185, 129, 0.1);
                    color: var(--primary);
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.85rem;
                    font-weight: 500;
                    border: 1px solid var(--primary);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }
                th {
                    text-align: left;
                    padding: 15px;
                    color: var(--text-secondary);
                    font-weight: 600;
                    font-size: 0.9rem;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                }
                td {
                    padding: 18px 15px;
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                    font-size: 1rem;
                }
                tr:hover td {
                    background: rgba(255, 255, 255, 0.02);
                }
                .student-id { font-family: monospace; font-size: 1.1rem; color: var(--primary); }
                .gpa-badge {
                    background: var(--primary);
                    color: #000;
                    padding: 2px 8px;
                    border-radius: 6px;
                    font-weight: 700;
                    font-size: 0.9rem;
                }
                .footer {
                    margin-top: 30px;
                    text-align: center;
                    color: var(--text-secondary);
                    font-size: 0.85rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Danh sách sinh viên (MariaDB)</h1>
                    <div class="status-badge">Connected: relational-database-server</div>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Mã sinh viên</th>
                            <th>Họ và tên</th>
                            <th>Chuyên ngành</th>
                            <th>GPA</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in students %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td><span class="student-id">{{ s.student_id }}</span></td>
                            <td>{{ s.full_name }}</td>
                            <td>{{ s.major }}</td>
                            <td><span class="gpa-badge">{{ s.gpa }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                <div class="footer">
                    &copy; 2026 MyMiniCloud - Khang & Minh. Toàn bộ dữ liệu được truy vấn thực tế từ Cloud Database.
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template, students=students)
    except Exception as e:
        return f"<h1 style='color:red'>Lỗi hệ thống: {str(e)}</h1>", 500

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
