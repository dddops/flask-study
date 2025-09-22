from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    pass

@app.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    return render_template("greet.html", name=name)
    pass


if __name__ == "__main__":
    app.run(debug=True)
