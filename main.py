import datetime as dt
import os
import shutil

from rich.console import Console

# ^  KONSTANTE: Pfad zu Downloads
DOWNLOADS_PATH = os.path.join(os.path.expanduser('~'), 'Downloads')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# ^ Prüft ob Datei älter als n Tage ist
def old_file(file, days=3):
    return dt.datetime.now() - dt.datetime.fromtimestamp(os.path.getctime(file)) > dt.timedelta(days)

def print_directories(console, working_path):
    directories = []
    for data in os.listdir(working_path):
        if os.path.isdir(data):
            directories.append(data)
            console.print(f'{data}', style='blue')
    return directories


# Main
def main():
    console = Console()
    working_path = DOWNLOADS_PATH
    sortbydate: bool = False
    showoldfiles: bool = False
    oldfilesdays: int = 3

    while True:
        clear_console()
        os.chdir(working_path)
        console.print(f'Path: [blue]{os.getcwd()}[/blue]\n')

        # Gibt alle Ordner blau aus und fügt sie einer Liste hinzu
        directories = print_directories(console, working_path)

        # Fügt Dateien einer Liste hinzu
        files = []
        for data in os.listdir():
            if os.path.isfile(data):
                files.append(data)

        # Bool: Sortiert Dateien nach Datum
        if sortbydate:
            files.sort(key=os.path.getctime, reverse=True)

        for file in files:
            # Bool: Markiert Dateien, die älter als n Tage sind
            if showoldfiles:
                if old_file(file, oldfilesdays):
                    console.print(f'{file}', style='red')
                else:
                    print(f'{file}')
            else:
                print(f'{file}')

        # Gibt Befehle aus
        print()
        console.print(f'Commands:', style='bold')

        console.print(f'{"sort":15}Sort by date: {sortbydate}')
        console.print(f'{"mark":15}Mark files older than {oldfilesdays} days: {showoldfiles}')
        print(f'{"open [name]":15}Open folder')
        print(f'{"up":15}Open the parent directory')
        print(f'{"reset":15}Reset path to Downloads')

        print(f'{"":15}---')
        print(f'{"del [name]":15}Delete file or folder')  # TODO: Implement delete file or folder
        console.print(f'{"del old":15}Delete files older than {oldfilesdays} days')  # TODO: Implement delete old files
        print(f'{"del all":15}Delete all files')  # TODO: Implement delete all files

        print(f'{"":15}---')
        print(f'{"quit":15}Quit')

        # Führt Eingabe aus
        cmd = console.input('\n[bold]cmd >>[/bold] ').lower()
        if cmd in ['quit', 'q']:  # * Beenden
            break
        elif cmd in ['sort', 's']:  # * Sortiere Dateien nach Datum
            sortbydate = not sortbydate
        elif cmd in ['mark', 'm']:  # * Markiere alte Dateien
            showoldfiles = not showoldfiles
        elif cmd in ['up', 'u']:  # * Öffne übergeordneten Ordner
            os.chdir('..')
            working_path = os.getcwd()
        elif cmd.split()[0] in ['open', 'o']:  # * Öffne Ordner
            # Prüft, ob Ordnername existiert
            try:
                os.chdir(working_path + '\\' + cmd.split()[1])
            except Exception:
                pass
            # Prüft ob Eingabe gültige Zahl ist und weisst Ordner zu
            try:
                if cmd.split()[1].isdigit():
                    os.chdir(working_path + '\\' + directories[int(cmd.split()[1]) - 1])
            except Exception:
                pass
            # Wenn True, dann öffne Ordner
            working_path = os.getcwd()
        elif cmd in ['reset', 'r']:  # *Setze Pfad zu Downloads zurück
            working_path = DOWNLOADS_PATH


# Startet main()
if __name__ == '__main__':
    main()

# os.remove('main.py')
# os.rmdir('src')
# shutil.rmtree('venv')
