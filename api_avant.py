import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def find_first_no_repeating_char(name):
    lower_name = name.lower()
    counts_char = {}

    for char in lower_name:
        if char in counts_char:
            counts_char[char] = counts_char[char] + 1
        else:
            counts_char[char] = 1
    
    for char in lower_name:
        if counts_char[char] == 1:
            return char
    
    return '_'

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    data_students = cursor.fetchall()
    conn.close()

    students_list = []
    for row in data_students:
        student = {
            'id': row[0],
            'name': row[1],
            'grade': row[2],
            'first_non_repeating': find_first_no_repeating_char(row[1])
        }
        students_list.append(student)

    return jsonify(students_list)

@app.route('/students/<int:id>', methods=['GET'])
def get_one_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    sql_command = "SELECT * FROM students WHERE id = ?"
    
    cursor.execute(sql_command, (id,))
    
    student_row = cursor.fetchone()
    conn.close()

    if student_row is None:
        return jsonify({'error': 'Student not found'}), 404
    else:
        student = {
            'id': student_row[0],
            'name': student_row[1],
            'grade': student_row[2],
            'first_non_repeating': find_first_no_repeating_char(student_row[1])
        }
        return jsonify(student)

@app.route('/students', methods=['POST'])
def post_students():
    student_data = request.get_json()
    name = student_data['name']
    grade = student_data['grade']

    if not 0 <= grade <= 10:
        return jsonify({'error': 'Grade must be between 0 and 10'}), 400
    
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    sql_command = 'INSERT INTO students (name, grade) VALUES (?, ?)'
    cursor.execute(sql_command, (name, grade))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student created successfully'}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
