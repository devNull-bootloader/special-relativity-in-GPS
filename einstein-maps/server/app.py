from flask import Flask, jsonify, request, send_from_directory
import time
import error_model as em

app = Flask(__name__, static_folder="../web", static_url_path="")
T0 = time.time()
MODES = ("full", "secular_only", "none")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html") # type: ignore

@app.route("/api/error")
def api_error():
    system = request.args.get("system", "GPS")
    mode = request.args.get("mode", "none")

    if system not in em.SYSTEMS or mode not in MODES:
        return jsonify({"error": "bad system or mode"}), 400

    sim_s = ((time.time() - T0) * em.TIME_SCALE) % 86400
    result = em.error_vector(system, mode, sim_s)
    result["sim_s"] = sim_s
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def reset():
    global T0
    T0 = time.time()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(port=5000, debug=False)
