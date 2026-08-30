from flask import Flask, render_template, request, jsonify
import joblib
import sys, os, time, threading, collections

try:
    import psutil
except ImportError:
    psutil = None

app = Flask(__name__)

# --- Denial of Service demo: simulated backend capacity + live metrics ---
MAX_CONCURRENT = 8       # how many /ping requests the "server" can handle at once
QUEUE_TIMEOUT = 3.0      # seconds a request waits for a free slot before being rejected (503)
METRICS_WINDOW = 10.0    # seconds of history used to compute rps/latency

_capacity = threading.Semaphore(MAX_CONCURRENT)
_metrics_lock = threading.Lock()
_metrics = {
    "requests_total": 0,
    "rejected_total": 0,
    "in_flight": 0,
    "queue_waiting": 0,
    "start_time": time.time(),
}
_recent = collections.deque()  # (timestamp, latency_seconds, ok)


def _record(latency, ok):
    now = time.time()
    with _metrics_lock:
        _recent.append((now, latency, ok))
        _metrics["requests_total"] += 1
        if not ok:
            _metrics["rejected_total"] += 1
parent_dir = os.getcwd() 

path = os.path.dirname(parent_dir)

sys.path.append(path)
sys.path.append(parent_dir)
from attacks.cypher import stego
#model_filename = os.path.join(os.path.dirname(__file__), 'full.joblib')

#loaded_model = joblib.load(model_filename)

def classify_message(text):    
    predictions = loaded_model.predict([text])
    if predictions[0] == 0:
        return "0-250000"
    elif predictions[0] == 1:
        return "250000-350000"
    elif predictions[0] == 2:
        return "350000-450000"
    elif predictions[0] == 3:
        return "450000-550000"
    else:
        return "650000+"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    message = data.get("message", "")   
    result = classify_message(message)    
    return jsonify({"result": result})

@app.route("/hide_message", methods=["POST"])
def stego_img():
    file = request.files["image"]
    if not file:
        return "No images uploaded", 400
    text_tohidden = request.values["texthidden"]
    file_stego = os.path.join(os.path.dirname(__file__), 'imagen_con_mensaje.png')
    result = stego.hide_message(file, text_tohidden, file_stego)    
    return render_template("index.html", result=result)   
    

@app.route('/ping')
def ping():
    start = time.time()
    with _metrics_lock:
        _metrics["queue_waiting"] += 1
    acquired = _capacity.acquire(timeout=QUEUE_TIMEOUT)
    with _metrics_lock:
        _metrics["queue_waiting"] -= 1

    if not acquired:
        _record(time.time() - start, ok=False)
        return 'Service Unavailable - server overloaded', 503

    try:
        with _metrics_lock:
            _metrics["in_flight"] += 1
        time.sleep(0.1)  # Simula trabajo del servidor
        _record(time.time() - start, ok=True)
        return 'pong'
    finally:
        with _metrics_lock:
            _metrics["in_flight"] -= 1
        _capacity.release()


@app.route('/metrics')
def metrics():
    now = time.time()
    with _metrics_lock:
        while _recent and now - _recent[0][0] > METRICS_WINDOW:
            _recent.popleft()
        recent = list(_recent)
        snapshot = dict(_metrics)

    ok_latencies = [lat for (_, lat, ok) in recent if ok]
    rps = len(recent) / METRICS_WINDOW
    avg_latency_ms = (sum(ok_latencies) / len(ok_latencies) * 1000) if ok_latencies else 0
    if ok_latencies:
        sorted_lat = sorted(ok_latencies)
        p95_latency_ms = sorted_lat[min(len(sorted_lat) - 1, int(0.95 * len(sorted_lat)))] * 1000
    else:
        p95_latency_ms = 0
    error_rate_pct = (snapshot["rejected_total"] / snapshot["requests_total"] * 100) if snapshot["requests_total"] else 0

    cpu_percent = psutil.cpu_percent(interval=None) if psutil else None
    mem_mb = round(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024), 1) if psutil else None

    return jsonify({
        "requests_total": snapshot["requests_total"],
        "rejected_total": snapshot["rejected_total"],
        "in_flight": snapshot["in_flight"],
        "queue_waiting": snapshot["queue_waiting"],
        "capacity": MAX_CONCURRENT,
        "rps": round(rps, 2),
        "avg_latency_ms": round(avg_latency_ms, 1),
        "p95_latency_ms": round(p95_latency_ms, 1),
        "error_rate_pct": round(error_rate_pct, 1),
        "uptime_s": round(now - snapshot["start_time"], 1),
        "cpu_percent": cpu_percent,
        "mem_mb": mem_mb,
    })


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=False, threaded=True)
    