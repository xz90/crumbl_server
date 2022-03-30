from flask import Flask, g, request
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('./data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    #Check if DB is there
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

#close the connection to the database automatically
@app.teardown_appcontext
def close_db(error):
    #if global object has a sqlite database then close it. If u leave it open noone can access it and gets lost in memory causing leaks.
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()


@app.route('/')
def viewusers():
    db = get_db()
    if 'name' in request.args:
      name = request.args['name']
      query1 = "SELECT trackers.name, categories.name as 'category' FROM trackers, categories WHERE trackers.category_id = categories.id and trackers.name = {n}".format(n = name)
      cursor = db.execute(query1)
      results = cursor.fetchall()
      category = results[0]['category']
      return HELLO_HTML.format(name, category)
    else:
      return "<p>Hello World</p>"

HELLO_HTML = """
  <html><body>
    <h1>Hello, {0}!</h1>
    Your category is {1}.
  </body></html>"""

if __name__ == '__main__':
    app.run(debug = True)

# Old edition
# from unittest import TestLoader
# from flask import Flask, render_template, request
# import sqlite3
# import os

# currentdirectory = os.path.dirname(os.path.abspath(__file__))

# app = Flask(__name__)


# @app.route("/")
# def main():
#   return "<p>hello</p>"


# @app.route("/", methods = ["POST"])
# def cookiejar():
#   name = request.form["Name"]
#   category = request.form["Category"]
#   connection = sqlite3.connect(currentdirectory + "\cookiejar.db")
#   cursor = connection.cursor()
#   query1 = "INSERT INTO Cookiejar VALUES('{n}','{c}')".format(n = name, c = category)
#   cursor.execute(query1)
#   connection.commit()

# @app.route("/resultpage",methods = ["GET"])
# def resultpage():
#   try:
#     if request.method == "GET":
#       name = request.args.get("Name")
#       connection = sqlite3.connect(currentdirectory + "\cookiejar.db")
#       cursor = connection.cursor()
#       query1 = "SELECT Category from Cookiejar WHERE Name = {n}".format(n = name)
#       result = cursor.execute(query1)
#       result = result.fetchall()[0][0]
#       return render_template("Resultpage.html", Category = result)
#   except:
#     return render_template("Resultpage.html", Category = "")




# if __name__ == "__main__":
#   app.run()