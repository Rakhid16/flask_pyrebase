from pyrebase import initialize_app
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

config = {"apiKey": "rahasia",
          "authDomain": "rahasia",
          "databaseURL": "rahasia",
          "projectId": "rahasia",
          "storageBucket": "rahasia",
          "messagingSenderId": "rahasia",
          "appId": "rahasia",
          "serviceAccount" : "firebase_key.json"}

storage = initialize_app(config).storage()

@app.route('/', methods=['GET', 'POST'])
def index():
  data = [i.name for i in storage.child('').list_files()]
  
  if request.method=="POST":
    storage.child(secure_filename(request.files['gambar'].filename)).put(request.files['gambar'])
    return redirect(url_for('index'))

  return render_template("index.html", data = data)

@app.route('/lihat/<nama>')
def lihat(nama):
  id = storage.child(nama).get_url(None)
  return render_template("lihat.html", gambar = id)

@app.route('/unduh/<nama>')
def unduh(nama):
  storage.child(nama).download(nama)
  return redirect(url_for('index'))

@app.route('/hapus/<nama>')
def hapus(nama):
  storage.delete(nama)
  return redirect(url_for('index'))

app.run(debug=True)