import argparse
import dns.message
import dns.query
import dns.rdatatype
import dns.exception

def log(domain, record_type, use_udp, query_size, response_size, amplification):
    print(f"Anfrage an: {domain} [{record_type}] via {'UDP' if use_udp else 'TCP'}")
    print(f"Anfragegröße: {query_size} Bytes")
    print(f"Antwortgröße: {response_size} Bytes")
    print(f"Verstärkungsfaktor: {amplification:.2f}")

def print_dns_response_content(response):
    if not response.answer:
        print("Keine Antwortdaten (empty answer section).")
        return

    for rrset in response.answer:
        print(f"{rrset.name} ({dns.rdatatype.to_text(rrset.rdtype)}):")
        for item in rrset:
            print(f"  {item}")
    print("-" * 50)

def query_dns(domain, record_type, server, use_udp):
    try:
        # Anfrage erzeugen
        query = dns.message.make_query(domain, record_type, want_dnssec=True)
        raw_query = query.to_wire()
        query_size = len(raw_query)

        # Anfrage senden
        if use_udp:
            response = dns.query.udp(query, server, timeout=3)
        else:
            response = dns.query.tcp(query, server, timeout=3)

        # Antwort auswerten
        raw_response = response.to_wire()
        response_size = len(raw_response)
        amplification = response_size / query_size

        log(domain, record_type, use_udp, query_size, response_size, amplification)


        print_dns_response_content(response)

    except dns.exception.Timeout:
        print(f"Zeitüberschreitung bei Anfrage an {domain}")
    except Exception as e:
        print(f"Fehler: {e}")

def main():
    parser = argparse.ArgumentParser(description="DNS Amplification Analyzer")
    parser.add_argument("domain", help="Ziel-Domain (z.B. example.com)")
    parser.add_argument("--record", default="ANY", help="Record-Typ: A, AAAA, TXT, DNSKEY, ANY...")
    parser.add_argument("--server", default="8.8.8.8", help="DNS-Server (z.B. 8.8.8.8)")
    parser.add_argument("--udp", action="store_true", help="UDP verwenden (Standard ist TCP)")
    args = parser.parse_args()

    query_dns(args.domain, args.record.upper(), args.server, args.udp)

if __name__ == "__main__":
    main()