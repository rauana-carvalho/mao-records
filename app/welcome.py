import os
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
import math

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

    "(NOVO)Buscar com filtros avançados",
    "(NOVO) Realizar compra",
    "(NOVO) Ver pedidos",
    "(NOVO) Histórico do cliente",
    "(NOVO) Relatório mensal",

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
        f"\n\n[dim]↑ ↓ scroll • Enter para continuar • mostrando {start_line}-{end_line} de {total}[/dim]"
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


def _is_printable_key(key):
    return len(key) == 1 and key.isprintable()


def _render_input_screen(form_title, label, value, helper_text, error_text=None):
    cursor = "█"
    shown_value = value + cursor

    lines = [
        f"[bold #d16d9e]{label}[/bold #d16d9e]",
        "",
        shown_value if shown_value.strip() else cursor,
        "",
        "[dim]Esc = cancelar[/dim]",
    ]

    if helper_text:
        lines.extend(["", f"[dim]{helper_text}[/dim]"])

    if error_text:
        lines.extend(["", f"[bold red]{error_text}[/bold red]"])

    return "\n".join(lines)


def _input_text_in_panel(title, label, *, initial_value="", max_length=None, helper_text="", validator=None):
    value = initial_value
    error_text = None

    with Live(
        build_layout(title, _render_input_screen(title, label, value, helper_text, error_text)),
        console=console,
        screen=False,
        auto_refresh=False,
    ) as live:
        while True:
            key = readchar.readkey()

            if key == readchar.key.CTRL_C:
                raise KeyboardInterrupt

            if key == readchar.key.ESC:
                return None

            if key in (readchar.key.ENTER, readchar.key.CR, readchar.key.LF):
                text = value.strip()

                if validator is not None:
                    ok, processed_or_error = validator(text)
                    if ok:
                        return processed_or_error

                    error_text = processed_or_error
                    live.update(
                        build_layout(title, _render_input_screen(title, label, value, helper_text, error_text)),
                        refresh=True,
                    )
                    continue

                return text

            if key in (readchar.key.BACKSPACE, readchar.key.DELETE):
                if value:
                    value = value[:-1]
                    error_text = None
                    live.update(
                        build_layout(title, _render_input_screen(title, label, value, helper_text, error_text)),
                        refresh=True,
                    )
                continue

            if _is_printable_key(key):
                if max_length is None or len(value) < max_length:
                    value += key
                    error_text = None
                    live.update(
                        build_layout(title, _render_input_screen(title, label, value, helper_text, error_text)),
                        refresh=True,
                    )


def _validate_non_empty(max_length=None):
    def validator(text):
        if not text:
            return False, "Esse campo não pode ser vazio."
        if max_length is not None and len(text) > max_length:
            return False, f"Esse campo pode ter no máximo {max_length} caracteres."
        return True, text
    return validator


def _validate_int(min_value=None, max_value=None, max_error_message=None):
    def validator(text):
        if not text:
            return False, "Esse campo não pode ser vazio."
        try:
            value = int(text)
        except ValueError:
            return False, "Entrada inválida. Deve ser um número inteiro."

        if min_value is not None and value < min_value:
            return False, f"O valor deve ser no mínimo {min_value}."

        if max_value is not None and value > max_value:
            if max_error_message:
                return False, max_error_message
            return False, f"O valor deve ser no máximo {max_value}."

        return True, value
    return validator


def _validate_float(min_value=None, max_value=None):
    def validator(text):
        if not text:
            return False, "Esse campo não pode ser vazio."
        try:
            value = float(text)
        except ValueError:
            return False, "Entrada inválida. Deve ser um número."

        if not math.isfinite(value):
            return False, "Entrada inválida. Digite um número finito."

        if min_value is not None and value <= min_value:
            return False, f"O valor deve ser maior que {min_value}."

        if max_value is not None and value > max_value:
            return False, f"O valor deve ser no máximo {max_value}."

        return True, value
    return validator


def _confirm_in_panel(title, message, enter_text="Enter para confirmar", esc_text="Esc para cancelar"):
    content = (
        f"{message}\n\n"
        f"[dim]{enter_text}[/dim]\n"
        f"[dim]{esc_text}[/dim]"
    )

    with Live(
        build_layout(title, content),
        console=console,
        screen=False,
        auto_refresh=False,
    ) as live:
        while True:
            key = readchar.readkey()

            if key == readchar.key.CTRL_C:
                raise KeyboardInterrupt
            if key in (readchar.key.ENTER, readchar.key.CR, readchar.key.LF):
                return True
            if key == readchar.key.ESC:
                return False


def prompt_non_empty_text(title, label, max_length):
    return _input_text_in_panel(
        title,
        label,
        max_length=max_length,
        validator=_validate_non_empty(max_length=max_length),
    )


def prompt_id(title, label):
    return _input_text_in_panel(
        title,
        label,
        max_length=10,
        validator=_validate_int(min_value=1),
    )


def prompt_insert_cd_form():
    titulo = _input_text_in_panel(
        "Inserir CD",
        "Título:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if titulo is None:
        return None

    artista = _input_text_in_panel(
        "Inserir CD",
        "Artista:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if artista is None:
        return None

    genero = _input_text_in_panel(
        "Inserir CD",
        "Gênero:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if genero is None:
        return None

    ano = _input_text_in_panel(
        "Inserir CD",
        "Ano de lançamento:",
        max_length=4,
        validator=_validate_int(min_value=1982, max_value=2026),
    )
    if ano is None:
        return None

    preco = _input_text_in_panel(
        "Inserir CD",
        "Preço:",
        max_length=12,
        validator=_validate_float(min_value=0, max_value=1000000.99),
    )
    if preco is None:
        return None

    quantidade = _input_text_in_panel(
        "Inserir CD",
        "Quantidade:",
        max_length=10,
        validator=_validate_int(
            min_value=0,
            max_value=50,
            max_error_message="Nossa loja tem o limite de 50 unidades por cd.",
        ),
    )
    if quantidade is None:
        return None

    resumo = (
        f"[bold #d16d9e]Confira os dados:[/bold #d16d9e]\n\n"
        f"Título: {titulo}\n"
        f"Artista: {artista}\n"
        f"Gênero: {genero}\n"
        f"Ano de lançamento: {ano}\n"
        f"Preço: {preco}\n"
        f"Quantidade: {quantidade}\n\n"
    )

    confirm = _confirm_in_panel("Confirmar Inserção", resumo)
    if not confirm:
        return None

    return {
        "titulo": titulo,
        "artista": artista,
        "genero": genero,
        "ano": ano,
        "preco": preco,
        "quantidade": quantidade,
    }


def prompt_edit_cd_form(cd_existente):
    titulo = _input_text_in_panel(
        "Alterar CD",
        "Novo título:",
        initial_value=str(cd_existente.titulo),
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if titulo is None:
        return None

    artista = _input_text_in_panel(
        "Alterar CD",
        "Novo artista:",
        initial_value=str(cd_existente.artista),
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if artista is None:
        return None

    genero = _input_text_in_panel(
        "Alterar CD",
        "Novo gênero:",
        initial_value=str(cd_existente.genero),
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if genero is None:
        return None

    ano = _input_text_in_panel(
        "Alterar CD",
        "Novo ano:",
        initial_value=str(cd_existente.ano),
        max_length=4,
        validator=_validate_int(min_value=1982, max_value=2026),
    )
    if ano is None:
        return None

    preco = _input_text_in_panel(
        "Alterar CD",
        "Novo preço:",
        initial_value=str(cd_existente.preco),
        max_length=12,
        validator=_validate_float(min_value=0, max_value=1000000.99),
    )
    if preco is None:
        return None

    quantidade = _input_text_in_panel(
        "Alterar CD",
        "Nova quantidade:",
        initial_value=str(cd_existente.quantidade),
        max_length=10,
        validator=_validate_int(
            min_value=0,
            max_value=50,
            max_error_message="Nossa loja tem o limite de 50 unidades por cd.",
        ),
    )
    if quantidade is None:
        return None

    resumo = (
        f"[bold #d16d9e]Confira os novos dados:[/bold #d16d9e]\n\n"
        f"Título: {titulo}\n"
        f"Artista: {artista}\n"
        f"Gênero: {genero}\n"
        f"Ano de lançamento: {ano}\n"
        f"Preço: {preco}\n"
        f"Quantidade: {quantidade}\n\n"
    )

    confirm = _confirm_in_panel("Confirmar Alteração", resumo)
    if not confirm:
        return None

    return {
        "titulo": titulo,
        "artista": artista,
        "genero": genero,
        "ano": ano,
        "preco": preco,
        "quantidade": quantidade,
    }


def prompt_remove_confirmation(cd_existente):
    message = (
        "[bold red]Tem certeza que deseja remover este CD?[/bold red]\n\n"
        f"{cd_existente}"
    )
    return _confirm_in_panel("Remover CD", message)


def show_home_screen():
    return True