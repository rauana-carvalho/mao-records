import os
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live

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
    "   ·        ✦              ⋆         ✦",
    "             ｡         ✦",
]

TITLE_ART = [

    "⋆｡° ✦  MAO RECORDS  ✦ °｡⋆",
    "",
    "███    ███  █████   ██████      ██████  ███████  ██████  ██████  ██████  ███████   ███████",
    "████  ████ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██ ██    ██  ██",
    "██ ████ ██ ███████ ██    ██     ██████  █████   ██      ██    ██ ██████  ██     ██ ███████",
    "██  ██  ██ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██ ██    ██       ██",
    "██      ██ ██   ██  ██████      ██   ██ ███████  ██████  ██████  ██   ██ ███████   ███████",
    "",
    "                          ⋆ your soft little cd store ⋆",
]

TITLE_PANEL_HEIGHT = len(TITLE_ART) + 4

OPTIONS = [
    "Inserir CD",
    "Alterar CD",
    "Pesquisar CD por nome",
    "Remover CD",
    "Listar todos",
    "Exibir CD",
    "Relatório de estoque",
    "Sair",
]


def render_menu(selected):
    lines = []

    for i, option in enumerate(OPTIONS):
        if i == selected:
            lines.append(f"[bold #d16d9e]✦ {option}[/bold #d16d9e]")
        else:
            lines.append(f"  [#6f6f6a]{option}[/#6f6f6a]")

    lines.append("")
    lines.append("[dim]Use ↑ ↓ pra navegar e Enter pra selecionar[/dim]")

    return "\n".join(lines)


def build_layout(right_title, right_content):
    layout = Layout()

    layout.split_row(
        Layout(name="left", size=42),
        Layout(name="right", ratio=1),
    )

    layout["right"].split_column(
        Layout(name="title", size=TITLE_PANEL_HEIGHT),
        Layout(name="content", minimum_size=14),
    )

    left_panel = Panel(
        Align.center("\n".join(LEFT_ART), vertical="middle"),
        title="[bold #e7c6d1]⋆ Welcome ⋆[/bold #e7c6d1]",
        border_style="#d8b7c4",
        padding=(1, 2),
    )

    title_panel = Panel(
        Align.center("\n".join(TITLE_ART), vertical="middle"),
        title="[bold #e7c6d1]✦ Mao Records ✦[/bold #e7c6d1]",
        border_style="#d8b7c4",
        padding=(0, 2),
    )

    content_panel = Panel(
        right_content,
        title=f"[bold #e7c6d1]⋆ {right_title} ⋆[/bold #e7c6d1]",
        border_style="#d8b7c4",
        padding=(1, 3),
    )

    layout["left"].update(left_panel)
    layout["title"].update(title_panel)
    layout["content"].update(content_panel)

    return layout

def interactive_menu():
    selected = 0

    with Live(
        build_layout("Menu", render_menu(selected)),
        console=console,
        screen=False,
        auto_refresh=False,
    ) as live:
        while True:
            key = readchar.readkey()

            if key == readchar.key.UP:
                selected = (selected - 1) % len(OPTIONS)
                live.update(build_layout("Menu", render_menu(selected)), refresh=True)

            elif key == readchar.key.DOWN:
                selected = (selected + 1) % len(OPTIONS)
                live.update(build_layout("Menu", render_menu(selected)), refresh=True)

            elif key == readchar.key.ENTER:
                return OPTIONS[selected]

            elif key == readchar.key.CTRL_C:
                return "Sair"


def _get_result_window_height():
    terminal_height = console.size.height
    usable = terminal_height - 18
    return max(8, usable)


def _render_scrolled_content(content_lines, offset, window_height):
    total = len(content_lines)
    visible_lines = content_lines[offset:offset + window_height]

    body = "\n".join(visible_lines)

    start_line = 0 if total == 0 else offset + 1
    end_line = min(offset + window_height, total)

    footer = (
        f"\n\n[dim]↑ ↓ scroll • Enter para continuar • mostrando {start_line}-{end_line} of {total}[/dim]"
    )

    if total > window_height:
        if offset > 0:
            body = "[dim]▲ mais informações acima[/dim]\n" + body
        if end_line < total:
            body = body + "\n[dim]▼ mais informações abaixo[/dim]"

    return body + footer

def show_result(title, content):
    if not content.strip():
        content = "Não há informações para exibir."

    content_lines = content.rstrip().splitlines()
    if not content_lines:
        content_lines = ["Não há informações para exibir."]
    window_height = _get_result_window_height()
    offset = 0
    max_offset = max(0, len(content_lines) - window_height)

    with Live(
        build_layout(title, _render_scrolled_content(content_lines, offset, window_height)),
        console=console,
        screen=False,
        auto_refresh=False,
    ) as live:
        while True:
            key = readchar.readkey()

            if key == readchar.key.UP:
                new_offset = max(0, offset - 1)
                if new_offset != offset:
                    offset = new_offset
                    live.update(
                        build_layout(title, _render_scrolled_content(content_lines, offset, window_height)),
                        refresh=True,
                    )

            elif key == readchar.key.DOWN:
                new_offset = min(max_offset, offset + 1)
                if new_offset != offset:
                    offset = new_offset
                    live.update(
                        build_layout(title, _render_scrolled_content(content_lines, offset, window_height)),
                        refresh=True,
                    )

            elif key == readchar.key.PAGE_UP:
                new_offset = max(0, offset - window_height)
                if new_offset != offset:
                    offset = new_offset
                    live.update(
                        build_layout(title, _render_scrolled_content(content_lines, offset, window_height)),
                        refresh=True,
                    )

            elif key == readchar.key.PAGE_DOWN:
                new_offset = min(max_offset, offset + window_height)
                if new_offset != offset:
                    offset = new_offset
                    live.update(
                        build_layout(title, _render_scrolled_content(content_lines, offset, window_height)),
                        refresh=True,
                    )

            elif key == readchar.key.ENTER:
                break

            elif key == readchar.key.CTRL_C:
                break


def show_home_screen():
    return True