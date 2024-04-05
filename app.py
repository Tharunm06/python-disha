from flask import Flask, request, redirect, session, render_template
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to check if user is logged in
def is_logged_in():
    return 'guard_id' in session

@app.route('/', methods=['GET', 'POST'])
def guard_login():
    error_message = None

    if request.method == 'POST':
        guard_id = request.form['guard-id']
        password = request.form['password']

        connection = pymysql.connect(host='database-v-db.cto2s4800gfa.us-east-1.rds.amazonaws.com',
                                     user='admin',
                                     password='panodisha',
                                     database='disha_db',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM tbl_user WHERE user_name = %s AND password = %s"
                cursor.execute(sql, (guard_id, password))
                result = cursor.fetchone()
                if result:
                    session['guard_id'] = guard_id
                    return redirect('/dashboard')
                else:
                    error_message = "Invalid credentials"
        except Exception as e:
            error_message = str(e)
        finally:
            connection.close()

    return render_template('index.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
    if is_logged_in():
        return render_template('register.html', success_message=session.pop('success_message', None))
    else:
        return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/save_data', methods=['POST'])
def save_data():
    if request.method == 'POST':
        name = request.form['name']
        mobile_number = request.form['mobileNumber']
        purpose = request.form['purpose']
        vehicle_number = request.form['VehicleNumber']

        # Connect to the database
        connection = pymysql.connect(host='database-v-db.cto2s4800gfa.us-east-1.rds.amazonaws.com',
                                     user='admin',
                                     password='panodisha',
                                     database='disha_db',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # SQL query to insert data into the visitors table
                sql = "INSERT INTO visitors (name, mobilenumber, purpose, licenceplate, status, datetime) VALUES (%s, %s, %s, %s, %s, NOW())"
                cursor.execute(sql, (name, mobile_number, purpose, vehicle_number, 1))
            connection.commit()
            session['success_message'] = "Data saved successfully!"
            return redirect('/dashboard')
        except Exception as e:
            return str(e)
        finally:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
