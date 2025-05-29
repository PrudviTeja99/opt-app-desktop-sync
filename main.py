import os
import json
from pathlib import Path

APPS_DIR = Path('/opt/apps')
DESKTOP_DIR = Path.home() / '.local' / 'share' / 'applications'
TRACKED_FILE_NAME = 'installed_apps_tracker.json'
TRACKED_FILE = DESKTOP_DIR / TRACKED_FILE_NAME

def fetch_desktop_entry_template(program_metadata):

    template = f"""
    [Desktop Entry]
    Type=Application
    Name={program_metadata["program_name"]}
    Exec={program_metadata["program_exec_path"]}
    Icon={program_metadata["program_icon_path"]}
    Comment=Installed program from /opt/apps
    Categories=Application;
    Terminal=false
    """

    return template

def load_tracked_file():
    print('Loading tracked file...')
    if TRACKED_FILE.exists():
        with open(TRACKED_FILE) as f:
            return json.load(f)
    else:
        with open(TRACKED_FILE, 'w') as f:
            json.dump({},f)
        return {}

def save_tracked_file(updated_tracked_file_content):
    print('Saving tracked file...')
    with open(TRACKED_FILE, 'w') as f:
        json.dump(updated_tracked_file_content,f)


def create_desktop_file(desktop_entry,program_name):
    print(f"Creating desktop file for {program_name}")
    program_desktop_entry_path = DESKTOP_DIR / f"{program_name}.desktop"
    with open(program_desktop_entry_path,'w') as f:
        f.write(desktop_entry.strip())


def remove_desktop_file():
    print('Removing desktop file.')

def fetch_installed_programs():
    print('Fetching installed programs...')
    if APPS_DIR.exists():
        programs_list = [d for d in APPS_DIR.iterdir() if d.is_dir()]
    else :
        programs_list = []

    return programs_list

def processing(installed_programs, tracked_file):
    print('Processing installed programs...')
    for program in installed_programs:
        if program.name not in tracked_file:
            print('Processing ' + program.name)
            program_bin = program / 'bin'
            program_exec_path = program_bin / program.name
            program_icon_path = next(program_bin.glob("*.svg"),None)
            program_metadata = {'program_name': program.name,'program_exec_path': program_exec_path,'program_icon_path': program_icon_path}
            create_desktop_file(fetch_desktop_entry_template(program_metadata),program.name)


if __name__ == '__main__':

    installed_programs = fetch_installed_programs()
    tracked_file = load_tracked_file()

    processing(installed_programs, tracked_file)




