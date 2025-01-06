import random
import string
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_session import Session
import pyotp
import qrcode
from io import BytesIO
from flask import send_file
from functools import wraps
import os
import re
from flask_cors import CORS
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
import bcrypt

def hash_password(password):
    """
    Generează un hash bcrypt pentru parola dată.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed_password):
    """
    Verifică dacă parola corespunde hash-ului salvat.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Configurație pentru criptare
SALT_LENGTH = 16
KEY_LENGTH = 32
ITERATIONS = 100000

def generate_key(master_password, salt):
    """
    Generează o cheie derivată folosind PBKDF2.
    """
    return PBKDF2(master_password, salt, dkLen=KEY_LENGTH, count=ITERATIONS)

def encrypt_password(master_password, plain_password):
    """
    Criptează o parolă utilizând AES-GCM.
    """
    salt = os.urandom(SALT_LENGTH)
    key = generate_key(master_password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plain_password.encode('utf-8'))

    return base64.b64encode(salt + nonce + tag + ciphertext).decode('utf-8')

def decrypt_password(master_password, encrypted_data):
    """
    Decriptează o parolă utilizând AES-GCM.
    """
    encrypted_data = base64.b64decode(encrypted_data)
    salt = encrypted_data[:SALT_LENGTH]
    nonce = encrypted_data[SALT_LENGTH:SALT_LENGTH + 16]
    tag = encrypted_data[SALT_LENGTH + 16:SALT_LENGTH + 32]
    ciphertext = encrypted_data[SALT_LENGTH + 32:]

    key = generate_key(master_password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

def generate_password(length, include_lowercase, include_uppercase, include_numbers, include_special):
    characters = ""
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"

    if not characters:
        return "Error: No character types selected."
    
    return ''.join(random.choice(characters) for _ in range(length))

def check_password_strength(password):
    # Define criteria
    min_length = 8
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'\d')
    special_char_regex = re.compile(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]')
    
    # List of most used passwords (can be updated regularly)
    most_used_passwords = [
        "123456", "123456789", "qwerty", "password", "12345", "12345678", "111111", "123123",
        "1234567", "1234567890", "1234", "000000", "iloveyou", "123", "qwertyuiop", "abc123",
        "password1", "123321", "654321", "superman", "hello123", "987654321", "sunshine",
        "1q2w3e4r", "password123", "qwe123", "admin", "letmein", "welcome", "passw0rd",
        "freedom", "whatever", "princess", "dragon", "baseball", "football", "monkey",
        "shadow", "master", "michael", "ashley", "123qwe", "password!", "qazwsx", "trustno1",
        "starwars", "harley", "ninja", "zxcvbnm", "zaq12wsx", "test", "batman", "soccer",
        "mustang", "jordan23", "jennifer", "hunter", "buster", "thomas", "love123", "charlie",
        "access", "q1w2e3r4", "merlin", "maggie", "hello", "password123!", "cookie", "pepper",
        "ginger", "winter", "summer", "apple", "orange", "tigger", "internet", "pokemon",
        "matrix", "star", "letmein123", "hello1234", "welcome123", "flower", "peanut", "football1",
        "iloveyou1", "secure123", "newyork", "chelsea", "123abc", "buster1", "monkey123", "admin123",
        "hunter123", "abc12345", "123456a", "secret", "strong123", "liverpool"
    ]
    
    # Check if password is in the list of most-used passwords
    if password in most_used_passwords:
        return "Weak: Password is too common"
    
    # Check minimum length
    if len(password) < min_length:
        return "Weak: Password should be at least {} characters long".format(min_length)
    
    # Check for uppercase and lowercase letters
    if not uppercase_regex.search(password) or not lowercase_regex.search(password):
        return "Weak: Password should contain at least one uppercase and one lowercase letter"
    
    # Check for digits
    if not digit_regex.search(password):
        return "Weak: Password should contain at least one digit"
    
    # Check for special characters
    if not special_char_regex.search(password):
        return "Weak: Password should contain at least one special character"
    
    # If all criteria are met
    return "Strong: Password meets the criteria"

def set_connection_cursor():
    # Establish a connection to the MySQL database
    connection  = mysql.connector.connect(
        host="localhost",
        user="root",
        password="parolacont1.",
        database="password_management"
    )
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    # Return both the connection and cursor objects
    return connection,cursor

def show_table(ID_master_account):
    # Establish a connection to MySQL                                 
    connection, cursor = set_connection_cursor()
    # Execute the query with the parameter as a tuple
    query = "SELECT site_name, email, account_name, password, details FROM password_management_table WHERE ID_master_account = %s"
    cursor.execute(query, (ID_master_account,))
    rows = cursor.fetchall()
    
    if not rows:  # Dacă nu există date
        return []

    master_account_password = session.get('master_account_password')
    if not master_account_password:
        raise ValueError("Parola master nu este disponibilă pentru decriptare.")

    result = []
    for row in rows:
        try:
            decrypted_password = decrypt_password(master_account_password, row[3])
            result.append((row[0], row[1], row[2], decrypted_password, row[4]))
        except Exception as e:
            print(f"Eroare la decriptarea parolei pentru site-ul {row[0]}: {e}")
            result.append((row[0], row[1], row[2], "EROARE", row[4]))

    # Close cursor and connection
    cursor.close()
    connection.close()
    return result

def get_master_password(ID_master_account):
    connection, cursor = set_connection_cursor()
    query = "SELECT master_account_password FROM account_table WHERE ID_master_account = %s"
    cursor.execute(query, (ID_master_account,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return result[0]  # Parola master este în prima coloană
    else:
        raise Exception("Parola master nu a fost găsită pentru acest cont.")

def show_table_for_modify_entry(ID_master_account):
    # Establish a connection to MySQL
    connection, cursor = set_connection_cursor()
    
    # Execute the query with the parameter as a tuple
    query = """
    SELECT ID_account, site_name, email, account_name, password, details
    FROM password_management_table
    WHERE ID_master_account = %s
    """
    cursor.execute(query, (ID_master_account,))  # Note the comma to make it a tuple
    
    result = cursor.fetchall()
     
    # Close cursor and connection
    cursor.close()
    connection.close()
    
    return result

def insert_into_table(site_name, email, account_name, password, details, ID_master_account):
    connection, cursor = set_connection_cursor()
    master_account_password = session.get('master_account_password')
    if not master_account_password:
        raise ValueError("Parola master nu este disponibilă pentru criptare.")

    encrypted_password = encrypt_password(master_account_password, password)
    # Define your insert statement
    insert_query = "INSERT INTO password_management_table (site_name, email, account_name, password, details, ID_master_account) VALUES (%s, %s, %s, %s, %s, %s)"
    # Data to be inserted                     
    data_to_insert = (site_name, email, account_name, encrypted_password, details, ID_master_account)
    # Execute the insert query                          
    cursor.execute(insert_query, data_to_insert)
    # Commit the transaction
    connection.commit()
    # Close cursor and connection                             
    cursor.close()
    connection.close()

#new functions    
def create_master_account(master_account_name, master_account_password, master_account_email):
    # Hash password
    hashed_password = hash_password(master_account_password)
    # Generate TOTP secret for 2FA
    totp_secret = pyotp.random_base32()

    connection, cursor = set_connection_cursor()

    # Check if the account name or email already exists
    check_query = """
        SELECT COUNT(*)
        FROM account_table
        WHERE master_account_name = %s OR master_account_email = %s
    """
    cursor.execute(check_query, (master_account_name, master_account_email))
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        # Account name or email already exists
        cursor.close()
        connection.close()
        return False  # Indicate account creation failure

    # Proceed with account creation if no duplicates found
    insert_query = """
        INSERT INTO account_table (master_account_name, master_account_password, master_account_email, totp_secret)
        VALUES (%s, %s, %s, %s)
    """
    data_to_insert = (master_account_name, hashed_password, master_account_email, totp_secret)
    cursor.execute(insert_query, data_to_insert)
    connection.commit()

    cursor.close()
    connection.close()

    # Store the secret in the session for the next step
    session['totp_secret'] = totp_secret

    return True  # Indicate successful account creation
    
def login_master_account(master_account_name, master_account_password):
    connection, cursor = set_connection_cursor()

    # Define your select statement to retrieve user information                                                           
    select_query = """
        SELECT ID_master_account, master_account_password, totp_secret
        FROM account_table
        WHERE master_account_name = %s
    """
    cursor.execute(select_query, (master_account_name,))
    
    # Fetch the result                  
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        ID_master_account, hashed_password, totp_secret = result

        # Verifică parola
        if verify_password(master_account_password, hashed_password):
            session['ID_master_account'] = ID_master_account
            session['master_account_name'] = master_account_name
            session['master_account_password'] = master_account_password  # Salvează parola pentru criptare/decriptare
            session['2fa_authenticated'] = False
            session['totp_secret'] = totp_secret

            if totp_secret:
                return redirect(url_for('verify_2fa'))
            else:
                session['2fa_authenticated'] = True
                return True
        else:
            return False  # Parola incorectă
                                                       
    else:
        return False  # Utilizatorul nu a fost găsit

def modify_master_password(master_account_name, current_password, new_password):
    connection, cursor = set_connection_cursor()

    # Selectează hash-ul actual al parolei
    select_query = "SELECT master_account_password FROM account_table WHERE master_account_name = %s"
    cursor.execute(select_query, (master_account_name,))
    result = cursor.fetchone()

    if result and verify_password(current_password, result[0]):
        # Hash nou pentru parola
        new_hashed_password = hash_password(new_password)

        update_query = "UPDATE account_table SET master_account_password = %s WHERE master_account_name = %s"
        cursor.execute(update_query, (new_hashed_password, master_account_name))
        connection.commit()
        cursor.close()
        connection.close()
        return True  # Actualizare reușită
    else:
        cursor.close()
        connection.close()
        return False  # Parola actuală este incorectă

def get_credentials_by_site_name(site_name):
    # Use existing set_connection_cursor function to get connection and cursor
    connection, cursor = set_connection_cursor()
    
    # Define the SQL query to get the account details by site_name
    query = "SELECT email, account_name, password, details FROM password_management_table WHERE site_name = %s"
    
    # Execute the query with the provided site name
    cursor.execute(query, (site_name,))
    
    # Fetch the first matching result, if any
    credentials = cursor.fetchone()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    return credentials

#end of new functions
    
def update_table_entry_by_id(id_to_be_updated, site_name, email, account_name, password, details):
    
    connection,cursor = set_connection_cursor()
    
    # Define your update statement
    update_query = "UPDATE password_management_table SET site_name = %s, email = %s, account_name = %s, password = %s, details = %s WHERE ID_account = %s"
    
    # New values to be updated
    new_values = (str(site_name), str(email), str(account_name), str(password), str(details), int(id_to_be_updated))  
    
    # Execute the update query
    cursor.execute(update_query, new_values)

    # Commit the transaction
    connection.commit()
    
    # Close cursor and connection
    cursor.close()
    connection.close()
       
def delete_table_entry_by_details(site_name, email, account_name, details):
    connection, cursor = set_connection_cursor()
    
    # Define the delete query using multiple fields
    delete_query = """
        DELETE FROM password_management_table
        WHERE site_name = %s AND email = %s AND account_name = %s AND details = %s
    """
    
    # Execute the query with the provided parameters
    cursor.execute(delete_query, (site_name, email, account_name, details))

    # Commit the transaction
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
app.config['SESSION_TYPE'] = 'filesystem'  # Use server-side sessions
Session(app)
CORS(app)

def requires_2fa(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('2fa_authenticated'):
            return redirect(url_for('verify_2fa'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/setup_2fa')
def setup_2fa():
    # Retrieve the TOTP secret from session (set during account creation)
    totp_secret = session.get('totp_secret')
    if not totp_secret:
        return "2FA setup incomplete. Please try again or contact support."
    
    # Generate a TOTP instance and QR code URI
    totp = pyotp.TOTP(totp_secret)
    uri = totp.provisioning_uri("user@example.com", issuer_name="PasswordGenKeep")

    # Generate QR code for the TOTP URI
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf)
    buf.seek(0)

    # Display the QR code
    return send_file(buf, mimetype='image/png')

@app.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    # Check if `totp_secret` exists in the session
    if 'totp_secret' not in session:
        return "2FA setup is missing. Please set up 2FA first.", 400
    if request.method == 'POST':
        otp = request.form.get('otp')
        totp = pyotp.TOTP(session['totp_secret'])
        print("Generated OTP:", totp.now())
        # Verify the OTP entered by the user
        if totp.verify(otp):
            session['2fa_authenticated'] = True
            return redirect(url_for('homepage'))
        else:
            return "Invalid OTP. Please try again."

    # Render the OTP input page if request method is GET
    return render_template('verify_2fa.html')

@app.route('/verify_2fa_change_password', methods=['GET', 'POST'])
def verify_2fa_change_password():
    # Check if `totp_secret` exists in the session
    if 'totp_secret' not in session:
        return "2FA setup is missing. Please set up 2FA first.", 400
    if request.method == 'POST':
        otp = request.form.get('otp')
        totp = pyotp.TOTP(session['totp_secret'])
        print("Generated OTP:", totp.now())
        # Verify the OTP entered by the user
        if totp.verify(otp):
            session['2fa_authenticated'] = True
            return redirect(url_for('/'))
        else:
            return "Invalid OTP. Please try again."

    # Render the OTP input page if request method is GET
    return render_template('verify_2fa.html')

@app.route('/')
def index():
    return render_template('index.html')

# Route to display the account creation form and QR code for 2FA setup
@app.route('/sign_up_master_account', methods=['GET', 'POST'])
def sign_up_master_account():
    if request.method == 'POST':
        # Get the form data
        master_account_name = request.form['master_account_name']
        master_account_password = request.form['master_account_password']
        master_account_email = request.form['master_account_email']
        
        # Create the account in the database (function not shown here)
        # This should return True if the account creation was successful
        account_created = create_master_account(master_account_name, master_account_password, master_account_email)

        if account_created:
            # Generate a TOTP secret for the user and store it in the session
            totp_secret = pyotp.random_base32()
            session['totp_secret'] = totp_secret
            
            # Redirect to show the QR code for 2FA setup
            return redirect(url_for('index'))
        else:
            return "Account creation failed. The username or email is already in use."

    # For GET requests, render the create account form
    return render_template('create_master_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        master_account_name = request.form['master_account_name']
        master_account_password = request.form['master_account_password']
        
        # Attempt to log in with the provided credentials
        login_success = login_master_account(master_account_name, master_account_password)
        
        if login_success == True:
            # If login is successful without 2FA, redirect to index
            return redirect(url_for('index'))
        elif login_success == False:
            # If login fails due to incorrect credentials
            return "Login failed. Incorrect username or password."
        else:
            # If login requires 2FA, login_master_account redirects to /verify_2fa
            return login_success
    
    return render_template('login.html')  # Display the login form for GET requests

@app.route('/homepage')
@requires_2fa
def homepage():
    ID_master_account = session.get('ID_master_account')
    if not ID_master_account:
        return redirect(url_for('login'))  # Redirect to login if not authenticated
    
    # Use the ID for personalized functionality
    return render_template('homepage.html', user_id=ID_master_account)

@app.route('/logout')
def logout():
    session.pop('master_account_password', None)  # Elimină parola master
    session.clear()  # Curăță toate datele sesiunii
    return redirect(url_for('login'))

@app.route('/change_password_master_account', methods=['GET', 'POST'])
def change_password_master_account():
    if request.method == 'POST':
        # Get the email, current password, and new password from the form
        email = request.form['email']
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        # Verify current password (using a function like modify_master_password)
        password_changed = modify_master_password(email, current_password, new_password)
        
        if password_changed:
            # If password is correct, ask for 2FA
            session['2fa_authenticated'] = False  # Reset 2FA authentication
            return redirect(url_for('verify_2fa_change_password'))  # Redirect to 2FA verification
        else:
            return render_template('change_password_master_account.html', error_message="Incorrect current password or the account does not exist.")

    # For GET requests, render the change password form
    return render_template('change_password_master_account.html')

@app.route('/view_table', methods=['GET'])
@requires_2fa
def view_table():
    ID_master_account = session.get('ID_master_account')
    if not ID_master_account:
        return redirect(url_for('login'))

    # Obține datele tabelului
    table_data = show_table(ID_master_account)

    # Fetch the master account password from the database using set_connection_cursor
    connection, cursor = set_connection_cursor()

    query = "SELECT master_account_password FROM account_table WHERE ID_master_account = %s"
    cursor.execute(query, (ID_master_account,))
    result = cursor.fetchone()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    if not result:
        return "Master account not found", 404

    # Access the password from the tuple (the first and only column)
    master_account_password = session.get('master_account_password')

    # Pass the master password and table data to the template
    if verify_password(master_account_password, result[0]):
        return render_template('view_table.html', table_data=table_data, master_account_password=master_account_password)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    # Ensure user is logged in
    ID_master_account = session.get('ID_master_account')
    if not ID_master_account:
        return redirect(url_for('login'))

    if request.method == 'POST':
        site_name = request.form['site_name']
        email = request.form['email']
        account_name = request.form['account_name']
        password = request.form['password']
        details = request.form['details']
        
        # Insert the new entry with the associated ID_master_account
        insert_into_table(site_name, email, account_name, password, details, ID_master_account)
        return redirect(url_for('homepage'))
    
    return render_template('add_entry.html')

@app.route('/modify_entry', methods=['GET', 'POST'])
def modify_entry():
    ID_master_account = session.get('ID_master_account')
    if not ID_master_account:
        return redirect(url_for('login'))
    
    # Use the show_table function to fetch accounts
    data = show_table_for_modify_entry(ID_master_account)

    # Fetch the master password
    connection, cursor = set_connection_cursor()
    query = "SELECT master_account_password FROM account_table WHERE ID_master_account = %s"
    cursor.execute(query, (ID_master_account,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if not result:
        return "Master account not found", 404

    master_account_password = session.get('master_account_password')  

    # Handle POST request
    if request.method == 'POST':
        id_account = int(request.form['id_account'])
        site_name = request.form['site_name']
        email = request.form['email']
        account_name = request.form['account_name']
        password = request.form['password']
        details = request.form['details']
        encrypted_password = encrypt_password(master_account_password, password)
        # Update the entry with the new values
        update_table_entry_by_id(id_account, site_name, email, account_name, encrypted_password, details)
        return redirect(url_for('homepage'))
    
    # Return a response for the 'GET' method
    if verify_password(master_account_password, result[0]):
        return render_template('modify_entry.html', table_data=data, master_account_password=master_account_password)

@app.route('/delete_entry', methods=['GET', 'POST'])
def delete_entry():
    ID_master_account = session.get('ID_master_account')
    if not ID_master_account:
        return redirect(url_for('login'))
    
    # Fetch table data for the current master account
    data = show_table(ID_master_account)

    # Fetch the master password for the account
    connection, cursor = set_connection_cursor()
    query = "SELECT master_account_password FROM account_table WHERE ID_master_account = %s"
    cursor.execute(query, (ID_master_account,))
    result = cursor.fetchone()
    connection.close()

    if result:
        master_account_password = session.get('master_account_password')
    else:
        master_account_password = ""

    if request.method == 'POST':
        # Handle deletion logic as before
        num_entries = len(data)
        for i in range(num_entries):
            if f'delete_{i}' in request.form:
                site_name = request.form.get(f'site_name_{i}')
                email = request.form.get(f'email_{i}')
                account_name = request.form.get(f'account_name_{i}')
                details = request.form.get(f'details_{i}')
                delete_table_entry_by_details(site_name, email, account_name, details)

        return redirect(url_for('homepage'))

    # Render the delete page for GET requests
    if verify_password(master_account_password, result[0]):
        return render_template('delete_entry.html', table_data=data, master_account_password=master_account_password)

@app.route('/pw_gen', methods=['GET', 'POST'])
def pw_gen():
    if request.method == 'POST':
        length = int(request.form.get('length', 8))
        include_lowercase = 'lowercase' in request.form
        include_uppercase = 'uppercase' in request.form
        include_numbers = 'numbers' in request.form
        include_special = 'special' in request.form
        
        generated_password = generate_password(length, include_lowercase, include_uppercase, include_numbers, include_special)
        return jsonify({"generated_password": generated_password})
    
    return render_template('pw_gen.html')

@app.route('/check-password', methods=['GET'])
def check_password():
    password_input = request.args.get('password', '')
    if not password_input:
        return jsonify({"result": "Error: No password provided"}), 400  # Return HTTP 400 if no password
    result = check_password_strength(password_input)
    return jsonify({"result": result})

@app.route('/get_credentials', methods=['GET'])
def get_credentials():
    # Get the domain (site name) from the request, sent by the extension
    domain = request.args.get('domain')
    
    # Fetch credentials from the database based on the site name
    credentials = get_credentials_by_site_name(domain)
    
    # If credentials exist, return them in JSON format
    if credentials:
        # credentials will be in the form (email, account_name, password)
        return jsonify({
            "email": credentials[0],
            "account_name": credentials[1],
            "password": credentials[2]
        })
    else:
        return jsonify({"error": "No credentials found"}), 404

@app.route('/save_credentials', methods=['POST'])
def save_credentials():
    data = request.json
    site_name = data.get('site_name')
    email = data.get('email')
    account_name = data.get('account_name')
    password = data.get('password')

    if not site_name or not email or not account_name or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        connection, cursor = set_connection_cursor()
        insert_query = """
            INSERT INTO password_management_table (site_name, email, account_name, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (site_name, email, account_name, password))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True})
    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "Database error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
