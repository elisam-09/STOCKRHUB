from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    print("🚀 Serveur qui démarre sur http://127.0.0.1:5001")
    app.run(debug=True, port=5001)