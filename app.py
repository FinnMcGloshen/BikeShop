from flask import Flask,render_template,request,redirect, session,url_for, flash
# from Crypto.Cipher import PKCS1_OAEP
# from Crypto.PublicKey import RSA
from binascii import hexlify
import urllib.request
import psycopg2
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'JMnQZxe1IdA8MUIjUNAcm6PbiXaftmjC0cJRK3sO'

b1name = 'Bike 1'
b1price = '$12000'
b1desc = 'This mountian bike is not only sturdy but also loooks good to the eye.'
# message = 'hello pass'
# private_key = RSA.generate(1024)
# public_key = private_key.publickey()

# # print(public_key)
# # print(private_key)

# private_pem = private_key.export_key().decode()
# public_pem = public_key.export_key().decode()

# # print(private_pem)
# # print(public_pem)

# with open('private.pem', 'w') as pr:
# 	pr.write(private_pem)
# with open('public.pem', 'w') as pu:
# 	pu.write(public_pem)

# print('private.pem:')
# with open('private.pem', 'r') as f:
# 	print(f.read())

# print('public.pem:')
# with open('public.pem', 'r') as f:
#         print(f.read())

# pr_key = RSA.import_key(open('private.pem', 'r').read())
# pu_key = RSA.import_key(open('public.pem', 'r').read())

# cipher = PKCS1_OAEP.new(key=pu_key)
# decrypt = PKCS1_OAEP.new(key=pr_key)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
        # encoded_pass = bytes(pass1, 'utf-8')
        # encrypted_pass = cipher.encrypt(encoded_pass)
        # print(encrypted_pass)
        

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

        cur.execute('DROP TABLE IF EXISTS orders2;')
        cur.execute('''
                CREATE TABLE orders2 (
                   name text, 
                   username varchar(50), 
                   password varchar(50), 
                   email varchar(50), 
                   part_name varchar(100), 
                   part_price varchar(100)
                    )
                    ''')

        cur.execute('DROP TABLE IF EXISTS orders3;')
        cur.execute('''
                CREATE TABLE orders3 (
                   name text, 
                   username varchar(50), 
                   password varchar(50), 
                   email varchar(50), 
                   part varchar(100), 
                   price_part varchar(100)
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
                ('Bicycle12','$800'),
                ('Bicycle13','$500')''')
        conn.commit()

        cur.execute('DROP TABLE IF EXISTS Customize;')

        cur.execute('''
                CREATE TABLE Customize (
                   part_name varchar(50), 
                   part_price varchar(50)
                    )
                    ''')
        conn.commit()
        cur.execute('''
                INSERT INTO Customize (part_name, part_price) VALUES ('Gay Wheels','$15'),
                ('Mountain Bike Wheels','$100'),
                ('Race Wheels','$150'),
                ('Future wheels','$420'),
                ('Carbon Road Frame','$1,500'),
                ('Gravel Frame','$800'),
                ('Carbon Mountain Frame','$3,000'),
                ('Mountain Frame','$1,973'),
                ('12-Speed XTR Chain','$68.99'),
                ('Ultegra 10-Speed Chain','$43.99'),
                ('PC-850 8-Speed Chain','$$25.00'),
                ('NX Eagle Chain','$28.00'),
                ('xt Mountain bike Pedals','$156.81'),
                ('PD-EH500 Dual Sided Pedals','$79.99'),
                ('Shimano Dura-Ace PD-R9100 Pedals','$279.99'),
                ('Garmin Vector 3 Power Pedals','$699.00'),
                ('Alloy Road Bike Handlebars','$300.00'),
                ('Carbon Fiber Road Bike Handlebars','$500.00'),
                ('Carbon Fiber Race Bike Handlebars','$500.00'),
                ('Bike Handlebars','$100.00'),
                ('Sugino Messenger Track Fixed Gear 44t','$174.40'),
                ('Gear Mountain Bike Racing Professional','$46.60'),
                ('JRL 10Tooth Clutch Gear Drive Sprocket','$5.99'),
                ('Ultegra FC-R8000 Crankset','$289.99')''')
        conn.commit()

        cur.execute('''
                CREATE TABLE parttabel (
                   part varchar(100), 
                   price_part varchar(100)
                    )
                    ''')
        conn.commit()
        cur.execute('''
                INSERT INTO parttabel (part, price_part) VALUES ('Cloud 9 Cruiser Anatomic HD','$27.69'),
                ('Big Seat','$89.95'),
                ('Sunlite Backrest Saddle','$69.95'),
                ('Classic Bike Bell','$6.98'),
                ('Kids Bike Bell','$11.99'),
                ('Electric Bike Bell','$14.99'),
                ('Bontrager Ion 200 RT Front Bike Light','$64.99'),
                ('Bontrager Ion RT/Flare RT Light Set','$11.99'),
                ('Electra Retro Headlight','$54.99'),
                ('Zefal Spy Mirro','$14.99'),
                ('Third Eye Bar End Mirror','$11.00'),
                ('Sprintech Dropbar Mirror','$34.99')''')
        conn.commit()
        return render_template("login.html",error=error)

@app.route("/", methods=["POST", "GET"])
def logins():
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT username, password FROM bikeproject")
    users = curr.fetchall() 
    if request.method == 'POST':
        user1 = request.form['username']
        pass1 = request.form['password']

        # passwordFromDB = ''
        # for i in users:
        #     if i[0]==user1:
        #         passwordFromDB = i[1]
    
        # decrypt_key = PKCS1_OAEP.new (key=pr_key)
        # print((passwordFromDB.tobytes()))
        # decrypted_pass = decrypt_key.decrypt(passwordFromDB)
        
        
            
        
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

    return redirect(url_for('login'))

@app.route("/manager")
def manager():
    return render_template('manager.html')

# @app.route('/display/<filename>')
# def display_image(filename):
# 	print('display_image filename: ' + filename)
# 	return redirect(url_for('static', filename='uploads/' + filename), code=301)
# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/manager", methods=["POST"])
def edit():
    conn = get_db_connection()
    curr = conn.cursor()
    
    b1name = request.form['b1name']
    print(b1name)
    b1price = request.form['b1price']
    print(b1price)
    b1desc = request.form['b1desc']
    print(b1desc)
    curr.execute("UPDATE bikes SET bicycle_price = %s WHERE bicycle_name = 'Bicycle13';", [b1price])
    print('price updated')
    conn.commit()
    curr.close()
    conn.close()
    
   
    return render_template('manager.html',b1desc = b1desc,b1price=b1price,b1name=b1name)

@app.route("/desc")
def descrp():
    return render_template('Description.html')

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

            if request.form.get('Buy13'):
                    curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle13'")
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
    

@app.route("/Customize", methods=["POST", "GET"])
def cust1():
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT part_name,part_price FROM orders2")
    x = curr.fetchall()
    
    active_user = session["active_user"]
    print(active_user)

    if request.method == 'POST':
            if request.form.get('w1'):
                curr.execute("SELECT * FROM Customize WHERE part_name = 'Gay Wheels'")
                partname = curr.fetchone()
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], partname[0], partname[1]]
                curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('cust'))

           
            if request.form.get('w2'):
                curr.execute("SELECT * FROM Customize WHERE part_name = 'Mountain Bike Wheels'")
                part_name = curr.fetchone()
                print(part_name)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('cust'))

            
            if request.form.get('w3'):
                curr.execute("SELECT * FROM Customize WHERE part_name = 'Race Wheels'")
                part_name = curr.fetchone()
                print(part_name)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('cust'))

            if request.form.get('w4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Future wheels'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('f1'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Carbon Road Frame'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('f2'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Gravel Frame'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('f3'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Carbon Mountain Frame'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('f4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Mountain Frame'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('c1'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = '12-Speed XTR Chain'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('c2'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Ultegra 10-Speed Chain'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('c3'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'PC-850 8-Speed Chain'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('c4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'NX Eagle Chain'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('p1'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'xt Mountain bike Pedals'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('p2'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'PD-EH500 Dual Sided Pedals'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('p3'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Shimano Dura-Ace PD-R9100 Pedals'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('p4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Garmin Vector 3 Power Pedals'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('h1'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Alloy Road Bike Handlebars'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('h2'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Carbon Fiber Road Bike Handlebars'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('h3'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Carbon Fiber Race Bike Handlebars'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('h4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Bike Handlebars'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('g1'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Sugino Messenger Track Fixed Gear 44t'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

           
            if request.form.get('g2'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Gear Mountain Bike Racing Professional'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

            if request.form.get('g3'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'JRL 10Tooth Clutch Gear Drive Sprocket'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))

           
            if request.form.get('g4'):
                    curr.execute("SELECT * FROM Customize WHERE part_name = 'Ultegra FC-R8000 Crankset'")
                    part_name = curr.fetchone()
                    print(part_name)
                    entry = [active_user[0], active_user[1], active_user[2], active_user[3], part_name[0], part_name[1]]
                    curr.execute("INSERT INTO orders2 (name, username, password, email, part_name, part_price) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                    conn.commit()
                    curr.close()
                    conn.close()
                    return redirect(url_for('cust'))



@app.route("/Parts")
def part():
    return render_template("parts.html")

@app.route("/Parts", methods=["POST", "GET"])
def part1():
    conn = get_db_connection()
    curr = conn.cursor()


    active_user = session["active_user"]
    print(active_user)

    if request.method == 'POST':
            if request.form.get('s1'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Cloud 9 Cruiser Anatomic HD'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('s2'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Big Seat'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('s3'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Sunlite Backrest Saddle'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('b1'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Classic Bike Bell'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('b2'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Kids Bike Bell'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))
                
    if request.method == 'POST':
            if request.form.get('b3'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Kids Bike Bell'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('l1'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Bontrager Ion 200 RT Front Bike Light'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('l2'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Bontrager Ion RT/Flare RT Light Set'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('l3'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Electra Retro Headlight'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('m1'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Zefal Spy Mirror'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('m2'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Third Eye Bar End Mirror'")
                part = curr.fetchone()
                print(part)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

    if request.method == 'POST':
            if request.form.get('m3'):
                curr.execute("SELECT * FROM parttabel WHERE part = 'Sprintech Dropbar Mirror'")
                part = curr.fetchone()
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], part[0], part[1]]
                curr.execute("INSERT INTO orders3 (name, username, password, email, part, price_part) VALUES (%s, %s, %s, %s, %s, %s)", (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]))
                conn.commit()
                curr.close()
                conn.close()
                return redirect(url_for('part1'))

@app.route("/Checkout")
def check():
    conn = get_db_connection()
    curr = conn.cursor()

    curr.execute("SELECT bicycle_name,bicycle_price FROM orders")
    x = curr.fetchall()

    curr.execute("SELECT part_name,part_price FROM orders2")
    y = curr.fetchall()

    curr.execute("SELECT part,price_part FROM orders3")
    z = curr.fetchall()
    return render_template("Checkout.html", x=x, y=y, z=z)

@app.route("/Receipt")
def re():
    return render_template("Receipt.html")


if __name__ == '__main__':
   app.run(debug=True)