from flask import Flask, render_template, request, make_response, redirect, url_for
from pymongo import MongoClient
import utils, jwt
import register_user, register_item
import populate_db

app = Flask(__name__)

@app.route("/")
def catalog():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    return render_template("catalog.html", books=utils.get_books(), current='catalog')

@app.route("/items")
def items():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    return render_template("items.html", current='items', books=utils.get_user_items(register_user.get_user_id(decoded['email'])))

@app.route("/pending")
def pending():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    return render_template("pending.html", pending_transactions=utils.get_pending_transactions(), current='pending')

@app.route("/register-item")
def registerItem():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    isbn = request.args.get("isbn")
    if isbn == None:
        return redirect('/items')

    register_item.register_item(isbn, register_user.get_user_id(decoded['email']))

    return redirect('/items')

@app.route("/register")
def register():
    name = request.args.get("name")
    email = request.args.get("email")
    phone = request.args.get("phone")

    if name != None and email != None and phone != None:
        user_id = register_user.register_user(name, email, phone)

        if user_id == None:
            return render_template("register.html", current='register')

        resp = make_response(redirect('/'))
        resp.set_cookie("TOKEN", jwt.encode({'name': name, 'email': email, 'phone': phone}, 'secret', algorithm='HS256'))
        return resp

    return render_template("register.html", current='register')
    
if __name__ == "__main__":
    populate_db.populate_db()
    app.run(debug=True)