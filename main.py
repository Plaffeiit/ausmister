"""
Mistet den Download-Ordner aus, indem alle Dateien älter als n Tage in einen separaten Ordner verschoben werden.
"""

import datetime
import os
import shutil

# Pfad zum Download-Ordner
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


# Prüft ob Datei älter als n Tage ist
def old_file(file, days: int = 3) -> bool:
    now = datetime.datetime.now()
    file_time = datetime.datetime.fromtimestamp(os.path.getctime(file))
    return (now - file_time).days > days


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

    print(f"\nPath: {os.getcwd()}\n")

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
        print(f"<{dir}>")

    # Fügt alle Dateien einer Liste hinzu
    files = get_files(working_path)
    # Sortiert Dateien nach Datum
    if sortbydate:
        files.sort(key=os.path.getctime, reverse=True)
    for file in files:
        if old_file(file, oldfilesdays):
            oldfiles.append(file)
            print(f"* {file} *")
        else:
            print(f"{file}")

    print()

    now = datetime.datetime.now()
    dir_to_delete = f"delete_{now.strftime('%Y%m%d')}"

    # Anwenderabfrage wenn alte Dateien vorhanden
    if oldfiles:
        dat_del = input(
            f"Die mit einem * markierten Dateien sind älter als {oldfilesdays} Tage.\nDiese in Ordner <{dir_to_delete}> verschieben? \[n] "
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
