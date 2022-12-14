from typing import Tuple

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table


class _Table:
    def __init__(self) -> None:
        self.table = Table()
        self.table.add_column("S.No.", justify="center", style="magenta", header_style="magenta")
        self.table.add_column("Site", justify="center", style="green", header_style="green")
        self.table.add_column("Username / E-Mail", justify="center", style="red", header_style="red")
        self.table.add_column("Url", justify="center", style="green", header_style="green")

    def add_row(self, account: Tuple):
        self.table.add_row(*account)

    def show_table(self):
        console = Console()
        console.print(self.table)


class Print:
    @staticmethod
    def success(text):
        console = Console()
        console.print(f"[bold green]{text}[/bold green]")

    @staticmethod
    def warning(text):
        console = Console()
        console.print(f"[bold yellow]{text}[/bold yellow]")

    @staticmethod
    def fail(text):
        console = Console()
        console.print(f"[bold red]{text}[/bold red]")


class Input:
    @staticmethod
    def confirm() -> bool:
        if Confirm.ask("[bold yellow]Are you sure?[/bold yellow]"):
            return True
        else:
            return False

    @staticmethod
    def prompt() -> str:
        ans = Prompt.ask(default=None)
        return ans

    @staticmethod
    def getpass(prompt: str) -> str:
        ans = Prompt.ask(f"[bold cyan]{prompt}[/bold cyan]", password=True, default=None)
        return ans


def tabulate(accounts):
    t = _Table()
    for account in accounts:
        account = tuple(map(str, account))
        t.add_row(account)
    t.show_table()
