from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    pub = open('publications.json', 'r')
    content = pub.read()
    articals = json.loads(content)['data']
    return render_template('/main.html', articals=articals)

if __name__ == '__main__':
    app.run(debug=True)