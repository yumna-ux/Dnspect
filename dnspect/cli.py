import typer
from rich.console import Console
from rich.tree import Tree

from dnspect.resolver import resolve_domain, reverse_lookup, trace_domain
from dnspect.formatter import print_results
from dnspect.utils import validate_domain, validate_ip
from dnspect.parser import parse_record_types

app = typer.Typer(help="Professional DNS Lookup CLI Tool")
console = Console()


@app.command()
def lookup(
    domain: str,
    record: str = typer.Option(
        "A", "--record", "-r", help="DNS record types (comma-separated)"
    ),
    all: bool = typer.Option(False, "--all", help="Query all common DNS records"),
):
    """
    Lookup DNS records for a domain.
    """
    if not validate_domain(domain):
        typer.echo("❌ Invalid domain name")
        raise typer.Exit(1)

    record_types = (
        ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"] if all else parse_record_types(record)
    )

    for rtype in record_types:
        try:
            results, response_time = resolve_domain(domain, rtype)
            print_results(domain, rtype, results, response_time)

        except Exception as e:
            typer.echo(f"⚠️  Could not fetch {rtype} records: {e}")


@app.command()
def reverse(ip: str):
    """
    Reverse DNS lookup (IP → hostname).
    """
    if not validate_ip(ip):
        typer.echo("❌ Invalid IP address")
        raise typer.Exit(1)

    try:
        results, response_time = reverse_lookup(ip)
        print_results(ip, "PTR", results, response_time)
    except Exception as e:
        typer.echo(f"⚠️  Could not perform reverse lookup: {e}")


@app.command()
def trace(domain: str, record: str = "A"):
    """
    Trace DNS resolution path from root servers to authoritative servers.
    """
    if not validate_domain(domain):
        typer.echo("❌ Invalid domain name")
        raise typer.Exit(1)

    steps = trace_domain(domain, record.upper())
    if not steps:
        typer.echo("⚠️  Could not trace DNS path for this domain.")
        raise typer.Exit(1)

    tree = Tree(f"DNS Trace – {domain} ({record.upper()})")

    for i, step in enumerate(steps):
        node = tree.add(f"[cyan]Step {i + 1}[/]")

        for server, time_ms in step["servers"]:
            node.add(f"[yellow]{server}[/] ({time_ms:.2f} ms)")

        for answer in step["answers"]:
            node.add(f"[green]ANSWER → {answer}[/]")

    console.print(tree)


def main():
    app()


if __name__ == "__main__":
    main()
