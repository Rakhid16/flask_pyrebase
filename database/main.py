from pyrebase import initialize_app
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

config = {"apiKey": "rahasia",
          "authDomain": "rahasia",
          "databaseURL": "rahasia",
          "projectId": "rahasia",
          "storageBucket": "rahasia",
          "messagingSenderId": "rahasia",
          "appId": "rahasia"}

db = initialize_app(config).database()

@app.route('/')
def index():
  data = dict(db.child('').get().val())
  return render_template("index.html", data = data)

@app.route('/tambah-data', methods=['GET', 'POST'])
def tambah():
  if request.method=="POST":
    if db.child(request.form['id']).get().val() is not None:
      return '''Data sudah ada. Silahkan masukan data yang lain.
              <br><br><a href="/tambah-data">Kembali</a>'''
    else:
      db.child(request.form['id']).set({"nama" : request.form['nama'],
                                        "jurusan" : request.form['jurusan']})
    return redirect(url_for('index'))
  return render_template("tambah.html")

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
  if request.method=="POST":
    db.child(id).update({"nama" : request.form['nama'],
                         "jurusan" : request.form['jurusan']})

    return redirect(url_for('index'))
  return render_template("edit.html", id = id, data = dict(db.child(id).get().val()))

@app.route('/hapus/<id>')
def hapus(id):
  db.child(id).remove()
  return redirect(url_for('index'))

app.run(debug=True)