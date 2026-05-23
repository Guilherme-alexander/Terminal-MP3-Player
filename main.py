# =========================================================== #
# Terminal-MP3-Player (Terminal MP3 Player)                   #
# @Guilherme-alexander                                        #
# https://github.com/Guilherme-alexander/Terminal-MP3-Player  #
# =========================================================== #

import curses
import os
import threading
import time
import pygame

from mutagen.mp3 import MP3
from rich.console import Console

# =========================================
# BANNER
# =========================================

console = Console()

LOGO = """
 [bold #4DA3FF]████████╗███╗   ███╗██████╗[/]
 [bold #4DA3FF]╚══██╔══╝████╗ ████║██╔══██╗[/]
 [#7BB8FF]   ██║   ██╔████╔██║██████╔╝[/]
 [#7BB8FF]   ██║   ██║╚██╔╝██║██╔═══╝[/]
 [#BFC9D9]   ██║   ██║ ╚═╝ ██║██║[/]
 [#BFC9D9]   ╚═╝   ╚═╝     ╚═╝╚═╝[/]
┌─────────────────────────────┐
|     [bold white]TERMINAL MP3 PLAYER[/]     |
└─────────────────────────────┘
"""

console.print(LOGO)

time.sleep(2)

os.system("cls" if os.name == "nt" else "clear")

# =========================================
# CONFIG
# =========================================

PATH = os.path.join(
    os.path.expanduser("~"),
    "Music"
)

musics_path = []

TOTAL_MUSICS = 15 # Número de músicas

pagina = 0
indice = 0
volume = 0.5

scan_done = False

# =========================================
# PYGAME
# =========================================

pygame.init()
pygame.mixer.init()

pygame.mixer.music.set_volume(volume)

# =========================================
# SCAN MUSIC
# =========================================

def scan_music():

    global scan_done

    for root, dirs, files in os.walk(PATH):

        for f in files:

            if f.lower().endswith(".mp3"):

                musics_path.append(
                    os.path.join(root, f)
                )

    musics_path.sort()

    scan_done = True

# =========================================
# UTILS
# =========================================

def format_time(sec):

    sec = max(0, int(sec))

    h = sec // 3600
    m = (sec % 3600) // 60
    s = sec % 60

    return f"{h:02}:{m:02}:{s:02}"

"""
def progress_bar(current, total, width=35):

    if total <= 0:
        return "-" * width

    ratio = min(1, max(0, current / total))

    fill = int(ratio * width)

    # ■ · █ ─
    return (
        "█" * fill +
        "─" * (width - fill)
    )
"""

def progress_bar(current, total, width=35):

    if total <= 0:
        return "-" * width

    ratio = min(1, max(0, current / total))

    fill = int(ratio * width)

    percent = int(ratio * 100)

    bar = (
        "█" * fill +
        "░" * (width - fill)
    )

    return f"{bar} {percent}%"

# =========================================
# COLORS
# =========================================

def setup_colors():

    curses.start_color()
    curses.use_default_colors()

    # Selected item
    curses.init_pair(
        1,
        curses.COLOR_BLACK,
        curses.COLOR_CYAN
    )

    # Blue text
    curses.init_pair(
        2,
        curses.COLOR_CYAN,
        -1
    )

    # White text
    curses.init_pair(
        3,
        curses.COLOR_WHITE,
        -1
    )

    # Gray/Blue divider
    curses.init_pair(
        4,
        curses.COLOR_BLUE,
        -1
    )

    # Title light blue
    curses.init_pair(
        5,
        curses.COLOR_CYAN,
        -1
    )

    # White background + black text
    curses.init_pair(
        6,
        curses.COLOR_BLACK,
        curses.COLOR_WHITE
    )

# =========================================
# PLAYER
# =========================================

def player_screen(stdscr, start_index):

    global volume

    current_index = start_index

    stdscr.nodelay(True)
    stdscr.timeout(100)

    while True:

        if current_index < 0:
            current_index = len(musics_path) - 1

        if current_index >= len(musics_path):
            current_index = 0

        music_path = musics_path[current_index]

        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play()

        audio = MP3(music_path)

        total = audio.info.length

        paused = False

        while True:

            pos = pygame.mixer.music.get_pos() / 1000

            if pos < 0:
                pos = 0

            stdscr.erase()

            h, w = stdscr.getmaxyx()

            setup_colors()

            title = "♫ TERMINAL MP3 PLAYER ♫"

            stdscr.attron(curses.color_pair(5))

            stdscr.addstr(
                1,
                max(0, (w // 2) - (len(title) // 2)),
                title
            )

            stdscr.attroff(curses.color_pair(5))

            # Divider
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(2, 0, "─" * (w - 1))
            stdscr.attroff(curses.color_pair(4))

            name = os.path.basename(music_path)

            stdscr.attron(curses.color_pair(2))

            stdscr.addstr(
                4,
                2,
                f"Music : {name[:w-12]}"
            )

            stdscr.attroff(curses.color_pair(2))

            bar = progress_bar(pos, total)

            stdscr.attron(curses.color_pair(3))

            stdscr.addstr(
                6,
                2,
                f"{format_time(pos)} [{bar}] {format_time(total)}"
            )

            stdscr.attroff(curses.color_pair(3))

            stdscr.attron(curses.color_pair(2))

            stdscr.addstr(
                10,
                2,
                f"Volume : {int(volume * 100)}%"
            )

            stdscr.attroff(curses.color_pair(2))

            if paused:

                status = "PAUSED"

            else:

                status = "PLAYING"

            stdscr.attron(curses.color_pair(4))

            stdscr.addstr(
                8,
                2,
                f"Status : {status}"
            )

            stdscr.attroff(curses.color_pair(5))

            # Controls Box
            stdscr.attron(curses.color_pair(4))

            stdscr.addstr(
                13,
                2,
                "─" * 50
            )

            stdscr.attroff(curses.color_pair(4))

            stdscr.attron(curses.color_pair(3))

            stdscr.attron(curses.color_pair(3))

            stdscr.addstr(
                15,
                2,
                " SPACE Pause | S Stop | N Next | B Previous "
            )

            stdscr.addstr(
                16,
                2,
                " + - Volume | ESC Menu | Q Quit "
            )

            stdscr.attroff(curses.color_pair(3))

            stdscr.refresh()

            key = stdscr.getch()

            # ESC
            if key == 27:

                pygame.mixer.music.stop()
                return

            # SPACE
            elif key == ord(" "):

                if paused:

                    pygame.mixer.music.unpause()
                    paused = False

                else:

                    pygame.mixer.music.pause()
                    paused = True

            # STOP
            elif key in [ord("s"), ord("S")]:

                pygame.mixer.music.stop()
                paused = True

            # NEXT
            elif key in [ord("n"), ord("N")]:

                pygame.mixer.music.stop()

                current_index += 1

                break

            # PREVIOUS
            elif key in [ord("b"), ord("B")]:

                pygame.mixer.music.stop()

                current_index -= 1

                break

            # +
            elif key in [ord("+"), ord("=")]:

                volume = min(1.0, volume + 0.1)

                pygame.mixer.music.set_volume(volume)

            # -
            elif key == ord("-"):

                volume = max(0.0, volume - 0.1)

                pygame.mixer.music.set_volume(volume)

            # close          
            elif key in [ord("q"), ord("Q")]:

                 pygame.mixer.music.stop()
                 raise KeyboardInterrupt

            # Music ended
            if not pygame.mixer.music.get_busy() and not paused:

                current_index += 1

                break

            time.sleep(0.03)

# =========================================
# MENU
# =========================================

def menu(stdscr):

    global pagina
    global indice

    curses.curs_set(0)

    setup_colors()

    stdscr.nodelay(True)
    stdscr.timeout(100)

    while True:

        stdscr.erase()

        h, w = stdscr.getmaxyx()

        title = "♫ TERMINAL MP3 PLAYER ♫"

        stdscr.attron(curses.color_pair(5))

        stdscr.addstr(
            1,
            max(0, (w // 2) - (len(title) // 2)),
            title
        )

        stdscr.attroff(curses.color_pair(5))

        # Divider
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(2, 0, "─" * (w - 1))
        stdscr.attroff(curses.color_pair(4))

        if not scan_done:

            stdscr.attron(curses.color_pair(2))

            stdscr.addstr(
                5,
                2,
                "Scanning music files..."
            )

            stdscr.attroff(curses.color_pair(2))

            stdscr.refresh()

            time.sleep(0.1)

            continue

        total_paginas = max(
            1,
            (len(musics_path) - 1) // TOTAL_MUSICS + 1
        )

        pagina = max(
            0,
            min(pagina, total_paginas - 1)
        )

        inicio = pagina * TOTAL_MUSICS 
        fim = inicio + TOTAL_MUSICS 

        lista = musics_path[inicio:fim]

        for i, music in enumerate(lista):

            linha = 5 + i

            if linha >= h - 5:
                break

            nome = os.path.basename(music)

            if i == indice:

                stdscr.attron(
                    curses.color_pair(1)
                )

                stdscr.addstr(
                    linha,
                    4,
                    f"> {nome[:w-10]}"
                )

                stdscr.attroff(
                    curses.color_pair(1)
                )

            else:

                stdscr.attron(
                    curses.color_pair(3)
                )

                stdscr.addstr(
                    linha,
                    4,
                    f"  {nome[:w-10]}"
                )

                stdscr.attroff(
                    curses.color_pair(3)
                )

        stdscr.attron(curses.color_pair(4))

        stdscr.addstr(
            h - 4,
            2,
            "─" * 50
        )

        stdscr.attroff(curses.color_pair(4))

        stdscr.attron(curses.color_pair(2))

        stdscr.addstr(
            h - 3,
            2,
            f"Page {pagina+1}/{total_paginas}"
        )

        stdscr.attroff(curses.color_pair(2))

        stdscr.attron(curses.color_pair(3))

        stdscr.addstr(
            h - 2,
            2,
            "↑↓ Move | ←→ Pages | ENTER Play | ESC Exit"
        )

        stdscr.attroff(curses.color_pair(3))

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN and lista:

            indice = (
                indice + 1
            ) % len(lista)

        elif key == curses.KEY_UP and lista:

            indice = (
                indice - 1
            ) % len(lista)

        elif key == curses.KEY_RIGHT:

            if pagina < total_paginas - 1:

                pagina += 1
                indice = 0

        elif key == curses.KEY_LEFT:

            if pagina > 0:

                pagina -= 1
                indice = 0

        elif key == 10 and lista:

            real_index = (
                pagina * TOTAL_MUSICS + indice
            )

            if real_index < len(musics_path):

                player_screen(
                    stdscr,
                    real_index
                )

        elif key in [ord("q"), ord("Q")]:

            pygame.mixer.music.stop()
            raise KeyboardInterrupt
      
        elif key == 27:

            break

        time.sleep(0.02)

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    try:

        thread = threading.Thread(
            target=scan_music,
            daemon=True
        )

        thread.start()

        curses.wrapper(menu)

    except KeyboardInterrupt:

        pygame.mixer.music.stop()

        console.print("\n[bold #4DA3FF]Terminal MP3 Player closed.[/]")

    except Exception as e:

        console.print(f"[bold red]ERROR:[/] {e}")

        input("\nENTER to exit...")
