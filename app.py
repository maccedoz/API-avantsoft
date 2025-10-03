import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('students.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

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

def find_first_non_repeating_char(name):
    lower_name = name.lower()
    counts = {}
    for char in lower_name:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    
    for char in lower_name:
        if counts[char] == 1:
            return char
    return '_'

@app.route('/students', methods=['GET'])
def get_students():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    
    students_list = []
    for row in rows:
        student = dict(row)
        student['first_non_repeating'] = find_first_non_repeating_char(student['name'])
        students_list.append(student)
        
    return jsonify(students_list)

@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    db = get_db()
    cursor = db.cursor()
    sql_command = "SELECT * FROM students WHERE id = ?"
    cursor.execute(sql_command, (id,))
    row = cursor.fetchone()
    
    if row is None:
        return jsonify({'error': 'Student not found'}), 404
    else:
        student = dict(row)
        student['first_non_repeating'] = find_first_non_repeating_char(student['name'])
        return jsonify(student)

@app.route('/students', methods=['POST'])
def post_students():
    try:
        student_data = request.get_json()
        if not student_data:
            return jsonify({'error': 'Invalid JSON'}), 400
        
        name = student_data['name']
        grade = int(student_data['grade'])
    except (KeyError, TypeError):
        return jsonify({'error': 'Missing or invalid name/grade field'}), 400
    except ValueError:
        return jsonify({'error': 'Grade must be a valid integer'}), 400

    if not 0 <= grade <= 10:
        return jsonify({'error': 'Grade must be between 0 and 10'}), 400
    
    db = get_db()
    cursor = db.cursor()
    sql_command = 'INSERT INTO students (name, grade) VALUES (?, ?)'
    cursor.execute(sql_command, (name, grade))
    db.commit()

    return jsonify({'message': 'Student created successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True) #apenas para debbugar e ver se funciona