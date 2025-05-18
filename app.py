from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bem-vindo ao site de terreiros religiosos!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)