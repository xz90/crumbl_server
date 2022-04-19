from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect("data\database_v3.db")
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
  name = request.form['name']
  domain = request.form['domain']
  if name:
    # For trackerdb.sql
    query = "SELECT trackers.name, categories.name as 'category' FROM trackers, categories WHERE trackers.category_id = categories.id and trackers.name = ?"
    cursor = db.execute(query, (name, ))
    results = cursor.fetchall()
    if len(results) > 0:
      category = results[0]['category']
      return jsonify(
        name = name,
        domain = domain,
        category = category
      )
    else:
      # For open-cookie-database.csv
      query1 = "SELECT cookie_data_key_name as 'name', category as 'category' FROM open_database WHERE cookie_data_key_name = ?"
      cursor1 = db.execute(query1, (name, ))
      results = cursor1.fetchall()
      if len(results) > 0: 
        category = results[0]['category']
        return jsonify(
          name = name,
          domain = domain,
          category = category
        )
  # For WhoTracksMe sites
  if domain:
    domaincopy = domain
    query = "SELECT * FROM sites WHERE domain = ?"
    while len(domain) != 0:
      cursor = db.execute(query, (domain, ))
      results = cursor.fetchall()
      if len(results) > 0: 
        category = results[0]['category']
        return jsonify(
          name = name,
          domain = domain,
          category = category
        )
      else:
        dlist = domain.split('.', 1)
        if len(dlist) > 1:
          domain = dlist[1]
        else:
          break
  return jsonify(
        name = name,
        domain = domaincopy,
        category = "unknown"
      )

if __name__ == '__main__':
    app.run(debug = True)