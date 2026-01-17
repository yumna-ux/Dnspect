from rich.console import Console
from rich.table import Table

console = Console()


def print_results(target: str, record_type: str, results: list[str], response_time: float):
    if not results:
        console.print(f"[yellow]⚠️  No {record_type} records found[/]\n")
        return

    table = Table(
        title=f"DNS Lookup – {target} ({record_type})",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("#", style="dim", width=4)
    table.add_column("Result", style="green")

    for idx, value in enumerate(results, 1):
        table.add_row(str(idx), value)

    console.print(table)
    console.print(f"[dim]Response time: {response_time:.2f} ms[/]\n")
