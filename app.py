from flask import Flask,render_template,request,redirect, session,url_for, flash
import psycopg2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'JMnQZxe1IdA8MUIjUNAcm6PbiXaftmjC0cJRK3sO'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
   conn = psycopg2.connect(
   host = 'localhost',
   database = 'flask_db',
   user = 'postgres',
   password = '8010199'
   )

   return conn

@app.route("/register")
def register(error=None):   
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
        key = (user1,pass1)
        if key not in users:
            print(key)
            print(users)
            print('making new account')
            curr.execute("INSERT INTO bikeproject (name, username, password, email) VALUES (%s, %s, %s, %s)", [name1, user1, pass1, email1])
            conn.commit()
            
            curr.close()
            conn.close()
            return redirect(url_for('login'))
        elif key in users:
            print('account already exists')
            curr.close()
            conn.close()
            flash('Account already exists')
            return redirect(url_for('register',error='existingaccount'))

@app.route("/")
def login(error = None):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS orders;')
        cur.execute('''
                CREATE TABLE orders (
                   name text, 
                   username varchar(50), 
                   password varchar(50), 
                   email varchar(50), 
                   bicycle_name varchar(20), 
                   bicycle_price varchar(20)
                    )
                    ''')

        cur.execute('DROP TABLE IF EXISTS bikes;')

        cur.execute('''
                CREATE TABLE bikes (
                   bicycle_name varchar(20), 
                   bicycle_price varchar(20)
                    )
                    ''')
        conn.commit()
        cur.execute('''
                INSERT INTO bikes (bicycle_name, bicycle_price) VALUES ('Bicycle1','$12,000'),
                ('Bicycle2','$900'),
                ('Bicycle3','$700'),
                ('Bicycle4','$250'),
                ('Bicycle5','$50'),
                ('Велосипед6','₽448,049.79'),
                ('Bicycle7','$500'),
                ('Bicycle8','$1,000'),
                ('Bicycle9','$1,500'),
                ('Bicycle10','$5,000'),
                ('Bicycle11','$550'),
                ('Bicycle12','$800')''')
        conn.commit()
        return render_template("login.html",error=error)

@app.route("/", methods=["POST", "GET"])
def logins():
    print("here")
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT username, password FROM bikeproject")
    users = curr.fetchall()

    if request.method == 'POST':
        user1 = request.form['username']
        pass1 = request.form['password']

        if (user1, pass1) in users:
            curr.execute("SELECT name FROM bikeproject WHERE username = %s AND password = %s", [user1, pass1])
            name = curr.fetchone()
            curr.execute("SELECT email FROM bikeproject WHERE username = %s AND password = %s", [user1, pass1])
            email = curr.fetchone()

            active_user = [name[0], user1, pass1, email[0]]
            session["active_user"] = active_user

            curr.close()
            conn.close()
            return redirect(url_for('shop'))
        elif user1=='admin' and pass1 == 'admin':
            return redirect(url_for('manager'))
        else:
            flash('Incorrect Username or Password')
            return redirect(url_for('login',error='noaccount'))

@app.route("/manager")
def manager():
    return render_template('manager.html')

@app.route("/manager", methods=["POST"])
def edit():
    b1name = request.form['b1name']
    b1price = request.form['b1price']
    b1desc = request.form['b1desc']
    filename = request.form['b1image']
    # if 'file' not in request.files:
	# 	flash('No file part')
	# 	return redirect(request.url)
	# file = request.files['file']
	# if file.filename == '':
	# 	flash('No image selected for uploading')
	# 	return redirect(request.url)
	# if file and allowed_file(file.filename):
	# 	filename = secure_filename(file.filename)
	# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	# 	#print('upload_image filename: ' + filename)
	# 	flash('Image successfully uploaded and displayed below')
	# 	return render_template('upload.html', filename=filename)
	# else:
	# 	flash('Allowed image types are -> png, jpg, jpeg, gif')
	# 	return redirect(request.url)
    return render_template('manager.html',b1desc = b1desc,b1price=b1price,b1name=b1name,filename=filename)

@app.route("/shop")
def shop():
    return render_template("prebuilt.html")

@app.route("/shop", methods=["POST", "GET"])
def shop1():
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT bicycle_name,bicycle_price FROM orders")
    x = curr.fetchall()
    

    active_user = session["active_user"]
    print(active_user)

    if request.method == 'POST':

            if request.form.get('Cust1'):
                curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle1'")
                bike = curr.fetchone()
                print(bike)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                print(entry)
                curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('cust'))

            if request.form.get('Cust2'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle2'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust3'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle3'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust4'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle4'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust5'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle5'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust6'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Велосипед6'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust7'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle7'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust8'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle8'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust9'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle9'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust10'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle10'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust11'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle11'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('Cust12'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle12'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))
        
            if request.form.get('Buy1'):
                curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle1'")
                bike = curr.fetchone()
                print(bike)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                print(entry)
                curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('shop'))

            if request.form.get('Buy2'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle2'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy3'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle3'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy4'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle4'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy5'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle5'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy6'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Велосипед6'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy7'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle7'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy8'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle8'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy9'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle9'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy10'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle10'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy11'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle11'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

            if request.form.get('Buy12'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle12'")
                    bike = curr.fetchone()
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
                    curr.execute("INSERT INTO orders (name, username, password, email, bicycle_name, bicycle_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('shop'))

@app.route("/Customize")
def cust():
    return render_template("Customize.html")

@app.route("/Checkout")
def check():
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT bicycle_name,bicycle_price FROM orders")
    x = curr.fetchall()
    return render_template("Checkout.html", x=x)


if __name__ == '__main__':
   app.run(debug=True)