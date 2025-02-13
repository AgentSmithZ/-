from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/request')
def request():
    return render_template('request.html')

if __name__ == '__main__':
    app.run()