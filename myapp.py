from asyncio.windows_events import NULL
from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect("data\database_v2.db")
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    #Check if DB is there
    if not hasattr(g, 'sqlite3'):
        g.sqlite3_db = connect_db()
    return g.sqlite3_db

# close the connection to the database automatically
@app.teardown_appcontext
def close_db(error):
    #if global object has a sqlite database then close it. If u leave it open noone can access it and gets lost in memory causing leaks.
    if hasattr(g, 'sqlite_db'):
        g.sqlite3_db.close()

@app.route('/', methods=['GET'])
def viewusers():
  db = get_db()
  if request.method == 'GET':
    name = request.form['name']
    domain = request.form['domain']
    if name:
      # For trackerdb.sql
      query = "SELECT trackers.name, categories.name as 'category' FROM trackers, categories WHERE trackers.category_id = categories.id and trackers.name = ?"
      cursor = db.execute(query, (name, ))
      results = cursor.fetchall()
      if len(results) > 0:
        category = results[0]['category']
        return HELLO_HTML.format(name, category)
      else:
        # For open-cookie-database.csv
        query1 = "SELECT cookie_data_key_name as 'name', category as 'category' FROM open_database WHERE cookie_data_key_name = ?"
        cursor1 = db.execute(query1, (name, ))
        results = cursor1.fetchall()
        if len(results) > 0: 
          category = results[0]['category']
          return HELLO_HTML.format(name, category)
    # For WhoTracksMe sites
    if domain:
      query2 = "SELECT * FROM sites WHERE domain = ?"
      cursor2 = db.execute(query2, (domain, ))
      results2 = cursor2.fetchall()
      if len(results2) > 0: 
        category2 = results2[0]['category']
        return HELLO_HTML.format(name, category2)
  return "<p>Hello World</p>"


HELLO_HTML = """
  <html><body>
    <h1>Hello, {0}!</h1>
    Your category is {1}.
  </body></html>"""

if __name__ == '__main__':
    app.run(debug = True)