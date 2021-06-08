import PySimpleGUI as sg
import subprocess
from datetime import date

sg.theme("SystemDefault")

def pkgutil_cli(pid, command):
    output = subprocess.check_output(['bash','-c', f"pkgutil {command} {pid}"])
    output = str(output)
    output = (output[2:][:len(output)-5].split("\\n"))
    print(output)
    return output

def getPackageFiles(pid):
    return pkgutil_cli(pid, "--files")

def getPackageInfo(pid):
    output = pkgutil_cli(pid, "--pkg-info")
    result = []
    for item in output:
        key, value = item.split(":")

        if(key == "install-time"):
            result.append(f"Installed date: {date.fromtimestamp(int(value))}")
            continue

        result.append(item)
    
    return result

last_package = ""

def ListPackageWindow():
    global last_package

    output = pkgutil_cli("", "--pkgs")

    menu_def = [['File', ['Open', 'Save', 'Exit',]],
                ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['Help', 'About...'],]

    layout = [
        [sg.Menu(menu_def)],
        [
            sg.Listbox(values=output, size=(55, 30), right_click_menu = ['&Right', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']], key="pak_listbox"),
            sg.Button("files >> ", key="show_files"),
            sg.Listbox(values=[], size=(55, 30), key='file_listbox')
        ],
        [ sg.Listbox(values=[], size=(121, 7), key="pak_info")]
    ]

    window = sg.Window("pkgutil - list package", layout, font=("SF Pro", 16), margins=(16, 16))

    while True:
        event, values = window.read()

        print(event, values)
        selected_package = values['pak_listbox']
        print(len(selected_package))

        package = values['pak_listbox'][0]

        if(event=="show_files"):
            if(last_package == package):
                continue
            
            last_package = package

            if(len(selected_package) == 0):
                sg.Popup("No package selected")
                continue
            window.Element('file_listbox').Update(values=getPackageFiles(package))
            window.Element('pak_info').Update(values=getPackageInfo(package))

        if(event == "Exit" or event == sg.WIN_CLOSED):
            break

if __name__ == "__main__":
    ListPackageWindow()