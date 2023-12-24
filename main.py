"""
<<<<<<< HEAD
Mistet den Download-Ordner aus, indem alle Dateien älter als n Tage verschoben werden.
=======
Mistet den Download-Ordner aus, indem alle Dateien älter als n Tage in einen seperaten Ordner verschoben werden.
>>>>>>> 3d2fb7e63daeebe61d132ec2aa5cc22806df12ce
"""

import pendulum
import os
import shutil

from rich.console import Console

# Pfad zum Download-Ordner
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


# Prüft ob Datei älter als n Tage ist
def old_file(file, days: int = 3) -> bool:
    now = pendulum.now("Europe/Zurich")
    return now - pendulum.from_timestamp(os.path.getctime(file)) > pendulum.duration(
        days=days
    )


# Gibt Liste mit Ordnern zurück
def get_directories(working_path) -> list:
    directories = []
    for data in os.listdir(working_path):
        if os.path.isdir(data):
            directories.append(data)
    return directories


# Gibt Liste mit Dateien zurück
def get_files(working_path) -> list:
    files = []
    for data in os.listdir(working_path):
        if os.path.isfile(data):
            files.append(data)
    return files


if __name__ == "__main__":
    working_path = DOWNLOADS_PATH

    oldfilesdays: int = 14
    oldfiles = []
    sortbydate: bool = False

    os.chdir(working_path)

    console = Console()
    console.print(f"\nPath: [underline]{os.getcwd()}[/underline]\n")

    # Anwenderabfrage
    days = input(f"Wie alt dürfen die Dateien sein? [{oldfilesdays} Tage] ")
    if days.isnumeric():
        oldfilesdays = int(days)
    dat_sort = input("Dateien nach Datum sortieren? [n] ")
    if dat_sort.lower() in ["y", "j"]:
        sortbydate = True
    else:
        sortbydate = False
    print()

    # Fügt alle Ordner einer Liste hinzu
    directories = get_directories(working_path)
    for dir in directories:
        console.print(f"{dir}", style="underline")

    # Fügt alle Dateien einer Liste hinzu
    files = get_files(working_path)
    # Sortiert Dateien nach Datum
    if sortbydate:
        files.sort(key=os.path.getctime, reverse=True)
    for file in files:
        if old_file(file, oldfilesdays):
            oldfiles.append(file)
            console.print(f"{file}", style="red")
        else:
            console.print(f"{file}", style="white")

    print()

    now = pendulum.now("Europe/Zurich")
    dir_to_delete = f"{now.format('YYYYMMDD')}_to_delete"

    # Anwenderabfrage wenn alte Dateien vorhanden
    if oldfiles:
        dat_del = console.input(
            f"Dateien älter als [red]{oldfilesdays} Tage[/red] in Ordner [underline]\\{dir_to_delete}[/underline] verschieben? \[n] "
        )
        if dat_del.lower() in ["y", "j"]:
            new_dir = os.path.join(working_path, dir_to_delete)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            # Dateien verschieben
            for file in oldfiles:
                old_path = os.path.join(working_path, file)
                new_path = os.path.join(new_dir, file)
                shutil.move(old_path, new_path)

            print(f"{len(oldfiles)} Dateien verschoben.")
        else:
            print("Keine Dateien verschoben.")
    else:
        print(f"Keine Dateien älter als {oldfilesdays} Tage gefunden.")
