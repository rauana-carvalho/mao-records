import os
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.text import Text

console = Console()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


LEFT_ART = [
    "          ✦            ⋆         ✦",
    "    ⋆           ⋆                 ·",
    "                   .       ✦",
    "",
    "           ▒██▓░",
    "           ▒███▒ ░░███░░   ░██░░",
    "           ▒███▓░▒█████▓▓▓▓████▒",
    "           ▒████▒▓█████████████▒",
    "          ░▒███████████████████▓░",
    "        ░▒█████████████▒████▒███░",
    "       ░▒███████████████████████░",
    "       ░██████████████████████▓░",
    "      ░▓██████████████████████▒",
    "     ░▒████████████████████████░",
    "      ████▓░░░░▓████████░░▒█████▒",
    "     ░███▓░   ░▓█████░     ░▓████░",
    "              ░▓████░",
    "",
    "        ⋆ soft night vibes ⋆",
    "",
    "   ·        ✦              ⋆         ﾟ",
    "             ｡         ✦",
]

TITLE_ART = [
    "⋆｡° ✦  MAOS RECORDS  ✦ °｡⋆",
    "",
    "███    ███  █████   ██████      ██████  ███████  ██████  ██████  ██████  ███████",
    "████  ████ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██ ██",
    "██ ████ ██ ███████ ██    ██     ██████  █████   ██      ██    ██ ██████  ███████",
    "██  ██  ██ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██      ██",
    "██      ██ ██   ██  ██████      ██   ██ ███████  ██████  ██████  ██   ██ ███████",
    "",
    "                          ⋆ your soft little cd store ⋆",
]

def show_home_screen():
    clear_screen()

    left_panel = Panel(
        Align.center("\n".join(LEFT_ART), vertical="middle"),
        border_style="#c9a9b8",
        padding=(1, 2),
        title="[bold #e7c6d1]⋆ Welcome ⋆[/bold #e7c6d1]",
        width=42,
    )

    right_panel = Panel(
        Align.center("\n".join(TITLE_ART), vertical="middle"),
        border_style="#c9a9b8",
        padding=(1, 3),
        width=95,
    )

    console.print("\n")
    console.print(
        Align.center(
            Columns(
                [left_panel, right_panel],
                equal=False,
                expand=False,
            )
        )
    )
    console.print("\n")
    console.print("[bold #d16d9e]Press Enter to continue...[/bold #d16d9e]", justify="center")

    try:
        while True:
            key = readchar.readkey()
            if key == readchar.key.ENTER:
                break
            elif key == readchar.key.CTRL_C:
                return False
    except KeyboardInterrupt:
        return False

    clear_screen()
    return True