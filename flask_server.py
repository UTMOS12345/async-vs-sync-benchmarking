import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/test")
def sync_task():
    # Simulate a 100ms I/O operation
    time.sleep(0.1)
    return jsonify({"server": "flask", "status": "done"})


if __name__ == "__main__":
    # run  threaded=True
    app.run(port=5000, threaded=True)
