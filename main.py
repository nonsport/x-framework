import os
import sys
import asyncio
import json
import shutil
import argparse
import itertools
import random
import string
from colorama import init, Fore, Style
import apis

# Инициализация colorama для правильного отображения цветов в терминале
init(autoreset=True)

LOGO_LINES = [
    r"███████╗       ███████╗",
    r"╚███████╗     ███████╔╝",
    r" ╚███████╗   ███████╔╝ ",
    r"  ╚███████╗ ███████╔╝  ",
    r"   ╚██████████████╔╝   ",
    r"    ╚████████████╔╝    ",
    r"    ██████████████╗    ",
    r"   ███████╔████████╗   ",
    r"  ███████╔╝ ╚███████╗  ",
    r" ███████╔╝   ╚███████╗ ",
    r"███████╔╝     ╚███████╗",
    r"╚══════╝       ╚══════╝"
]

DESCRIPTION = "X-Framework | Advanced OSINT Architecture"
SEP_LINE = "═══════════════════════════════════════════════════════"

def get_padding(raw_length):
    cols = shutil.get_terminal_size().columns
    return max(0, (cols - raw_length) // 2)

def print_centered(colored_text, raw_length):
    print(" " * get_padding(raw_length) + colored_text)

def display_header():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\n")
    for line in LOGO_LINES:
        print_centered(f"{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}", len(line))
    print("\n")
    print_centered(f"{Fore.RED}{DESCRIPTION}{Style.RESET_ALL}", len(DESCRIPTION))
    print_centered(f"{Fore.RED}{SEP_LINE}{Style.RESET_ALL}", len(SEP_LINE))
    print("\n")

async def animate_startup():
    """Анимация загрузки: Glitch-эффект логотипа + загрузка модулей."""
    os.system('clear' if os.name == 'posix' else 'cls')
    sys.stdout.write("\033[?25l") # Скрываем курсор

    try:
        # 1. Эффект расшифровки (Glitch Reveal)
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        frames = 20

        for frame in range(frames):
            sys.stdout.write("\033[H") # Перемещаем курсор в левый верхний угол
            print("\n")
            for line in LOGO_LINES:
                pad = " " * get_padding(len(line))
                if frame < frames - 1:
                    threshold = frame / frames
                    # Рандомно заменяем символы логотипа на мусорные, пока фреймы идут
                    mixed = "".join(
                        char if char == " " else (char if random.random() < threshold else random.choice(chars))
                        for char in line
                    )
                    print(f"{pad}{Fore.RED}{mixed}{Style.RESET_ALL}")
                else:
                    print(f"{pad}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}")
            await asyncio.sleep(0.06)

        print("\n")
        print_centered(f"{Fore.RED}{DESCRIPTION}{Style.RESET_ALL}", len(DESCRIPTION))
        print("\n")

        # 2. Эффект загрузки модулей (Progress Bar)
        modules = [
            "DNS Resolver", "WHOIS Engine", "IP Geolocation",
            "Port Scanner", "Subdomain Hunter", "Email OSINT + HIBP",
            "Sherlock Username", "Shodan API", "Phone OSINT"
        ]
        loaded_text = []
        bar_width = 30

        for i, mod in enumerate(modules):
            sys.stdout.write("\033[H") # Обновляем экран поверх старого вывода
            print("\n")
            for line in LOGO_LINES:
                pad = " " * get_padding(len(line))
                print(f"{pad}{Fore.RED}{Style.BRIGHT}{line}{Style.RESET_ALL}")
            print("\n")
            print_centered(f"{Fore.RED}{DESCRIPTION}{Style.RESET_ALL}", len(DESCRIPTION))
            print("\n")

            progress = int(((i + 1) / len(modules)) * 100)
            filled = int((progress / 100) * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)

            header_str = "[ Open Source Intelligence Framework v3.0 ]"
            print_centered(f"{Fore.RED}{header_str}{Style.RESET_ALL}", len(header_str))

            bar_str = f"[{bar}] {progress}%"
            print_centered(f"{Fore.RED}[{Fore.LIGHTRED_EX}{bar}{Fore.RED}] {progress}%{Style.RESET_ALL}", len(bar_str))
            print("\n")

            # Выводим уже загруженные модули
            for loaded_mod in loaded_text:
                mod_line = f"* {loaded_mod:<25} [LOADED]"
                print_centered(f"{Fore.RED} * {Fore.WHITE}{loaded_mod:<25} {Fore.LIGHTRED_EX}[LOADED]{Style.RESET_ALL}", len(mod_line))

            # Текущий модуль в процессе загрузки (ИСправлен цвет на LIGHTBLACK_EX)
            curr_line = f"* {mod:<25} [......]"
            print_centered(f"{Fore.RED} * {Fore.WHITE}{mod:<25} {Fore.LIGHTBLACK_EX}[......]{Style.RESET_ALL}", len(curr_line))

            loaded_text.append(mod)
            await asyncio.sleep(0.2)

        await asyncio.sleep(0.6) # Небольшая пауза перед открытием меню

    finally:
        sys.stdout.write("\033[?25h") # Возвращаем курсор обратно

async def run_module(coro, target):
    search_title = f"❖ Выполнение: {target} ❖"
    print("\n")
    print_centered(f"{Fore.LIGHTRED_EX}{search_title}{Style.RESET_ALL}", len(search_title))
    print_centered(f"{Fore.RED}└{'─'* (len(search_title) + 2)}┘{Style.RESET_ALL}", len(search_title) + 4)
    print("\n")

    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    task = asyncio.create_task(coro)

    pad = " " * get_padding(40)
    while not task.done():
        sys.stdout.write(f"\r{pad}{Fore.LIGHTRED_EX}{next(spinner)} {Fore.WHITE}Обработка данных...{Style.RESET_ALL}")
        sys.stdout.flush()
        await asyncio.sleep(0.1)

    sys.stdout.write(f"\r{' ' * shutil.get_terminal_size().columns}\r")
    results = task.result()

    for mod, data in results.items():
        status_icon = "✔" if "error" not in str(data).lower() else "✖"
        status_color = Fore.LIGHTRED_EX if status_icon == "✔" else Fore.RED

        print(f"{Fore.RED}╔══ {status_color}{status_icon} Модуль: {Fore.WHITE}{mod}{Style.RESET_ALL}")

        clean_text = json.dumps(data, indent=2, ensure_ascii=False)
        for line in clean_text.splitlines():
            print(f"{Fore.RED}║ {Fore.WHITE}{line}{Style.RESET_ALL}")
        print(f"{Fore.RED}╚{'═'*40}{Style.RESET_ALL}\n")

    with open("x_results.json", "a", encoding="utf-8") as f:
        f.write(json.dumps({target: results}, ensure_ascii=False) + "\n")

async def menu():
    await animate_startup() # Запуск анимации при старте

    while True:
        display_header()

        menu_items = [
            (f"{Fore.RED}╔══════════════════════════════════════╗", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[1] {Fore.WHITE}IP & Infrastructure Search      {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[2] {Fore.WHITE}Domain & Email Search         {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[3] {Fore.WHITE}Phone & Identity Search       {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[4] {Fore.WHITE}Username Global Scan          {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[5] {Fore.WHITE}Google Dorks Generator        {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[6] {Fore.WHITE}Generate Fake Identity        {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[7] {Fore.WHITE}Password Generator            {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.LIGHTRED_EX}[8] {Fore.WHITE}Base64 Encoder / Decoder      {Fore.RED}║", 40),
            (f"{Fore.RED}║  {Fore.RED}[0] {Fore.WHITE}Exit Framework                {Fore.RED}║", 40),
            (f"{Fore.RED}╚══════════════════════════════════════╝", 40)
        ]

        for colored_line, raw_len in menu_items:
            print_centered(colored_line, raw_len)

        print("\n")

        pad = " " * get_padding(40)
        choice = input(f"{pad}{Fore.LIGHTRED_EX}➤ X-Terminal > {Fore.WHITE}")

        if choice == '1':
            target = input(f"{pad}{Fore.RED}❖ Введите IP: {Fore.WHITE}")
            await run_module(apis.scan_ip(target), f"IP: {target}")
        elif choice == '2':
            target = input(f"{pad}{Fore.RED}❖ Введите Домен: {Fore.WHITE}")
            await run_module(apis.scan_domain(target), f"Domain: {target}")
        elif choice == '3':
            target = input(f"{pad}{Fore.RED}❖ Введите Номер: {Fore.WHITE}")
            await run_module(apis.scan_phone(target), f"Phone: {target}")
        elif choice == '4':
            target = input(f"{pad}{Fore.RED}❖ Введите Username: {Fore.WHITE}")
            await run_module(apis.scan_username(target), f"User: {target}")
        elif choice == '5':
            target = input(f"{pad}{Fore.RED}❖ Введите Домен для Dorks: {Fore.WHITE}")
            await run_module(apis.google_dorks_scan(target), f"Dorks: {target}")
        elif choice == '6':
            target = input(f"{pad}{Fore.RED}❖ Введите локаль (ru_RU/en_US) [Enter=ru_RU]: {Fore.WHITE}") or 'ru_RU'
            await run_module(apis.get_fake_identity_async(target), f"Identity [{target}]")
        elif choice == '7':
            try:
                length = int(input(f"{pad}{Fore.RED}❖ Длина пароля (6-32): {Fore.WHITE}"))
                pwd = apis.generate_password(length)
                print(f"\n{pad}{Fore.GREEN}✔ Сгенерированный пароль: {Fore.WHITE}{pwd}")
            except ValueError:
                print(f"\n{pad}{Fore.RED}✖ Ошибка: Введите число!")
        elif choice == '8':
            action = input(f"{pad}{Fore.RED}❖ [1] Кодировать (Encode) | [2] Декодировать (Decode) : {Fore.WHITE}")
            text = input(f"{pad}{Fore.RED}❖ Введите текст: {Fore.WHITE}")
            if action == '1':
                await run_module(apis.b64_encode(text), "Base64 Encode")
            elif action == '2':
                await run_module(apis.b64_decode(text), "Base64 Decode")
        elif choice == '0':
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"{Fore.RED}Завершение работы...{Style.RESET_ALL}")
            break

        print("\n")
        input(f"{pad}{Fore.RED}[ {Fore.WHITE}Enter для возврата в меню {Fore.RED}]{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        asyncio.run(menu())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Прервано пользователем. Выход...{Style.RESET_ALL}")

