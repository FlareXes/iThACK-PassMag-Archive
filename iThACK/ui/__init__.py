from typing import Tuple

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

MODE = ""


class _Table:
    def __init__(self, *, vp: bool = False, qp: bool = False, pp: bool = False) -> None:
        self.table = Table()
        self.table.add_column("S.No.", justify="center", style="magenta", header_style="magenta")
        self.table.add_column("Site", justify="center", style="green", header_style="green")
        self.table.add_column("Username / E-Mail", justify="center", style="red", header_style="red")
        self.table.add_column("Url", justify="center", style="green", header_style="green")

        self._vp = vp  # View Prompt
        self._qp = qp  # Quit Prompt
        self._pp = pp  # Password Prompt

    def add_row(self, account: Tuple):
        self.table.add_row(*account)

    def prompts(self) -> str:
        password_format = "[bold magenta] p [/bold magenta][bold white]>[/bold white] [bold]print password[/bold]"
        view_format = "[bold magenta] v [/bold magenta][bold white]>[/bold white] [bold]view accounts[/bold]"
        quit_format = "[bold magenta] q [/bold magenta][bold white]>[/bold white] [bold]quit[/bold]"

        if self._vp and self._qp and self._pp:
            return view_format + "\t" + password_format + "\n" + quit_format
        if self._vp and self._qp:
            return view_format + "\n" + quit_format
        if self._vp:
            return view_format
        if self._qp:
            return quit_format

    def show_table(self):
        console = Console()
        console.print(self.table)
        prompts = self.prompts()
        console.print(prompts)


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
    def prompt(prompt: str) -> str:
        ans = Prompt.ask(prompt, default=None)
        return ans

    @staticmethod
    def getpass(prompt: str) -> str:
        ans = Prompt.ask(f"[bold cyan]{prompt}[/bold cyan]", password=True, default=None)
        return ans


def tabulate(accounts):
    t = _Table(vp=True, qp=True, pp=True)
    for account in accounts:
        account = tuple(map(str, account))
        t.add_row(account)
    t.show_table()


def set_mode(status: str) -> None:
    global MODE
    MODE = status


def get_mode() -> str:
    return MODE
