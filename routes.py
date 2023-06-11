from app import app, db, bcrypt
from flask import request, render_template, redirect, url_for, session
from check_validate import *
from models import Users, Products
from validate_email import validate_email


@app.route('/', methods=['GET', 'POST'])                                # страница для неавторизованных пользователей
def main_page():
    products_amount = str(db.engine.execute("SELECT COUNT(product_name) FROM products").all())
    amount = int("".join(i for i in products_amount if i.isdigit()))
    products_identifiers = db.engine.execute("SELECT product_identifier FROM products").all()
    pid = []
    for i in range(len(products_identifiers)):
        value = str(products_identifiers[i])
        element = "".join(i for i in value if i.isdigit())
        pid.append(element)
    products_names = db.engine.execute("SELECT product_name FROM products").all()
    names = []
    for i in range(len(products_names)):
        value = str(products_names[i])
        element = "".join(i for i in value if (i.isdigit() or i.isalpha() or i == ' '))
        names.append(element)
    products_prices = db.engine.execute("SELECT product_price FROM products").all()
    prices = []
    for i in range(len(products_prices)):
        value = str(products_prices[i])
        element = "".join(i for i in value if i.isdigit())
        prices.append(element)
    products_descriptions = db.engine.execute("SELECT product_description FROM products").all()
    descriptions = []
    for i in range(len(products_descriptions)):
        value = str(products_descriptions[i])
        element = "".join(i for i in value if i.isdigit() or i.isalpha() or i == ' ')
        descriptions.append(element)
    return render_template('main_page.html', amount=amount, names=names, prices=prices, descriptions=descriptions, pid=pid)


@app.route('/registration', methods=['GET', 'POST'])                    # страница регистрации
def registration():
    result = ''
    if "user" in session:                                            # перенаправление, если пользователь авторизован
        return redirect(url_for("authorized_user"))
    if "admin" in session:
        return redirect(url_for("admin"))
    if request.method == 'POST':
        email = request.form['email']                                   # получение данных из формы
        login = request.form['login']
        password = request.form['password']
        confirm_password = request.form['conf_password']
        if confirm_password == password:
            if validate_email(email) and validate_login(login) and validate_password(password):     # проверка на валидность введенных данных
                user = Users(email=request.form['email'],
                             login=request.form['login'],
                             password=bcrypt.generate_password_hash(password))  # хэширование пароля
                user_test_email = Users.query.filter_by(email=user.email).first()  # проверка на наличие зарегистрированного пользователя
                user_test_login = Users.query.filter_by(login=user.login).first()
                if user_test_email is None and user_test_login is None:
                    db.session.add(user)                                            # добавление польлзователя в таблицу
                    db.session.commit()
                    return redirect(url_for("auth"))                                # перенаправление на аутентификацию
                else:
                    result = 'There is a user with this login/email.'               # ошибки при вводе данных
            else:
                result = 'Something went wrong! Check all forms.'
        else:
            result = 'Check passwords.'
    return render_template('/registration.html', result=result)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    result = ""
    if "user" in session:
        return redirect(url_for("authorized_user"))
    if "admin" in session:
        return redirect(url_for("admin"))
    if request.method == "POST":
        login = request.form["login"]
        user_test_login = Users.query.filter_by(login=login).first()
        if user_test_login is not None:
            user_test_password = bcrypt.check_password_hash(user_test_login.password, request.form["password"])
        else:
            user_test_password = False
        if user_test_login is None:
            result = "There is no user with this login."
        elif user_test_password is False:
            result = "Incorrect password."
        else:
            with app.app_context():
                res_id = str(db.engine.execute(f"SELECT identifier FROM users WHERE login is '{login}';").all())
            uid = int("".join(i for i in res_id if i.isdigit()))
            print(uid)
            if login != 'admin':
                session["user"] = login
                return redirect(url_for('authorized_user'))
            if login == 'admin':
                session["admin"] = login
                return redirect(url_for('admin'))
    return render_template("/auth.html", result=result)


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    return render_template('admin_panel.html')


@app.route('/admin/add/', methods=['GET', 'POST'])
def admin_add():
    if "admin" in session:
        add_result = ''
        if request.method == 'POST':
            product_type = request.form["product_type"]
            product_name = request.form["product_name"]
            product_description = request.form["product_description"]
            product_brand = request.form["product_brand"]
            product_price_input = request.form["product_price"]
            product_price = int(product_price_input)
            if product_type == "":
                add_result = 'Неверно указан тип продукта.'
            elif product_name == "":
                add_result = 'Неверно указано наименование продукта.'
            elif product_description == "":
                add_result = 'Неверно указано краткое описание продукта.'
            elif product_brand == "":
                add_result = 'Неверно указан производитель продукта.'
            elif product_price <= 0:
                add_result = 'Неверно указана цена продукта.'
            else:
                product = Products(product_type=request.form["product_type"],
                                   product_name=request.form["product_name"],
                                   product_description=request.form["product_description"],
                                   product_brand=request.form["product_brand"],
                                   product_price=request.form["product_price"])
                product_test_name = Products.query.filter_by(product_name=product.product_name).first()
                if product_test_name is None:
                    db.session.add(product)
                    db.session.commit()
                    add_result = 'Товар был успешно добавлен'
                    return render_template('/add_new_product.html', add_result=add_result)
                else:
                    add_result = 'Товар с таким названием уже существует.'
        return render_template('/add_new_product.html', add_result=add_result)
    else:
        return redirect(url_for('auth'))


@app.route('/admin/delete/', methods=['GET', 'POST'])
def admin_delete():
    symbol = ';'
    if "admin" in session:
        add_result = ''
        if request.method == 'POST':
            product_name = request.form["product_name"]
            if product_name == "":
                add_result = 'Incorrect name of the product.'
            elif symbol in product_name:                                # experiment
                add_result = "Incorrect name of the product."
            else:
                product = Products(product_name=request.form["product_name"])
                product_test_name = Products.query.filter_by(product_name=product.product_name).first()
                if product_test_name is None:
                    add_result = 'There is no products with this name.'
                    return render_template('/delete_product.html', add_result=add_result)
                else:
                    db.engine.execute(f"DELETE FROM products WHERE product_name = '{product_name}'")
                    add_result = 'The product has been deleted.'
        return render_template('/delete_product.html', add_result=add_result)
    else:
        return redirect(url_for('auth'))


@app.route('/admin/edit/', methods=['GET', 'POST'])
def admin_edit():
    symbol = ';'
    if "admin" in session:
        add_result = ''
        if request.method == 'POST':
            product_name = request.form["product_name"]
            if product_name == "":
                add_result = 'Incorrect name of the product.'
            elif symbol in product_name:  # experiment
                add_result = "Incorrect name of the product."
            else:
                product = Products(product_name=request.form["product_name"])
                product_test_name = Products.query.filter_by(product_name=product.product_name).first()
                if product_test_name is None:
                    add_result = 'There is no products with this name.'
                    return render_template('/delete_product.html', add_result=add_result)
                else:
                    product_type = request.form["product_type"]
                    product_description = request.form["product_description"]
                    product_brand = request.form["product_brand"]
                    product_price_input = request.form["product_price"]
                    product_price = int(product_price_input)
                    if product_type == "":
                        add_result = 'Неверно указан тип продукта.'
                    elif product_description == "":
                        add_result = 'Неверно указано краткое описание продукта.'
                    elif product_brand == "":
                        add_result = 'Неверно указан производитель продукта.'
                    elif product_price <= 0:
                        add_result = 'Неверно указана цена продукта.'
                    else:
                        db.engine.execute(
                            f"UPDATE products SET product_type = '{product_type}' WHERE product_name = '{product_name}'")
                        db.engine.execute(
                            f"UPDATE products SET product_description = '{product_description}' WHERE product_name = '{product_name}'")
                        db.engine.execute(
                            f"UPDATE products SET product_brand = '{product_brand}' WHERE product_name = '{product_name}'")
                        db.engine.execute(
                            f"UPDATE products SET product_price = '{product_price}' WHERE product_name = '{product_name}'")
                        add_result = 'The product has been edited.'
                        return render_template('/edit_product.html', add_result=add_result)
        return render_template('/edit_product.html', add_result=add_result)
    else:
        return redirect(url_for('auth'))


@app.route('/authorized_user/', methods=['GET', 'POST'])
def authorized_user():
    if "user" in session:
        return render_template('/main_page_for_authorized_users.html')
    else:
        return redirect(url_for('auth'))


@app.route('/logout/')
def logout():
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for("main_page"))
    if "admin" in session:
        session.pop("admin", None)
        return redirect(url_for("main_page"))


@app.route('/cards/<pid>')
def cards(pid):
    pr_type = db.engine.execute(f"SELECT product_type FROM products WHERE product_identifier = '{int(pid)}';").all()
    type_product = "".join(i for i in str(pr_type) if i.isalpha() or i == ' ')
    pr_name = db.engine.execute(f"SELECT product_name FROM products WHERE product_identifier = '{int(pid)}';").all()
    name_product = "".join(i for i in str(pr_name) if i.isalpha() or i == ' ' or i.isdigit())
    pr_description = db.engine.execute(f"SELECT product_description FROM products WHERE product_identifier = '{int(pid)}';").all()
    description_product = "".join(i for i in str(pr_description) if i.isalpha() or i == ' ')
    pr_price = db.engine.execute(f"SELECT product_price FROM products WHERE product_identifier = '{int(pid)}';").all()
    price_product = "".join(i for i in str(pr_price) if i.isdigit() or i == ' ')
    return render_template('/card.html', pid=pid, type_product=type_product, name_product=name_product,
                           description_product=description_product, price_product=price_product)
