import os, sqlite3
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
app=FastAPI(); DB='/tmp/challenge.db'
db=sqlite3.connect(DB); db.executescript('CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT); CREATE TABLE IF NOT EXISTS secret_flag(flag TEXT); DELETE FROM secret_flag;'); db.execute('INSERT INTO secret_flag VALUES (?)',(os.getenv('FLAG','vladilk{local-second-order}'),)); db.commit(); db.close()
@app.post('/register',response_class=HTMLResponse)
def register(username:str=Form(...),password:str=Form(...)):
    conn=sqlite3.connect(DB); conn.execute('INSERT INTO users VALUES (?,?)',(username,password)); conn.commit(); conn.close(); return 'Registered. <a href="/">Login</a>'
@app.post('/login',response_class=HTMLResponse)
def login(username:str=Form(...),password:str=Form(...)):
    conn=sqlite3.connect(DB); stored=conn.execute('SELECT username,password FROM users WHERE username=? AND password=?',(username,password)).fetchone()
    if not stored: return 'User not found'
    sql=f"SELECT * FROM users WHERE username='{stored[0]}' AND password='{stored[1]}'"
    try: result=conn.execute(sql).fetchall(); message=str(result)
    except sqlite3.Error as exc: message=f'SQLite error: {exc}'
    conn.close(); return f'<pre>{sql}\n{message}</pre>'
@app.get('/',response_class=HTMLResponse)
def index(): return '<h1>Second-order SQLi</h1><form method="post" action="/register">Register <input name="username"><input name="password"><button>Register</button></form><form method="post" action="/login">Login <input name="username"><input name="password"><button>Login</button></form>'
