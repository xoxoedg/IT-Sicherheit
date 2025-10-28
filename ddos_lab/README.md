# Lokales DDoS-/Rate‑Limit‑Labor (README)

**Kurz:** Dieses Lab dient ausschließlich **akademischen Zwecken** und lokalen Tests. Führe es nur in einer isolierten Testumgebung aus — niemals gegen fremde Systeme oder das Internet. Du trägst die Verantwortung für die Durchführung.

---

## Aufbau des Repositories

* `docker-compose.yml` — definiert zwei Hauptservices:

    * **victim** — Nginx‑Webserver (konfigurierbar via `./nginx.conf`). Wenn kein `./html`‑Ordner vorhanden ist, liefert das offizielle Nginx‑Image die Standard‑Willkommensseite.
    * **attacker** — harmloser, konfigurierbarer Lastgenerator (`attacker/load_test.py`) — thread‑basiert, typischerweise one‑off.
* `nginx.conf` — Beispielkonfiguration mit `limit_req_zone` / `limit_req` (Rate‑Limiting).
* `attacker/load_test.py` — Python‑Script mit Parametern: `--target`, `--threads`, `--reqs`, `--delay`, optional `--ramp`.
* `tools/` — Hilfs‑Skripte (z. B. `log_parser.py`) für Log‑Analyse und Monitoring.
* `logs/` — gemounteter Ordner für `access.log` / `error.log` (hostseitig sichtbar) — optional.

> Hinweis: Falls du eigene statische Inhalte testen willst, lege optional einen `html/`‑Ordner an und mounte ihn in `docker-compose.yml` auf `/usr/share/nginx/html`.

---

## Voraussetzungen

* Docker & Docker Compose (V2) installiert.
* Python (nur falls du `attacker/load_test.py` lokal ausführen willst).
* Führe das Lab in einem privaten/isolierten Netzwerk aus.

---

## Schnellstart — Container hochfahren

Im Projektverzeichnis:

```bash
# Build & start (detached)
docker compose up -d --build

# Status prüfen
docker compose ps
```

Erwartetes Verhalten:

* `victim` läuft dauerhaft 
* `attacker` wird typischerweise als one‑off ausgeführt (siehe Abschnitt weiter unten).

---

## Angreifer starten (empfohlen: one‑off)

Nutze `docker compose run --rm` für saubere, temporäre Testläufe:

```bash
# Moderates Beispiel
docker compose run --rm attacker python load_test.py \
  --target http://victim:80/ \
  --threads 5 --reqs 200 --delay 0.05
```

Parameter:

* `--target` — Standard `http://victim:80/`. Innerhalb des Compose‑Netzwerks ist `victim` per DNS erreichbar.
* `--threads` — Anzahl gleichzeitiger Worker.
* `--reqs` — Requests pro Thread.
* `--delay` — Pause (s) zwischen Requests eines Threads.

Empfehlung: Nutze `--ramp` oder Jitter, um instant spikes zu vermeiden.

Beispiel mit Ramp:

```bash
docker compose run --rm attacker python load_test.py \
  --target http://victim:80/ \
  --threads 20 --reqs 500 --delay 0.02 --ramp 10
```

---

## Logs, Monitoring & Debugging

* Live‑Logs:

```bash
docker compose logs -f victim
docker compose logs --follow attacker
# Hostseitig (falls gemountet):
tail -f ./logs/access.log ./logs/error.log
```

* Nginx‑Konfigprüfung im Victim:

```bash
docker compose exec victim nginx -t
# bei Erfolg:
docker compose exec victim nginx -s reload
```



## Nützliche Kommandos (Schnellreferenz)

```bash
docker compose up -d --build
docker compose run --rm attacker python load_test.py --target http://victim:80/ --threads 5 --reqs 200 --delay 0.05
docker compose exec attacker ping -c3 victim
docker compose logs -f victim
docker compose down
```

HAVE FUN <3