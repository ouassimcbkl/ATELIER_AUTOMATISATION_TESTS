from flask import Flask, render_template, jsonify, redirect
from tester.runner import run_all_tests
from storage import save_run, list_runs

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    runs = list_runs(limit=20)
    return render_template("dashboard.html", runs=runs)

@app.route("/run", methods=["POST", "GET"])
def trigger_run():
    run_data = run_all_tests()
    save_run(run_data)
    return jsonify(run_data)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
