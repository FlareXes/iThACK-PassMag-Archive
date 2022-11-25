from rich.console import Console
from rich.table import Table


class _Table:
    def __init__(self) -> None:
        self.table = Table()
        self.table.add_column("S.No.", justify="center", style="magenta", header_style="magenta")
        self.table.add_column("Site", justify="center", style="green", header_style="green")
        self.table.add_column("Username / E-Mail", justify="center", style="red", header_style="red")
        self.table.add_column("Url", justify="center", style="green", header_style="green")

    def add_row(self, account):
        self.table.add_row(*account.get_str_type())

    def show_table(self):
        console = Console()
        console.print(self.table)


class Print:
    def __init__(self, text: str):
        self.text = text
        self.console = Console()

    def success(self):
        self.console.print(f"[bold green]{self.text}[/bold green]")

    def warning(self):
        self.console.print(f"[bold yellow]{self.text}[/bold yellow]")

    def fail(self):
        self.console.print(f"[bold red]{self.text}[/bold red]")


def tabulate(accounts):
    t = _Table()
    for account in accounts:
        t.add_row(account)
    t.show_table()
