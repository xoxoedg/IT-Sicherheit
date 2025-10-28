import re, time, argparse
from collections import Counter

LOGFILE = "../logs/access.log"

line_re = re.compile(r'(\S+) - - \[.*?\] ".*?" \d+ \d+ ".*" ".*"')

def parse(path):
    counts = Counter()
    try:
        with open(path, "r") as f:
            for line in f:
                m = line_re.match(line)
                if m:
                    ip = m.group(1)
                    counts[ip] += 1
    except FileNotFoundError:
        print("Logfile nicht gefunden:", path)
    return counts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--follow", action="store_true", help="tail -f Verhalten")
    args = parser.parse_args()

    while True:
        counts = parse(LOGFILE)
        if counts:
            print("Top IPs:", counts.most_common(args.top))
        else:
            print("Keine Einträge.")
        if not args.follow:
            break
        time.sleep(3)

if __name__ == "__main__":
    main()