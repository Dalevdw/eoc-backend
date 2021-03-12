from flask import Flask, render_template, request, jsonify
import sqlite3
from flask_cors import CORS


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d


def init_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute(
        'CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, username TEXT, password TEXT, repeat_password TEXT, email TEXT)')

    print("Table created")
    # conn.execute
    # ("CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT")
    # cur = conn.cursor()
    # print(cur.fetchall())


init_db()
app = Flask(__name__)
CORS(app)


@app.route('/add-new/', methods=['POST'])
def add():
    if request.method == "POST":
        post_data = request.get_json()
        first_name = post_data['first_name']
        username = post_data['username']
        password = post_data['password']
        repeat_password = post_data['repeat_password']
        email = post_data['email']

        print(first_name, username, password, email)
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO accounts (first_name, username, password,  repeat_password, email) VALUES (?, ?, ?, ?, ?,)",
                            (first_name, username, password, repeat_password, email))
                # cur.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin')",
                #             (username, password))
                con.commit()
                msg = first_name + "Account created"
        except Exception as x:
            con.rollback()
            msg = "Error, insert operation:" + str(x)
        finally:

            return jsonify(msg=msg)


@app.route('/show-record/', methods=['GET'])
def list_users():
    # if request.method == "GET":
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM accounts")
            con.commit()
            rows = cur.fetchall()

    except Exception as e:
        con.rollback()
        print("Something happened when getting data from db:" + str(e))
    finally:
        return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True)
