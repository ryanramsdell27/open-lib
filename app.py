from flask import Flask, render_template, request, make_response, redirect, url_for
from pymongo import MongoClient
import utils, jwt
import register_user, register_item, events, pprint

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

    return render_template("catalog.html", books=utils.get_catalog_items(), current='catalog')

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

    return render_template("pending.html", current='pending')

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

@app.route("/unregister-item")
def unregisterItem():
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

    owner = register_user.get_user_id(decoded['email'])
    pprint.pprint(owner)
    catalog_item = utils.get_catalog_item(isbn, owner)
    pprint.pprint(catalog_item)

    register_item.deregister_item(catalog_item['_id'])

    return redirect('/items')

@app.route("/verify")
def verifyTransaction():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    code = request.args.get("code")
    if code == None:
        return redirect('/pending')

    code_recipient = register_user.get_user_id(decoded['email'])

    transaction = utils.get_pending_transaction(code_recipient)

    pprint.pprint(transaction)
    print(code)

    # if (code == transaction['verification_code']):
    #     print("VALIDATED")
    # else:
    #     print("NOT VALID")

    events.event_transaction(transaction['event_token'])
    

    return redirect('/items')

@app.route("/cancel")
def cancelTransaction():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    return redirect('/pending')

@app.route("/request")
def requestItem():
    if request.cookies.get('TOKEN') == None:
        return redirect('/register')
    decoded = jwt.decode(request.cookies.get('TOKEN'), 'secret', algorithms=['HS256'])
    if decoded == None:
        resp = make_response(redirect('/register'))
        resp.set_cookie('TOKEN', '', expires=0)
        return resp

    isbn = request.args.get("isbn")
    owner = request.args.get("owner")
    if isbn == None or owner == None:
        return redirect('/')

    events.event_request(register_user.get_user_id(owner), utils.get_book(isbn)['_id'])

    return redirect('/pending')

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
    app.run(debug=True)