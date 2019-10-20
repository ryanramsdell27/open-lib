from flask import Flask, render_template
from register_item import register_item
import utils
import populate_db

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", current='home')
    
@app.route("/about")
def about():
    return render_template("about.html", current='about')

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", books=utils.get_books(), current='catalog')
    
if __name__ == "__main__":
    populate_db.populate_db()
    app.run(debug=True)