CREATE DATABASE IF NOT EXISTS minicloud;
USE minicloud;
CREATE TABLE IF NOT EXISTS notes(
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO notes(title) VALUES ('Day la he thong cloud cua Khang va Minh - MariaDB Connected!');

CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL UNIQUE,
  full_name VARCHAR(100) NOT NULL,
  major VARCHAR(100) NOT NULL,
  gpa DECIMAL(3,2) NOT NULL
);
INSERT INTO students (student_id, full_name, major, gpa) VALUES
  ('523H0039', 'Pham Nguyen Duy Khang', 'Software Engineering', 8.50),
  ('523H0055', 'Tran Vu Nhat Minh', 'Software Engineering', 8.60),
  ('523H0000', 'Nguyen Van A', 'Software Engineering', 7.50);
