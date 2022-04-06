from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect('data\data2db.db')
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
      # For data.db
      # query1 = "SELECT trackers.name, categories.name as 'category' FROM trackers, categories WHERE trackers.category_id = categories.id and trackers.name = {n}".format(n = name)
      # For data2db.db
      # query1 = "SELECT cookie_data_key_name as 'name', category as 'category' FROM mytable WHERE cookie_data_key_name = {n}".format(n = name)
     
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