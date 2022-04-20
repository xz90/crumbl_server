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
    # check whether cookie name exists in open-cookie-database.csv
    query = "SELECT cookie_data_key_name as 'name', category as 'category' FROM open_database WHERE cookie_data_key_name = ?"
    cursor = db.execute(query, (name, ))
    results = cursor.fetchall()
    if len(results) > 0: 
        category = results[0]['category']
        return jsonify(
          name = name,
          domain = domain,
          category = category
        )

  # check whether cookie domain exists in tracker_domains table
  if domain:
    query = """
    SELECT categories.id, categories.name, trackers.id, tracker_domains.domain
    FROM trackers
    JOIN categories ON categories.id = trackers.category_id
    JOIN tracker_domains ON tracker_domains.tracker = trackers.id
    WHERE domain = ?
    """
    while len(domain) != 0:
      cursor = db.execute(query, (domain, ))
      results = cursor.fetchall()
      if len(results) > 0: 
        category = results[0]['name']
        return jsonify(
          name = name,
          domain = request.form['domain'],
          category = category
        )
      else:
        dlist = domain.split('.', 1)
        if len(dlist) > 1:
          domain = dlist[1]
        else:
          break

    # check whether cookie domain exists in sites table
    domain = request.form['domain']
    query = "SELECT * FROM sites WHERE domain = ?"
    while len(domain) != 0:
      cursor = db.execute(query, (domain, ))
      results = cursor.fetchall()
      if len(results) > 0: 
        category = results[0]['category']
        return jsonify(
          name = name,
          domain = request.form['domain'],
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
        domain = request.form['domain'],
        category = "unknown"
      )

if __name__ == '__main__':
    app.run(debug = True)