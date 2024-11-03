CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    level VARCHAR(50),
    gender VARCHAR(10)
);

CREATE TABLE grades (
    grade_id INT PRIMARY KEY,
    student_id INT,
    course_code VARCHAR(10),
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE exams (
    exam_id INT PRIMARY KEY,
    exam_code VARCHAR(10),
    course_code VARCHAR(10)
);

CREATE TABLE finances (
    finance_id INT PRIMARY KEY,
    student_id INT,
    fee_due DECIMAL(10, 2),
    fee_paid DECIMAL(10, 2),
    fee_balance AS (fee_due - fee_paid),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100)
);

CREATE TABLE courses (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(100),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE student_courses (
    student_id INT,
    course_code VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
);

INSERT INTO students (student_id, name, level, gender) VALUES
(1, 'Alice Johnson', 'Undergraduate', 'Female'),
(2, 'Bob Smith', 'Graduate', 'Male'),
(3, 'Carol White', 'Undergraduate', 'Female'),
(4, 'David Brown', 'Postgraduate', 'Male'),
(5, 'Eve Davis', 'Undergraduate', 'Female'),
(6, 'Frank Miller', 'Graduate', 'Male'),
(7, 'Grace Wilson', 'Postgraduate', 'Female'),
(8, 'Hank Moore', 'Undergraduate', 'Male'),
(9, 'Ivy Taylor', 'Undergraduate', 'Female'),
(10, 'Jack Anderson', 'Graduate', 'Male');


INSERT INTO departments (department_id, department_name) VALUES
(1, 'Computer Science'),
(2, 'English Literature'),
(3, 'Mathematics'),
(4, 'Physics'),
(5, 'Biology');

INSERT INTO courses (course_code, course_name, department_id) VALUES
('CS101', 'Introduction to Computer Science', 1),
('ENG102', 'English Composition', 2),
('MATH201', 'Calculus I', 3),
('PHYS301', 'General Physics', 4),
('BIO405', 'Genetics', 5);

INSERT INTO student_courses (student_id, course_code) VALUES
(1, 'CS101'),
(1, 'ENG102'),
(2, 'MATH201'),
(3, 'PHYS301'),
(4, 'BIO405'),
(5, 'CS101'),
(6, 'ENG102'),
(7, 'MATH201'),
(8, 'PHYS301'),
(9, 'BIO405'),
(10, 'CS101');

INSERT INTO exams (exam_id, exam_code, course_code) VALUES
    (1, 'EXAM101', 'CS101'),
    (2, 'EXAM102', 'ENG102'),
    (3, 'EXAM103', 'MATH201'),
    (4, 'EXAM104', 'PHYS301'),
    (5, 'EXAM105', 'BIO405');


INSERT INTO grades (grade_id, student_id, course_code, grade) VALUES
(1, 1, 'CS101', 'A'),
(2, 1, 'ENG102', 'B+'),
(3, 2, 'MATH201', 'B'),
(4, 3, 'PHYS301', 'A-'),
(5, 4, 'BIO405', 'B'),
(6, 5, 'CS101', 'A'),
(7, 6, 'ENG102', 'C'),
(8, 7, 'MATH201', 'A'),
(9, 8, 'PHYS301', 'B+'),
(10, 9, 'BIO405', 'A');


INSERT INTO finances (finance_id, student_id, fee_due, fee_paid) VALUES
(1, 1, 5000.00, 3000.00),
(2, 2, 5000.00, 2500.00),
(3, 3, 5000.00, 5000.00),
(4, 4, 7000.00, 4000.00),
(5, 5, 5000.00, 1000.00),
(6, 6, 6000.00, 4000.00),
(7, 7, 5500.00, 2000.00),
(8, 8, 5000.00, 5000.00),
(9, 9, 4500.00, 3500.00),
(10, 10, 6000.00, 1000.00);