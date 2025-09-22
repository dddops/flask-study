from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

@app.route('/hello')
def hello():
    return render_template("hello.html", name="홍길동")

@app.route('/user/<username>')
def user(username):
    return render_template("user.html", username=username)

@app.route('/fruits')
def fruits():
    fruits_list = ["사과", "바나나", "딸기", "포도", "오렌지"]
    return render_template("fruits.html", fruits=fruits_list)

if __name__ == '__main__':
    app.run(debug=True)