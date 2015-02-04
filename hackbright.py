import sqlite3
import re

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project(title):
    query = """SELECT * FROM Projects WHERE title = ?""" 
    DB.execute(query, (title,))
    single_proj = DB.fetchone()
    print """The project is titled %s, 
it's description is %s 
and has a maximum grade of %s.""" % (single_proj[1], 
        single_proj[2], single_proj[3])

# def add_project(title, description, max_grade):
#     query = """INSERT into Projects (title, description, max_grade) Values (?,?,?)"""
#     DB.execute(query, (title, description, max_grade))
#     CONN.commit()
#     print "Successfully added project: %s %s %s" % (title, description, max_grade)

# def get_grade(project):
#     query = """SELECT project_title, grade, student_github FROM grades WHERE project_title = ?"""
#     DB.execute(query, (project,))
#     grade_time = DB.fetchone()
#     print "The project %s has recieved the following grade %s for github user %s" % (grade_time[0], 
#         grade_time[1], grade_time[2])

def get_grade(first_name, last_name, project_title):
    query = """SELECT first_name, last_name, project_title, grade FROM 
    students JOIN grades ON github=student_github WHERE first_name = ? AND last_name = ? AND project_title = ?"""
    DB.execute(query, (first_name, last_name, project_title))
    row = DB.fetchone()
    print """The grade of %s %s for %s is %s.""" % (row[0], row[1], row[2], row[3])

def give_grade(grade, project_title, first_name, last_name):
    github_query = """SELECT github FROM Students WHERE first_name = ? AND last_name = ?"""
    DB.execute(github_query, (first_name, last_name))
    github = DB.fetchone()[0]
    query = """INSERT INTO Grades VALUES (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added grade %s of project %s to student %s %s" %\
    (grade, project_title, first_name, last_name)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(' ')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_project":
            get_project(*args)
        # elif command == "add_project":
        #     add_project(*args)
        elif command == "get_grade":
            get_grade(*args)
        elif command == "give_grade":
            give_grade(*args)


    CONN.close()


if __name__ == "__main__":
    main()
