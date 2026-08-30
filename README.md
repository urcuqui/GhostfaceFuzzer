# 🧠 Overview

GhostfaceFuzzer is an adversarial testing toolkit designed to uncover vulnerabilities in AI models and systems. Whether you're testing Large Language Models (LLMs), image classifiers, or decision-making pipelines, GhostfaceFuzzer provides the mechanisms to probe, break, and analyze AI behavior under adversarial and stress conditions.

Inspired by stealth tactics and fuzzing strategies in cybersecurity, this tool aims to reveal blind spots in model robustness, fairness, and safety.

## ⚙️ Features

🔍 Adversarial Input Generation: Textual and prompt-based fuzzing strategies for LLMs.

🖼️ Perturbation-based attacks: Pixel-level noise and transformations for computer vision models.

🔐 Classic cryptography attacks: Caesar cipher brute-forcing and decoding.

🕵️ Steganography: Hide and extract messages inside images (LSB technique).

💥 Denial of Service (DoS) simulation: Stress-test a local endpoint with concurrent requests.

🧪 Model-Agnostic Evaluation: Plug-and-play support for PyTorch, HuggingFace, and REST API-based models.

📊 Reporting Engine: Logs anomalies, hallucinations, misclassifications, and failure patterns.

🦾 Automation Ready: Easily integrate into CI pipelines or red team simulations.

## 🎯 Use Cases

✅ Red-teaming AI systems

✅ Evaluating LLM safety filters

✅ Ethical hacking activities

✅ Stress-testing image classifiers

✅ Identifying fairness and bias issues

✅ Building robust AI pipelines

## 🔒 Disclaimer

This tool is intended for research and educational purposes only. Do not use it to attack or exploit systems without proper authorization. The Denial of Service module in particular must **only** be run against systems you own or are explicitly authorized to test (e.g. the local demo app included in this repo).

## 📁 Project structure

```
GhostfaceFuzzer/
├── app/                      # Demo Flask app used as a target for the attacks
│   ├── app.py                 # Routes: / , /classify , /hide_message , /ping , /metrics , /dashboard
│   ├── templates/
│   │   ├── index.html          # Main SPA-ish UI
│   │   └── dashboard.html      # Live DoS monitor (polls /metrics)
│   ├── static/skull.gif
│   └── resources/ic.png
├── attacks/
│   ├── cypher/
│   │   ├── ceasar.py           # Caesar cipher brute-force/decoder
│   │   └── stego.py            # Image steganography (hide/extract messages)
│   └── Denial/
│       └── atta.py             # Denial of Service (DoS) load generator against /ping
├── requirements.txt
└── README.md
```

## 🛠️ Requirements & environment setup (venv)

Requires Python 3.9+.

```bash
# 1. Clone the repo (if you haven't already)
git clone <repo-url>
cd GhostfaceFuzzer

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

To leave the virtual environment when you're done: `deactivate`.

## 🚀 Attacks & how to test them

### 1. Caesar cipher (`attacks/cypher/ceasar.py`)

Decodes text encrypted with a classic Caesar cipher, either brute-forcing all 26 shifts or decoding with a known shift.

```bash
# Brute force all possible shifts
python attacks/cypher/ceasar.py "PixxgPiksqvo"

# Decode with a known shift
python attacks/cypher/ceasar.py "PixxgPiksqvo" -s 8
# -> Decrypted with shift 8: happyhacking
```

### 2. Steganography (`attacks/cypher/stego.py`)

Hides a text message inside an image using LSB (least significant bit) encoding on the RGB channels, and extracts it back out. It's also exposed through the demo app via the `/hide_message` endpoint.

**Standalone usage:**

```bash
source venv/bin/activate
python3 -c "
from attacks.cypher import stego

# Hide a message inside an image
stego.hide_message('app/resources/ic.png', 'hack the planet', 'attacks/cypher/imagen_con_mensaje.png')

# Extract the hidden message back out
print(stego.extract_message('attacks/cypher/imagen_con_mensaje.png'))
"
```

**Extract from an existing image via CLI** using `-t/--target` to point to the image (defaults to `imagen_con_mensaje.png` next to the script if omitted):

```bash
python attacks/cypher/stego.py -t attacks/cypher/imagen_con_mensaje.png
```

**Via the demo app** (see step-by-step below): upload an image and a message to `/hide_message` and it returns the stego image.

### 3. Denial of Service — Denial attack (`attacks/Denial/atta.py`)

Floods a target URL with concurrent GET requests using worker threads, to observe how a service degrades under load. By default it targets the demo app's `/ping` endpoint.

⚠️ **Only run this against the local demo app or another target you are explicitly authorized to test.**

```bash
# Default: 50 threads against http://127.0.0.1:5000/ping
python attacks/Denial/atta.py

# Custom thread count / target
python attacks/Denial/atta.py -n 150 -u http://127.0.0.1:5000/ping
```

Stop it with `Ctrl+C` — it prints a summary of response status counts and runs until interrupted.

### 4. Live DoS monitor (`/dashboard`)

The demo app (`app/app.py`) simulates a backend with **limited capacity** (8 concurrent request slots) and exposes live metrics so you can *see* it degrade in real time instead of just reading terminal logs:

- `/ping` — the target endpoint; requests queue for a free slot (up to 3s) and get a `503` if the backend stays saturated too long.
- `/metrics` — JSON snapshot: requests/sec, avg & p95 latency, in-flight vs capacity, queue depth, rejected (503) count, error rate, CPU/memory, uptime.
- `/dashboard` — a live web UI (polls `/metrics` every 500ms) with stat tiles, a real-time RPS/latency chart, and a status banner that flips **OK → DEGRADED → OVERLOADED** as the attack ramps up.

Open `http://127.0.0.1:5000/dashboard` in a browser while `atta.py` is running against the app to watch the degradation live.

## ✅ Step-by-step: try everything end to end

```bash
# 1. Set up the environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Test the Caesar cipher decoder
python attacks/cypher/ceasar.py "PixxgPiksqvo" -s 8

# 3. Test steganography (hide + extract a message)
python3 -c "
from attacks.cypher import stego
stego.hide_message('app/resources/ic.png', 'hack the planet', 'attacks/cypher/imagen_con_mensaje.png')
print(stego.extract_message('attacks/cypher/imagen_con_mensaje.png'))
"

# 4. Start the demo Flask app (target for the DoS attack, stego endpoint, and the live dashboard)
cd app
python app.py
# App runs on http://127.0.0.1:5000

# 5. Open the live monitor in your browser
#    http://127.0.0.1:5000/dashboard

# 6. In a second terminal, with the venv activated, run the Denial attack against it
source venv/bin/activate
python attacks/Denial/atta.py -n 100
# Watch /dashboard: RPS and latency climb, the queue backs up, and 503s/rejections
# appear once the simulated 8-slot capacity stays saturated — status flips to
# DEGRADED then OVERLOADED.
# Press Ctrl+C in the second terminal to stop the attack and watch it recover to OK.
```

## 🤝 Contributors

GhostfaceFuzzer is a collaborative project built with the efforts of professionals passionate about AI security and adversarial robustness.

We thank the following contributors for their valuable input, ideas, and code:

@espinosacodes – Developer

@curcuqui – Latest contributor: enhancements on adversarial pipelines 🔥

Want to contribute? Open an issue, submit a pull request, or reach out!
