
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests
from datetime import datetime
from bson import ObjectId
app = Flask(__name__)

password = '1lh4m1h54n'
cnn_str = f'mongodb://ilham10ihsan:{password}@ac-qpbduu1-shard-00-00.uobexa5.mongodb.net:27017,ac-qpbduu1-shard-00-01.uobexa5.mongodb.net:27017,ac-qpbduu1-shard-00-02.uobexa5.mongodb.net:27017/?ssl=true&replicaSet=atlas-11enlv-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(cnn_str)
db = client.dbdictionary_sparta

@app.route('/')
def main():
     words_result = db.words.find({},{'_id':False})
     words = []
     for word in words_result :
        definition = word['definitions'][0]['shortdef']
        definition = definition if type(definition) is str else definition[0]
        words.append({
            'word': word['word'],
            'definition': definition,
        })
     msg = request.args.get('msg')
     return render_template('index.html',words=words, msg=msg)

@app.route('/detail/<keyword>')
def detail(keyword):
     api_key = 'b95a1c04-ce53-4f95-859b-8e6863a8741f'
     url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
     response = requests.get(url)
     definitions = response.json()
     if not definitions :
        return render_template('error.html', suggestions=[])
     if type(definitions[0]) is str :
         suggestions = definitions
         return render_template('error.html', suggestions=suggestions)
     status = request.args.get('status_give', 'new')
     return render_template(
          'detail.html', 
          word=keyword,
          definitions = definitions,
          status=status
          )

@app.route('/api/save_word', methods=['POST'])
def save_word():
    if request.method == 'POST':  # Menambahkan penanganan metode POST
        json_data = request.get_json()
        word = json_data.get('word_give')  # Fix typo 'worl_give' to 'word_give'
        definitions = json_data.get('definitions_give')
        doc = {
            'word': word,
            'definitions': definitions,
            'date' : datetime.now().strftime('%Y''-''%m''-''%d'),
        }
        db.words.insert_one(doc)
        return jsonify({
            'result': 'success',
            'msg': f'The Word, {word} Was Saved!!!',
        })
    else:
        return jsonify({
            'result': 'error',
            'msg': 'Invalid request method',
        })

@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    db.examples.delete_many({'word':word})
    return jsonify({
          'result':'success',
          'msg':f'The Word,{word} Was Delete',
     })

@app.route('/api/get_exs', methods=['GET'])
def get_exs():
    word = request.args.get('word')
    example_data = db.examples.find({'word':word})
    examples = []
    for example in example_data:
        examples.append({
            'example' : example.get('example'),
            'id' : str(example.get('_id')),
        })
    return jsonify({'result': 'success','examples':examples})

@app.route('/api/save_ex', methods=['POST'])
def save_ex():
    word = request.form.get('word')
    example =request.form.get('example') 
    doc = {
        'word' : word,
        'example' : example,
    }
    db.examples.insert_one(doc)
    return jsonify({'result': 'success','msg' :f'Your Example,{example}, Was Save {word} !!! ',})


@app.route('/api/delete_ex', methods=['POST'])
def delete_ex():
    id = request.form.get('id')
    word = request.form.get('word')
    db.examples.delete_one({
        '_id':ObjectId(id)
      
    })
    return jsonify({
        'result': 'success',
        'msg' : f'The Word {word} Was Deleted !!!',
    })


if __name__ == '__main__':
     app.run('0.0.0.0', port=5000, debug=True)
