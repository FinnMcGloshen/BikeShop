from flask import Flask,render_template,request,redirect, session,url_for, flash
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
import urllib.request
import psycopg2
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'JMnQZxe1IdA8MUIjUNAcm6PbiXaftmjC0cJRK3sO'

private_key = RSA.generate(1024)
public_key = private_key.publickey()

print(public_key)
print(private_key)

private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()

print(private_pem)
print(public_pem)

with open('private.pem', 'w') as pr:
	pr.write(private_pem)
with open('public.pem', 'w') as pu:
	pu.write(public_pem)

print('private.pem:')
with open('private.pem', 'r') as f:
	print(f.read())

print('public.pem:')
with open('public.pem', 'r') as f:
        print(f.read())

pr_key = RSA.import_key(open('private.pem', 'r').read())
pu_key = RSA.import_key(open('public.pem', 'r').read())

cipher = PKCS1_OAEP.new(key=pu_key)
decrypt = PKCS1_OAEP.new(key=pr_key)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def get_db_connection():
   conn = psycopg2.connect(
   host = 'localhost',
   database = 'X',
   user = 'postgres',
   password = 'pgadmin'
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
        encoded_pass = pass1.encode()
        encrypted_pass = cipher.encrypt(encoded_pass)
        

        email1 = request.form['email']
        key = (user1,encrypted_pass)
        if key not in users:
            print(key)
            print(users)
            print('making new account')
            curr.execute("INSERT INTO bikeproject (name, username, password, email) VALUES (%s, %s, %s, %s)", [name1, user1, encrypted_pass, email1])
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
        
        decrypted_pass = decrypt.decrypt(encrypted_pass)

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

# @app.route('/display/<filename>')
# def display_image(filename):
# 	print('display_image filename: ' + filename)
# 	return redirect(url_for('static', filename='uploads/' + filename), code=301)
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/manager", methods=["POST"])
def edit():
    b1name = request.form['b1name']
    print(b1name)
    b1price = request.form['b1price']
    print(b1price)
    b1desc = request.form['b1desc']
    print(b1desc)
    # b1image = request.files['b1image'].filename
    # b1image1 = "'"+UPLOAD_FOLDER+b1image+"'"
    # print(b1image)
    if request.method == "POST":
        print('here')
        file = request.files['b1image'].filename
        print(file)
        # if file and allowed_file(file.filename):
        #     print('here again')
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return render_template('manager.html',b1desc = b1desc,b1price=b1price,b1name=b1name,file=file)
        # # b1image.save(secure_filename(b1image.filename))



    # if file not in request.files:
    #     flash('No file part')
    #     return redirect('manager')
    #     file = request.files['file']
    # if file.filename == '':
    #     flash('No image selected for uploading')
    #     return redirect('manager')
    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     print('upload_image filename: ' + filename)
    #     flash('Image successfully uploaded and displayed below')
    #     return render_template('manager.html', b1desc = b1desc,b1price=b1price,b1name=b1name,b1image=b1image)
    # else:
    #     flash('Allowed image types are -> png, jpg, jpeg, gif')
    return render_template('manager.html',b1desc = b1desc,b1price=b1price,b1name=b1name,file=file)



@app.route("/shop")
def shop():
    return render_template("prebuilt.html")

@app.route("/shop", methods=["POST", "GET"])
def shop1():
    conn = get_db_connection()
    curr = conn.cursor()


    active_user = session["active_user"]
    print(active_user)

    if request.method == 'POST':

        
            if request.form.get('Buy1'):
                curr.execute("SELECT * FROM bikes WHERE bicycle_name = 'Bicycle1'")
                bike = curr.fetchone()
                print(bike)
                entry = [active_user[0], active_user[1], active_user[2], active_user[3], bike[0], bike[1]]
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
    return render_template("Checkout.html")


if __name__ == '__main__':
   app.run(debug=True)