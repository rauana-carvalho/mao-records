import os
import math

import readchar
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel

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
    "Cadastrar item musical",
    "Cadastrar cliente",
    "Cadastrar vendedor",
    "Buscar itens musicais",
    "Listar itens musicais",
    "Realizar compra",
    "Ver dados do cliente",
    "Ver pedidos do cliente",
    "Relatório mensal por vendedor",
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


def show_home_screen():
    return True


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
            try:
                key = readchar.readkey()
            except KeyboardInterrupt:
                return None

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


def _validate_optional_float(min_value=None, max_value=None):
    def validator(text):
        if text == "":
            return True, ""
        try:
            value = float(text)
        except ValueError:
            return False, "Entrada inválida. Deve ser um número."

        if not math.isfinite(value):
            return False, "Entrada inválida. Digite um número finito."

        if min_value is not None and value < min_value:
            return False, f"O valor deve ser no mínimo {min_value}."

        if max_value is not None and value > max_value:
            return False, f"O valor deve ser no máximo {max_value}."

        return True, value
    return validator


def _validate_optional_text(max_length=None):
    def validator(text):
        if text == "":
            return True, ""
        if max_length is not None and len(text) > max_length:
            return False, f"Esse campo pode ter no máximo {max_length} caracteres."
        return True, text
    return validator


def _validate_email(text):
    text = text.strip()

    if not text:
        return False, "Esse campo não pode ser vazio."

    if len(text) > 150:
        return False, "Esse campo pode ter no máximo 150 caracteres."

    if "@" not in text:
        return False, "Digite um e-mail válido."

    return True, text


def _validate_telefone(text):
    text = text.strip()

    if not text:
        return False, "Esse campo não pode ser vazio."

    if len(text) > 20:
        return False, "Esse campo pode ter no máximo 20 caracteres."

    if len(text) < 8:
        return False, "O telefone do cliente é inválido. Digite pelo menos 8 caracteres."

    return True, text


def _validate_tipo_midia(text):
    if not text:
        return False, "Esse campo não pode ser vazio."

    normalized = text.strip().upper()

    validos = {
        "CD": "CD",
        "DVD": "DVD",
        "VINIL": "VINIL",
        "CASSETE": "CASSETE",
    }

    if normalized not in validos:
        return False, "Digite apenas: CD, DVD, VINIL ou CASSETE."

    return True, validos[normalized]


def _validate_yes_no_or_empty(text):
    if text == "":
        return True, None

    normalized = text.strip().lower()
    if normalized in ("s", "sim", "y", "yes"):
        return True, True
    if normalized in ("n", "nao", "não", "no"):
        return True, False

    return False, "Digite S para sim, N para não, ou Enter para ignorar."


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


def prompt_produto_form():
    titulo_album = _input_text_in_panel(
        "Cadastrar item musical",
        "Título do álbum:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if titulo_album is None:
        return None

    artista = _input_text_in_panel(
        "Cadastrar item musical",
        "Artista:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if artista is None:
        return None

    categoria = _input_text_in_panel(
        "Cadastrar item musical",
        "Categoria musical:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if categoria is None:
        return None

    tipo_midia = _select_option_in_panel(
        "Cadastrar item musical",
        "Tipo de mídia:",
        ["CD", "DVD", "VINIL", "CASSETE"],
        helper_text="Escolha o tipo de mídia do item musical.",
    )
    if tipo_midia is None:
        return None

    ano_fabricacao = _input_text_in_panel(
        "Cadastrar item musical",
        "Ano de fabricação:",
        max_length=4,
        validator=_validate_int(min_value=1900, max_value=2026),
    )
    if ano_fabricacao is None:
        return None

    fabricado_em_mari = _input_text_in_panel(
        "Cadastrar item musical",
        "Fabricado em Mari? (S/N):",
        max_length=3,
        validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
    )
    if fabricado_em_mari is None:
        return None

    preco = _input_text_in_panel(
        "Cadastrar item musical",
        "Preço:",
        max_length=12,
        validator=_validate_float(min_value=0, max_value=1000000.99),
    )
    if preco is None:
        return None

    estoque = _input_text_in_panel(
        "Cadastrar item musical",
        "Estoque:",
        max_length=10,
        validator=_validate_int(min_value=0, max_value=10000),
    )
    if estoque is None:
        return None

    resumo = (
        f"[bold #d16d9e]Confira os dados:[/bold #d16d9e]\n\n"
        f"Título do álbum: {titulo_album}\n"
        f"Artista: {artista}\n"
        f"Categoria musical: {categoria}\n"
        f"Tipo de mídia: {tipo_midia}\n"
        f"Ano de fabricação: {ano_fabricacao}\n"
        f"Fabricado em Mari: {'Sim' if fabricado_em_mari else 'Não'}\n"
        f"Preço: {preco}\n"
        f"Estoque: {estoque}\n"
    )

    if not _confirm_in_panel("Confirmar cadastro", resumo):
        return None

    return {
        "titulo_album": titulo_album,
        "artista": artista,
        "categoria": categoria,
        "tipo_midia": tipo_midia,
        "ano_fabricacao": ano_fabricacao,
        "fabricado_em_mari": fabricado_em_mari,
        "preco": preco,
        "estoque": estoque,
    }


def prompt_cliente_form():
    nome = _input_text_in_panel(
        "Cadastrar cliente",
        "Nome:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if nome is None:
        return None

    email = _input_text_in_panel(
        "Cadastrar cliente",
        "E-mail:",
        max_length=150,
        validator=_validate_email,
    )
    if email is None:
        return None

    telefone = _input_text_in_panel(
        "Cadastrar cliente",
        "Telefone:",
        max_length=20,
        validator=_validate_telefone,
    )
    if telefone is None:
        return None

    cidade = _input_text_in_panel(
        "Cadastrar cliente",
        "Cidade:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if cidade is None:
        return None

    time_futebol = _input_text_in_panel(
        "Cadastrar cliente",
        "Time de futebol:",
        max_length=50,
        validator=_validate_non_empty(max_length=50),
    )
    if time_futebol is None:
        return None

    anime_favorito = _input_text_in_panel(
        "Cadastrar cliente",
        "Anime favorito:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if anime_favorito is None:
        return None

    resumo = (
        f"[bold #d16d9e]Confira os dados:[/bold #d16d9e]\n\n"
        f"Nome: {nome}\n"
        f"E-mail: {email}\n"
        f"Telefone: {telefone}\n"
        f"Cidade: {cidade}\n"
        f"Time de futebol: {time_futebol}\n"
        f"Anime favorito: {anime_favorito}\n"
    )

    if not _confirm_in_panel("Confirmar cadastro", resumo):
        return None

    return {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cidade": cidade,
        "time_futebol": time_futebol,
        "anime_favorito": anime_favorito,
    }


def prompt_vendedor_form():
    nome = _input_text_in_panel(
        "Cadastrar vendedor",
        "Nome:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if nome is None:
        return None

    email = _input_text_in_panel(
        "Cadastrar vendedor",
        "E-mail:",
        max_length=150,
        validator=_validate_email,
    )
    if email is None:
        return None

    ativo = _input_text_in_panel(
        "Cadastrar vendedor",
        "Vendedor ativo? (S/N):",
        max_length=3,
        validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
    )
    if ativo is None:
        return None

    return {
        "nome": nome,
        "email": email,
        "ativo": ativo,
    }


def prompt_busca_produtos_form():
    titulo_album = _input_text_in_panel(
        "Buscar itens musicais",
        "Título do álbum (opcional):",
        max_length=150,
        validator=_validate_optional_text(max_length=150),
    )
    if titulo_album is None:
        return None

    preco_min = _input_text_in_panel(
        "Buscar itens musicais",
        "Preço mínimo (opcional):",
        max_length=12,
        validator=_validate_optional_float(min_value=0),
    )
    if preco_min is None:
        return None

    preco_max = _input_text_in_panel(
        "Buscar itens musicais",
        "Preço máximo (opcional):",
        max_length=12,
        validator=_validate_optional_float(min_value=0),
    )
    if preco_max is None:
        return None

    categoria = _input_text_in_panel(
        "Buscar itens musicais",
        "Categoria musical (opcional):",
        max_length=100,
        validator=_validate_optional_text(max_length=100),
    )
    if categoria is None:
        return None

    tipo_midia = _input_text_in_panel(
        "Buscar itens musicais",
        "Tipo de mídia (opcional):",
        max_length=8,
        validator=lambda text: (True, "") if text == "" else _validate_tipo_midia(text),
    )
    if tipo_midia is None:
        return None

    fabricado_em_mari = _input_text_in_panel(
        "Buscar itens musicais",
        "Fabricado em Mari? (S/N ou Enter para ignorar):",
        max_length=5,
        validator=_validate_yes_no_or_empty,
    )
    if fabricado_em_mari is None:
        return None

    modo_funcionario = _input_text_in_panel(
        "Buscar itens musicais",
        "Busca como funcionário? (S/N):",
        max_length=3,
        validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
    )
    if modo_funcionario is None:
        return None

    somente_baixo_estoque = False
    if modo_funcionario:
        somente_baixo_estoque = _input_text_in_panel(
            "Buscar itens musicais",
            "Somente estoque < 5? (S/N):",
            max_length=3,
            validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
        )
        if somente_baixo_estoque is None:
            return None

    return {
        "titulo_album": titulo_album or None,
        "preco_min": preco_min,
        "preco_max": preco_max,
        "categoria": categoria or None,
        "tipo_midia": tipo_midia or None,
        "fabricado_em_mari": fabricado_em_mari,
        "somente_baixo_estoque": bool(somente_baixo_estoque),
    }


def prompt_compra_cliente_inline_form():
    nome = _input_text_in_panel(
        "Realizar compra",
        "Nome do cliente:",
        max_length=150,
        validator=_validate_non_empty(max_length=150),
    )
    if nome is None:
        return None

    email = _input_text_in_panel(
        "Realizar compra",
        "E-mail do cliente:",
        max_length=150,
        validator=_validate_email,
    )
    if email is None:
        return None

    telefone = _input_text_in_panel(
        "Realizar compra",
        "Telefone do cliente:",
        max_length=20,
        validator=_validate_telefone,
    )
    if telefone is None:
        return None

    cidade = _input_text_in_panel(
        "Realizar compra",
        "Cidade do cliente:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if cidade is None:
        return None

    time_futebol = _input_text_in_panel(
        "Realizar compra",
        "Time de futebol:",
        max_length=50,
        validator=_validate_non_empty(max_length=50),
    )
    if time_futebol is None:
        return None

    anime_favorito = _input_text_in_panel(
        "Realizar compra",
        "Anime favorito:",
        max_length=100,
        validator=_validate_non_empty(max_length=100),
    )
    if anime_favorito is None:
        return None

    return {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cidade": cidade,
        "time_futebol": time_futebol,
        "anime_favorito": anime_favorito,
    }


def _format_clientes_helper(clientes):
    if not clientes:
        return "Nenhum cliente cadastrado."

    linhas = ["Clientes cadastrados:"]
    for cliente in clientes:
        linhas.append(f"{cliente['id']} - {cliente['nome']}")
    return "\n".join(linhas)


def _format_vendedores_helper(vendedores):
    if not vendedores:
        return "Nenhum vendedor cadastrado."

    linhas = ["Vendedores cadastrados:"]
    for vendedor in vendedores:
        status = "ativo" if vendedor["ativo"] else "inativo"
        linhas.append(f"{vendedor['id']} - {vendedor['nome']} ({status})")
    return "\n".join(linhas)


def _format_formas_pagamento_helper(formas_pagamento):
    if not formas_pagamento:
        return "Nenhuma forma de pagamento cadastrada."

    linhas = ["Formas de pagamento:"]
    for forma in formas_pagamento:
        linhas.append(f"{forma['id']} - {forma['nome']}")
    return "\n".join(linhas)


def _format_produtos_helper(produtos):
    if not produtos:
        return "Nenhum item musical cadastrado."

    linhas = ["Itens musicais cadastrados:"]
    for produto in produtos:
        linhas.append(f"{produto['id']} - {produto['nome']}")
    return "\n".join(linhas)


def _buscar_nome_por_id(registros, registro_id, campo_nome="nome"):
    for registro in registros or []:
        if registro["id"] == registro_id:
            return registro[campo_nome]
    return None


def prompt_compra_form(clientes=None, vendedores=None, formas_pagamento=None, produtos=None):
    cliente_cadastrado = _input_text_in_panel(
        "Realizar compra",
        "Cliente já cadastrado? (S/N):",
        max_length=3,
        validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
    )
    if cliente_cadastrado is None:
        return None

    cliente_id = None
    cliente = None

    if cliente_cadastrado:
        cliente_id = _input_text_in_panel(
            "Realizar compra",
            "ID do cliente:",
            max_length=10,
            helper_text=_format_clientes_helper(clientes),
            validator=_validate_int(min_value=1),
        )
        if cliente_id is None:
            return None
    else:
        cliente = prompt_compra_cliente_inline_form()
        if cliente is None:
            return None

    vendedor_id = _input_text_in_panel(
        "Realizar compra",
        "ID do vendedor:",
        max_length=10,
        helper_text=_format_vendedores_helper(vendedores),
        validator=_validate_int(min_value=1),
    )
    if vendedor_id is None:
        return None

    forma_pagamento_id = _input_text_in_panel(
        "Realizar compra",
        "ID da forma de pagamento:",
        max_length=10,
        helper_text=_format_formas_pagamento_helper(formas_pagamento),
        validator=_validate_int(min_value=1),
    )
    if forma_pagamento_id is None:
        return None

    itens = []
    while True:
        produto_id = _input_text_in_panel(
            "Realizar compra",
            f"ID do item musical #{len(itens) + 1}:",
            max_length=10,
            helper_text=_format_produtos_helper(produtos),
            validator=_validate_int(min_value=1),
        )
        if produto_id is None:
            return None

        quantidade = _input_text_in_panel(
            "Realizar compra",
            f"Quantidade do item #{len(itens) + 1}:",
            max_length=10,
            validator=_validate_int(min_value=1, max_value=1000),
        )
        if quantidade is None:
            return None

        itens.append(
            {
                "produto_id": produto_id,
                "quantidade": quantidade,
            }
        )

        adicionar_mais = _input_text_in_panel(
            "Realizar compra",
            "Adicionar mais um item? (S/N):",
            max_length=3,
            validator=lambda text: _validate_yes_no_or_empty(text) if text else (False, "Esse campo não pode ser vazio."),
        )
        if adicionar_mais is None:
            return None

        if not adicionar_mais:
            break

    observacao = _input_text_in_panel(
        "Realizar compra",
        "Observação (opcional):",
        max_length=255,
        validator=_validate_optional_text(max_length=255),
    )
    if observacao is None:
        return None
    
    cliente_nome = _buscar_nome_por_id(clientes, cliente_id) if cliente_id is not None else None
    vendedor_nome = _buscar_nome_por_id(vendedores, vendedor_id)
    forma_pagamento_nome = _buscar_nome_por_id(formas_pagamento, forma_pagamento_id)

    resumo_linhas = []
    if cliente_id is not None:
        if cliente_nome:
            resumo_linhas.append(f"Cliente: {cliente_id} - {cliente_nome}")
        else:
            resumo_linhas.append(f"Cliente ID: {cliente_id}")

        resumo_linhas.extend(
        [
            f"Vendedor: {vendedor_id} - {vendedor_nome if vendedor_nome else 'não encontrado na lista'}",
            f"Forma de pagamento: {forma_pagamento_id} - {forma_pagamento_nome if forma_pagamento_nome else 'não encontrada na lista'}",
            "",
            "Itens:",
        ]
    )

    for indice, item in enumerate(itens, start=1):
        produto_nome = _buscar_nome_por_id(produtos, item["produto_id"])
        if produto_nome:
            resumo_linhas.append(
                f"{indice}. Produto {item['produto_id']} - {produto_nome} | Quantidade: {item['quantidade']}"
            )
        else:
            resumo_linhas.append(
                f"{indice}. Produto ID {item['produto_id']} | Quantidade: {item['quantidade']}"
            )

    if observacao:
        resumo_linhas.extend(["", f"Observação: {observacao}"])

    if not _confirm_in_panel("Confirmar compra", "\n".join(resumo_linhas)):
        return None

    return {
        "cliente_id": cliente_id,
        "cliente": cliente,
        "vendedor_id": vendedor_id,
        "forma_pagamento_id": forma_pagamento_id,
        "itens": itens,
        "observacao": observacao or None,
    }


def prompt_cliente_id(title):
    return _input_text_in_panel(
        title,
        "ID do cliente:",
        max_length=10,
        validator=_validate_int(min_value=1),
    )


def _render_select_screen(label, options, selected_index, helper_text="", error_text=None):
    lines = [f"[bold #d16d9e]{label}[/bold #d16d9e]", ""]

    for i, option in enumerate(options):
        if i == selected_index:
            lines.append(f"[bold #d16d9e]❯ {option}[/bold #d16d9e]")
        else:
            lines.append(f"  {option}")

    lines.append("")
    lines.append("[dim]↑ ↓ para navegar • Enter para confirmar • Esc para cancelar[/dim]")

    if helper_text:
        lines.extend(["", f"[dim]{helper_text}[/dim]"])

    if error_text:
        lines.extend(["", f"[bold red]{error_text}[/bold red]"])

    return "\n".join(lines)


def _select_option_in_panel(title, label, options, helper_text=""):
    selected_index = 0

    with Live(
        build_layout(title, _render_select_screen(label, options, selected_index, helper_text)),
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

            if key == readchar.key.UP:
                selected_index = (selected_index - 1) % len(options)
                live.update(
                    build_layout(title, _render_select_screen(label, options, selected_index, helper_text)),
                    refresh=True,
                )

            elif key == readchar.key.DOWN:
                selected_index = (selected_index + 1) % len(options)
                live.update(
                    build_layout(title, _render_select_screen(label, options, selected_index, helper_text)),
                    refresh=True,
                )

            elif key in (readchar.key.ENTER, readchar.key.CR, readchar.key.LF):
                return options[selected_index]