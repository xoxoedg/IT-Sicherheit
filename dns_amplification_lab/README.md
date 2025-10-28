# DNS Amplification Attack

**Kurz:** 
Dieses Lab dient ausschließlich **akademischen Zwecken** und lokalen Tests. Führe es nur in einer isolierten Testumgebung aus — niemals gegen fremde Systeme oder das Internet. Du trägst die Verantwortung für die Durchführung.
Außerdem erlaubt dieses Programm auch kein IP-Spoofing

## DNS-Auflösung – Recap

Das Domain Name System (DNS) dient der Auflösung von Domainnamen (z.B. `google.com`) in IP-Adressen.

Die Namensauflösung erfolgt hierarchisch:

1. Lokaler DNS-Resolver (z.B.vom ISP oder lokal installiert) erhält eine Anfrage, z.B nach `google.com`.
2. Falls keine Antwort im lokalen Cache liegt, erfolgt eine **rekursive Anfrage** (auch iterativ möglich) durch folgende Ebenen:

    - **Root-Server**: Liefert die IP-Adressen der zuständigen **Top-Level-Domain (TLD)**-Server (z.B. `.com`, `.de`).
    - **TLD-Server**: Liefert die Adresse der **authoritativen Nameserver** für die Ziel-Domain (z.B. `ns1.google.com`).
    - **Authoritativer Nameserver**: Kennt den endgültigen **A-, AAAA-, TXT- usw.-Record** für die Domain und liefert die gesuchte IP-Adresse zurück.

## DNS Resource Record Types – Übersicht

| Typ     | Bedeutung                     | Beschreibung                                         |
|---------|-------------------------------|------------------------------------------------------|
| A       | IPv4-Adresse                  | Verweist auf die IPv4-Adresse einer Domain           |
| AAAA    | IPv6-Adresse                  | Verweist auf die IPv6-Adresse einer Domain           |
| CNAME   | Canonical Name                | Alias für eine andere Domain                         |
| MX      | Mail Exchange                 | Zuständiger Mailserver für die Domain                |
| NS      | Name Server                   | Zuständige autoritative Nameserver                   |
| TXT     | Text                          | Freitext (z.B. SPF, DKIM, Verifizierungsdaten)       |
| SOA     | Start of Authority            | Zonenstart, Admin-Info, Serialnummer, Refresh-Zeiten |


![DNS_Hierarchie](img/dns.png)

## Ziel des DNS Amplification Angriffs

Der Angreifer sendet DNS-Anfragen über das UDP-Protokoll (geringer Overhead) an öffentlich erreichbare DNS-Resolver.  
Dabei manipuliert er den IP-Header so, dass als "Source Address" nicht seine eigene IP, sondern die des Opfers eingetragen ist (IP-Spoofing).

Die DNS-Anfrage ist bewusst klein gehalten, enthält aber gezielt einen Query-Typ (z.B. `TXT`, `ANY`, `DNSKEY`), der bei bestimmten Domains eine sehr große Antwort verursacht (z.B. ~3000 Byte).  
Die DNS-Server senden diese Antwort dann – wie vorgesehen – an die gefälschte Absenderadresse: das Opfer.

Das Ziel:  
Mit möglichst wenig eigener Bandbreite erzeugt der Angreifer ein Vielfaches an Antwortdaten, die das Opfer überfluten (DDoS durch Bandbreitenverstärkung).

---

## Auswahl gezielter Resource Records

Der Angreifer „manipuliert“ den Query nicht im Inhalt, sondern in der Auswahl:  
Er weiß aus vorheriger Analyse, dass bestimmte Domains bei bestimmten Resource Record Types besonders große Antworten liefern.

Beispiele:
- `TXT`-Records mit langen SPF/DKIM-Daten
- `DNSKEY`/`RRSIG` bei DNSSEC-aktivierten Zonen
- `ANY`-Anfragen, falls vom Resolver erlaubt

Indem der Angreifer gezielt solche Anfragen stellt, entstehen stark verstärkte Antwortpakete (z. B. Verstärkungsfaktor 40–50), die dann das Opfer treffen.



## Ausführung

```bash
python3 dns_amp_tool.py cloudflare.com --record TXT --server 1.1.1.1 --udp
```

| Argument              | Pflicht | Beschreibung                                                                 |
|-----------------------|---------|-------------------------------------------------------------------------------|
| `<domain>`            | ja      | Die Domain, die abgefragt werden soll (z.B. `example.com`)                  |
| `--record <TYPE>`     | nein    | Record-Typ: `A`, `TXT`, `ANY`, `DNSKEY`, etc. (Standard: `ANY`)             |
| `--server <IP>`       | nein    | DNS-Server, an den die Anfrage gesendet wird (Standard: `8.8.8.8`)           |
| `--udp`               | nein    | Verwende UDP statt TCP (Standard ist TCP)                                   |