from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return render_template('index.html')

@app.route('/classroom/<int:room>', methods=['POST', 'GET'])
def classroom(room):
    return render_template('classroom.html', room=room)

if __name__ == '__main__':
    app.run(port=3000, debug=True)