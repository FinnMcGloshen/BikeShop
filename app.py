
from flask import Flask,render_template,request,redirect, session,url_for
import psycopg2

app = Flask(__name__)
app.secret_key = 'JMnQZxe1IdA8MUIjUNAcm6PbiXaftmjC0cJRK3sO'

def get_db_connection():
   conn = psycopg2.connect(
   host = 'localhost',
   database = 'X',
   user = 'postgres',
   password = 'pgadmin'
   )

   return conn

@app.route("/register")
def register(error =None):   
    return render_template("register.html", error=error)

@app.route("/register", methods=["POST"])
def registers():

    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT username, password FROM bikeproject")
    users = curr.fetchall()

    if request.method == 'POST':
        name1 = request.form['name']
        user1 = request.form['username']
        pass1 = request.form['password']
        email1 = request.form['email']
        if [in_user, in_pass] not in users:
            curr.execute("INSERT INTO users (name, username, password, email) VALUES (%s, %s, %s, %s)", [name1, user1, pass1, email1])
            conn.commit()
            
            curr.close()
            conn.close()
            return redirect(url_for('login'))
        else:
            curr.close()
            conn.close()
            return redirect(url_for('register',error='existingaccount'))

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/", methods=["POST", "GET"])
def logins():
    print("here")
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT username, password FROM users")
    users = curr.fetchall()

    if request.method == 'POST':
        user1 = request.form['username']
        pass1 = request.form['password']

        if (user1, pass1) in users:
            curr.execute("SELECT name FROM users WHERE username = %s AND password = %s", [user1, pass1])
            name = curr.fetchone()
            curr.execute("SELECT email FROM users WHERE username = %s AND password = %s", [user1, pass1])
            email = curr.fetchone()

            active_user = [name[0], user1, pass1, email[0]]
            session["active_user"] = active_user

            curr.close()
            conn.close()
            return redirect(url_for('shop'))
        else:
            return redirect(url_for('login',error='faillogin'))


@app.route("/shop")
def shop():
    return render_template("shop.html")




if __name__ == '__main__':

   app.run(debug=True)