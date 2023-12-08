from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối đến MongoDB
client = MongoClient('mongodb://localhost:27017/')
database = client['danhba']
collection = database['lienlac']

@app.route('/')
def home():
    danh_ba = collection.find()
    return render_template('index.html', danh_ba=danh_ba)

@app.route('/them_lien_lac', methods=['POST'])
def them_lien_lac():
    ten = request.form.get('ten')
    sdt = request.form.get('sdt')
    lien_lac = {'ten': ten, 'sdt': sdt}
    collection.insert_one(lien_lac)
    return redirect(url_for('home'))

@app.route('/xoa_lien_lac/<ten>')
def xoa_lien_lac(ten):
    collection.delete_one({'ten': ten})
    return redirect(url_for('home'))

@app.route('/sua_lien_lac/<ten_cu>', methods=['GET', 'POST'])
def sua_lien_lac(ten_cu):
    if request.method == 'POST':
        ten_moi = request.form.get('ten')
        sdt_moi = request.form.get('sdt')
        collection.update_one({'ten': ten_cu}, {'$set': {'ten': ten_moi, 'sdt': sdt_moi}})
        return redirect(url_for('home'))
    else:
        lien_lac = collection.find_one({'ten': ten_cu})
        return render_template('sua_lien_lac.html', lien_lac=lien_lac)

if __name__ == '__main__':
    app.run(debug=True)
