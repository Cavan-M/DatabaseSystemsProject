# Written with Love and Care by Cavan McLellan
# This python file is very large and may be difficult to grade
# I would recommend reviewing the Database class on line 15 for a solid grasp of the database concepts used

import pymysql
from flask import Flask, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from math import ceil as round_up
from flask_session import Session
import datetime
import hashlib
import random

hostname = 'database-2.cuea2qn2hugv.us-east-1.rds.amazonaws.com'
usr = ''
passwd = ''
db = 'licensestore'
db_port = 3306


class Database:
    def __init__(self, host, username, password, database, port):
        self.host = host
        self.user = username
        self.__password = password
        self.db = database
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.__password, db=self.db, port=self.port, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        return True

    def disconnect(self):
        self.connection.close()
        return True

    def insert(self, table, **kwargs):
        # Usage: self.insert(TABLE_NAME, ATTR=VAL, ATTR2=VAL2, ..., ATTRx=VALx)
        if self.connect():
            table_string = 'insert into ' + table
            key_string = ' ('
            value_string = ' values ('
            for key, value in kwargs.items():
                key_string = key_string + key + ', '
                value_string = value_string + str(value) + ', '
            key_string = key_string[:-2] + ')'
            value_string = value_string[:-2] + ')'
            exec_string = table_string + key_string + value_string
            print(exec_string)
            self.cursor.execute(exec_string)
            self.connection.commit()
            self.disconnect()

    def get_user(self, email):
        if self.connect():
            selection = "SELECT * FROM licensestore.customers WHERE email='" + email + "';"
            self.cursor.execute(selection)
            self.disconnect()
            results = []
            for row in self.cursor:
                results.append(row)
            return results

    def get_staff(self, email):
        if self.connect():
            selection = "SELECT * FROM licensestore.staff WHERE email='" + email + "';"
            self.cursor.execute(selection)
            self.disconnect()
            results = []
            for row in self.cursor:
                results.append(row)
            return results

    def get_all_packages(self, page=0):
        if self.connect():
            selection = "SELECT * FROM licensestore.packages LIMIT " + str(page * 6) + ", 6;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            selection = "SELECT COUNT(*) as pgkCount from packages;"
            self.cursor.execute(selection)
            page_count = 0
            for row in self.cursor:
                page_count = row["pgkCount"]
            page_count = round_up(page_count / 6)
            self.disconnect()
            return results, page_count

    def get_features(self, package):
        if self.connect():
            selection = "SELECT * FROM licensestore.features WHERE features.package=" + package + ";"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row['feature'])
            self.disconnect()
            return results

    def get_single_package(self, package):
        if self.connect():
            selection = 'SELECT * FROM licensestore.packages WHERE packages.ID=' + package + ";"
            self.cursor.execute(selection)
            results = {}
            for row in self.cursor:
                results = row
            self.disconnect()
            return results

    def place_order(self, total, customer, packages):
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        date_string = "'" + date + "'"
        customer_string = "'" + customer + "'"
        id = 0

        self.insert('orders', total=total, date=date_string, customer=customer_string)
        try:
            if self.connect():
                self.cursor.execute('SELECT MAX(orders.id) as last FROM licensestore.orders;')
                for row in self.cursor:
                    id = row['last']
                self.disconnect()
        except IndexError:
            id = 1000
        for package in packages:
            self.insert('order_packages', ordr=id, package=int(package['ID']))

    def create_license(self, pkgID, ownr, period=30):
        now = datetime.datetime.now()
        expiry_d = now + datetime.timedelta(days=period)
        expiry_date = "'" + expiry_d.strftime('%Y-%m-%d') + "'"
        keycursor = now.strftime('%Y-%m-%d %H:%M:%S') + str(random.randint(100, 199))
        key = hashlib.md5(keycursor.encode())
        key_string = "'" + str(key.hexdigest()) + "'"
        owner_string = "'" + str(ownr) + "'"
        self.insert('licenses', lkey=key_string, expiry=expiry_date, package=pkgID, owner=owner_string)

    def get_licenses(self, user):
        if self.connect():
            user_string = "'" + user + "'"
            selection = "SELECT lkey, expiry, packages.name, cost FROM licenses JOIN packages on licenses.package=packages.ID WHERE licenses.owner=" + user_string + ";"
            print(selection)
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()
            return results

    def user_exists(self, user):
        if self.connect():
            user_string = "'" + user + "'"
            selection = "SELECT * FROM customers WHERE customers.email=" + user_string + ";"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            if len(results) > 0:
                return True
            else:
                selection = "SELECT * FROM staff WHERE email=" + user_string + ";"
                self.cursor.execute(selection)
                for row in self.cursor:
                    results.append(row)
                    if len(results) > 0:
                        return True
                    else:
                        return False

    def get_latest_orders(self):
        if self.connect():
            selection = "SELECT * FROM orders JOIN order_packages on ordr=orders.id join packages on package=packages.ID ORDER BY date desc LIMIT 50;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()
            return results

    def get_orders_by_user(self, email):
        if self.connect():
            selection = "SELECT * FROM orders JOIN order_packages on ordr=orders.id join packages on package=packages.ID WHERE customer like '" + email + "%' ORDER BY date desc;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()
            return results

    def get_random_keys(self):
        if self.connect():
            selection = "SELECT lkey, expiry, name, email, firstname, lastname FROM licenses JOIN packages on licenses.package=packages.ID JOIN customers on email=owner ORDER BY expiry desc LIMIT 50;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()
            return results

    def get_keys_by_user(self, email):
        if self.connect():
            selection = "SELECT lkey, expiry, name, email, firstname, lastname FROM licenses JOIN packages on licenses.package=packages.ID JOIN customers on email=owner WHERE email like '" + email + "%';"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()
            return results

    def add_user(self, email, password, firstname, lastname):
        email_string = "'" + email + "'"
        password_string = "'" + password + "'"
        firstname_string = "'" + firstname + "'"
        lastname_string = "'" + lastname + "'"
        self.insert("customers", email=email_string, password=password_string, firstname=firstname_string, lastname=lastname_string)

    def create_staff(self, email, password, firstname, lastname):
        email_string = "'" + email + "'"
        password_string = "'" + password + "'"
        firstname_string = "'" + firstname + "'"
        lastname_string = "'" + lastname + "'"
        self.insert("staff", email=email_string, password=password_string, firstname=firstname_string, lastname=lastname_string)

    def get_orders(self, user):
        user_string = "'" + user + "'"
        selection = "select orders.id, orders.date, total, packages.name from orders join order_packages on orders.id=order_packages.ordr join packages on order_packages.package=packages.ID WHERE customer=" + user_string + ";"
        if self.connect():
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            self.disconnect()

            return results
        else:
            return []

    def remove_key(self, lkey, staff):
        self.audit_revocation(lkey, staff)
        key_string = "'" + lkey + "'"
        query = "DELETE FROM licenses WHERE lkey=" + key_string + ";"
        self.connect()
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()

    def audit_revocation(self, lkey, staff):
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        staff_string = "'" + staff + "'"
        key_string = "'" + lkey + "'"
        date_string = "'" + date + "'"
        self.connect()
        selection = "SELECT package, owner FROM licenses WHERE lkey=" + key_string + ";"
        self.cursor.execute(selection)
        package = 0
        owner = ""
        for row in self.cursor:
            package = row['package']
            owner = row['owner']
        owner_string = "'" + owner + "'"
        self.insert("revocations", lkey=key_string, staff=staff_string, date=date_string, package=package, customer=owner_string)


    def refund_order(self, ordernum, staff):
        query = "DELETE FROM orders WHERE id=" + ordernum + ";"
        self.audit_refund(ordernum, staff)
        self.connect()
        self.cursor.execute(query)
        self.connection.commit()
        self.disconnect()

    def audit_refund(self, order_id, staff):
        staff_string = "'" + staff + "'"
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        date_string = "'" + date + "'"
        self.connect()
        selection = "SELECT customer, total FROM orders WHERE id=" + order_id + ";"
        self.cursor.execute(selection)
        customer = ''
        total = 0
        for row in self.cursor:
            customer = row['customer']
            total = row['total']
        customer_string = "'" + customer + "'"
        self.insert('refunds', orderid=order_id, staff=staff_string, date=date_string, total=total, customer=customer_string)

    def get_revocations(self):
        if self.connect():
            selection = "SELECT * from revocations ORDER BY date desc LIMIT 50;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            return results

    def get_refunds(self):
        if self.connect():
            selection = "SELECT * from refunds ORDER BY date desc LIMIT 50;"
            self.cursor.execute(selection)
            results = []
            for row in self.cursor:
                results.append(row)
            return results


class User:
    def __init__(self, database, email, is_staff=False):
        if is_staff:
            self.usr = database.get_staff(email)[0]
        else:
            self.usr = database.get_user(email)[0]
        self.name = self.usr['firstname']
        self.surname = self.usr['lastname']
        self.email = self.usr['email']
        self.password = self.usr['password']
        self.staff = is_staff

    def to_json(self):
        return self.usr

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email


app_db = Database(hostname, usr, passwd, db, db_port)
app = Flask(__name__, template_folder='static')
app.secret_key = "HJdgb8u9NyA5KrhLZyKkwyNqAt39shVU"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(em):
    try:
        u = User(app_db, em, False)
    except IndexError:
        u = User(app_db, em, True)
    return u


@app.route('/')
def homepage():
    if current_user.is_authenticated:
        return render_template('html/index.html', loggedin=True, name=current_user.name, surname=current_user.surname)
    else:
        return render_template('html/index.html', loggedin=False)


@app.route('/staff')
def staff_homepage():
    if current_user.is_authenticated and current_user.staff:
        return render_template('html/staff.html', loggedin=True, name=current_user.name, surname=current_user.surname)
    else:
        return render_template('html/staff.html', loggedin=False)


@app.route('/stafflogin', methods=['POST'])
def staff_login():
    data = request.form
    u = data['email']
    p = data['password']
    r = app_db.get_staff(u)
    dbpass = r[0]['password']
    dbuser = r[0]['email']
    print(dbpass, p)
    try:
        if dbpass == p:
            u = User(app_db, dbuser, True)
            login_user(u, remember=True)
            return redirect('/staff')
        else:
            flash('Incorrect Username or Password, Check your spelling and try again')
            return render_template('html/staff.html', login=True)
    except IndexError:
        flash('Incorrect Username or Password,xx Check your spelling and try again')
        return render_template('html/staff.html', login=True)


@app.route('/addstaff', methods=['POST'])
@login_required
def add_staff():
    if current_user.staff:
        data = request.form
        u = data['email']
        p = data['password']
        fname = data['firstname']
        lname = data['lastname']
        if app_db.user_exists(u):
            flash("Looks like you've already made an account with us, please sign in below")
            return render_template('html/staff.html', login=True, loggedin=True, name=current_user.name, surname=current_user.surname)
        else:
            app_db.create_staff(u, p, fname, lname)
            return render_template('html/staff.html', login=True, newUser=True, loggedin=True, name=current_user.name, surname=current_user.surname)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    u = data['email']
    p = data['password']
    fname = data['firstname']
    lname = data['lastname']
    if app_db.user_exists(u):
        flash("Looks like you've already made an account with us, please sign in below")
        return render_template('html/index.html', login=True)
    else:
        app_db.add_user(u, p, fname, lname)
        return render_template('html/index.html', login=True, newUser=True)


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    u = data['email']
    p = data['password']
    r = app_db.get_user(u)
    try:
        if r[0]['password'] == p:
            u = User(app_db, r[0]['email'])
            login_user(u, remember=True)
            return redirect('/')
        else:
            flash('Incorrect Username or Password, Check your spelling and try again')
            return render_template('html/index.html', login=True)
    except IndexError:
        flash('Incorrect Username or Password, Check your spelling and try again')
        return render_template('html/index.html', login=True)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session['cart'] = []
    return redirect('/')


@app.route('/profile')
@login_required
def profile():
    return render_template('html/test.html', name=current_user.name)


@app.route('/store')
def store():
    page = 0
    try:
        page = int(request.args.get('page'))
    except TypeError:
        page = 0
    finally:
        packages, page_count = app_db.get_all_packages(page)

    features = []
    for pkg in packages:
        features.append({'ID': pkg['ID'], 'feature': app_db.get_features(str(pkg['ID']))})

    if current_user.is_authenticated:
        try:
            total = round(sum(float(cart_item['cost']) for cart_item in session['cart']), 2)
        except KeyError:
            session['cart'] = []
            total = 0.00
        return render_template('html/store.html', loggedin=True, name=current_user.name, surname=current_user.surname, packages=packages, pageCount=page_count, features=features, currentpage=page,
                               cart=session['cart'], total=total, showcart=request.args.get('showcart'))
    else:
        return render_template('html/store.html', loggedin=False, packages=packages, pageCount=page_count, features=features, currentpage=page)


@app.route('/order')
def order():
    if current_user.is_authenticated:
        try:
            session['cart'].append(app_db.get_single_package(str(request.args.get('id'))))
        except KeyError:
            session['cart'] = []
            session['cart'].append(app_db.get_single_package(str(request.args.get('id'))))

        return redirect('/store')
    else:
        return render_template('html/index.html', login=True)


@app.route('/removefromcart')
@login_required
def remove_cart_item():
    for item in range(len(session['cart'])):
        if session['cart'][item]['ID'] == int(request.args.get('id')):
            session['cart'].pop(item)
            break
    return redirect('/store?showcart=1')


@app.route('/placeorder')
@login_required
def place_order():
    total = round(sum(float(cart_item['cost']) for cart_item in session['cart']), 2)
    print(session['cart'])
    app_db.place_order(total, current_user.email, session['cart'])
    for i in session['cart']:
        frequency = i['period']
        usr_id = i['ID']
        pay_period = 0
        if frequency[-1] == 'm':
            pay_period = int(frequency[:-1]) * 31
        elif frequency[-1] == 'y':
            pay_period = int(frequency[:-1]) * 365
        elif frequency[-1] == 't':
            pay_period = 36525
        elif frequency[-1] == 'w':
            pay_period = int(frequency[:-1]) * 7

        app_db.create_license(usr_id, current_user.email, pay_period)
    session['cart'] = []
    return redirect('/keys')


@app.route('/keys')
@login_required
def user_keys():
    keys = app_db.get_licenses(current_user.email)
    return render_template('html/keys.html', loggedin=True, name=current_user.name, surname=current_user.surname, keys=keys)


@app.route('/user_orders')
@login_required
def user_orders():
    orders = app_db.get_orders(current_user.email)
    try:
        cur = orders[0]['id']
        order_fmt = [{'id': orders[0]['id'], 'date': orders[0]['date'], 'total': orders[0]['total'], 'names': []}]
        ind = 0
        for item in range(len(orders)):
            if orders[item]['id'] == cur:
                order_fmt[ind]['names'].append(orders[item]['name'])
            else:
                ind += 1
                cur = orders[item]['id']
                order_fmt.append({'id': orders[item]['id'], 'date': orders[item]['date'], 'total': orders[item]['total'], 'names': [orders[item]['name']]})
    except IndexError:
        return render_template('html/orders.html', loggedin=True, name=current_user.name, surname=current_user.surname)

    return render_template('html/orders.html', loggedin=True, name=current_user.name, surname=current_user.surname, orders=order_fmt)


@app.route('/managekeys')
@login_required
def manage_keys():
    if current_user.staff:
        query = str(request.args.get('q'))
        if query != 'None':
            keys = app_db.get_keys_by_user(query)
        else:
            keys = app_db.get_random_keys()
        return render_template('html/managekeys.html', loggedin=True, name=current_user.name, surname=current_user.surname, keys=keys)
    else:
        return redirect('/')


@app.route('/removekey')
@login_required
def remove_user_license():
    if current_user.staff:
        q = str(request.args.get('key'))
        app_db.remove_key(q, current_user.email)
        return redirect('/managekeys')


@app.route('/refund')
@login_required
def refund():
    if current_user.staff:
        q = str(request.args.get('order'))
        app_db.refund_order(q, current_user.email)
        return redirect('/manageorders')


@app.route('/manageorders')
@login_required
def manage_licenses():
    if current_user.staff:
        query = str(request.args.get('q'))
        if query != 'None':
            orders = app_db.get_orders_by_user(query)
        else:
            orders = app_db.get_latest_orders()
        try:
            cur = orders[0]['id']
            order_fmt = [{'id': orders[0]['id'], 'customer': orders[0]['customer'], 'date': orders[0]['date'], 'total': orders[0]['total'], 'names': []}]
            ind = 0
            for item in range(len(orders)):
                if orders[item]['id'] == cur:
                    order_fmt[ind]['names'].append(orders[item]['name'])
                else:
                    ind += 1
                    cur = orders[item]['id']
                    order_fmt.append({'id': orders[item]['id'], 'customer': orders[item]['customer'], 'date': orders[item]['date'], 'total': orders[item]['total'], 'names': [orders[item]['name']]})
        except IndexError:
            return render_template('html/manageorders.html', loggedin=True, name=current_user.name, surname=current_user.surname)

        return render_template('html/manageorders.html', loggedin=True, name=current_user.name, surname=current_user.surname, orders=order_fmt)
    else:
        return redirect('/')


@app.route('/log')
@login_required
def get_log():
    if current_user.staff:
        revocations = app_db.get_revocations()
        refunds = app_db.get_refunds()
        return render_template('html/log.html', loggedin=True, name=current_user.name, surname=current_user.surname, revocations=revocations, refunds=refunds)
    else:
        return redirect("/")


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')
