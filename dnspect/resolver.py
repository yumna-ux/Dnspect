import dns.resolver
import dns.reversename
import dns.message
import dns.query
import dns.rdatatype
import dns.name
import time
from typing import List, Tuple, Dict

ROOT_SERVERS = [
    "198.41.0.4", "199.9.14.201", "192.33.4.12", "199.7.91.13",
    "192.203.230.10", "192.5.5.241", "192.112.36.4", "198.97.190.53",
    "192.36.148.17", "192.58.128.30", "193.0.14.129", "199.7.83.42",
    "202.12.27.33"
]

def resolve_domain(domain: str, record_type: str) -> Tuple[List[str], float]:
    """
    Resolve a domain for a specific DNS record type.
    Returns list of results and response time in milliseconds.
    """
    resolver = dns.resolver.Resolver()
    start = time.time()
    answer = resolver.resolve(domain, record_type)
    elapsed = (time.time() - start) * 1000
    results = [r.to_text() for r in answer]
    return results, elapsed


def reverse_lookup(ip: str) -> Tuple[List[str], float]:
    """
    Reverse lookup an IP address to get PTR records.
    """
    reverse_name = dns.reversename.from_address(ip)
    resolver = dns.resolver.Resolver()
    start = time.time()
    answer = resolver.resolve(reverse_name, "PTR")
    elapsed = (time.time() - start) * 1000
    results = [r.to_text() for r in answer]
    return results, elapsed


def trace_domain(domain: str, record_type: str = "A") -> List[Dict]:
    """
    Trace DNS resolution from root servers to authoritative servers.
    Returns a list of steps; each step contains queried servers and answers.
    """
    record_type = record_type.upper()
    domain_name = dns.name.from_text(domain).canonicalize()
    steps = []

    current_servers = ROOT_SERVERS.copy()

    for step_number in range(10):  
        step_info = {"servers": [], "answers": []}
        next_ns = []

        for server in current_servers:
            try:
                query = dns.message.make_query(domain_name, record_type)
                start = time.time()
                response = dns.query.udp(query, server, timeout=3)
                elapsed = (time.time() - start) * 1000
                step_info["servers"].append((server, elapsed))

                if response.answer:
                    for ans in response.answer:
                        for item in ans:
                            step_info["answers"].append(str(item))
                    steps.append(step_info)
                    return steps

                if response.authority:
                    for auth in response.authority:
                        if auth.rdtype == dns.rdatatype.NS:
                            for ns in auth:
                                next_ns.append(ns.to_text())

            except Exception:
                continue  

        steps.append(step_info)

        resolved_ips = []
        for ns_name in set(next_ns):  
            try:
                ns_answers = dns.resolver.resolve(ns_name, "A")
                for ans in ns_answers:
                    resolved_ips.append(ans.address)
            except Exception:
                continue

        if not resolved_ips:
            break  

        current_servers = resolved_ips

    return steps
