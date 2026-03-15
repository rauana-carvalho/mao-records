import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_home_screen():
    clear_screen()

    left = [
        "                  ▒██▓░",
        "                  ▒███▒ ░░███░░   ░██░░",
        "                  ▒███▓░▒█████▓▓▓▓████▒",
        "                  ▒████▒▓█████████████▒",
        "                 ░▒███████████████████▓░",
        "               ░▒█████████████▒████▒███░",
        "              ░▒███████████████████████░",
        "              ░██████████████████████▓░",
        "             ░▓██████████████████████▒",
        "            ░▒████████████████████████░",
        "             ████▓░░░░▓████████░░▒█████▒",
        "            ░███▓░   ░▓█████░     ░▓████░",
        "                     ░▓████░",
    ]

    right = [
"   _",
" _( )_",
"(_ o _)",
" (_,_)",
        "\t   ███    ███  █████   ██████      ██████  ███████  ██████  ██████  ██████  ███████",
        "\t   ████  ████ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██ ██",
        "\t   ██ ████ ██ ███████ ██    ██     ██████  █████   ██      ██    ██ ██████  ███████",
        "\t   ██  ██  ██ ██   ██ ██    ██     ██   ██ ██      ██      ██    ██ ██   ██      ██",
        "\t   ██      ██ ██   ██  ██████      ██   ██ ███████  ██████  ██████  ██   ██ ███████",
                                                                                            "\t\t\t\t\t\t\t\t\t\t           _",
                                                                                            "\t\t\t\t\t\t\t\t\t\t         _( )_",
                                                                                            "\t\t\t\t\t\t\t\t\t\t        (_ o _)",
                                                                                            "\t\t\t\t\t\t\t\t\t\t         (_,_)",
        "",
    ]

    padding = 5
    top_margin = 3
    left_width = max(len(line) for line in left)

    print("\n" * top_margin, end="")

    for i in range(max(len(left), len(right))):
        l = left[i] if i < len(left) else ""
        r = right[i] if i < len(right) else ""
        print(l.ljust(left_width + padding) + r)

    print("\n" + " " * 71 + "[ Enter ]")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nEncerrando sistema...\n")
        return False

    clear_screen()
    return True