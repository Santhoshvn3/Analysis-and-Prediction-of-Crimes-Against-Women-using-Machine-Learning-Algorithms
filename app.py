from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
# model = pickle.load()

@app.route('/')
def home():
    return render_template("state.html")

@app.route('/analysis')
def analysis():
    return render_template("analysis.html")

if __name__ == "__main__":
    app.run(debug=True)
