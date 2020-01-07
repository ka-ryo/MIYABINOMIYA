import pathlib
import subprocess
import os
import pyautogui as pgui
import time
import pyperclip

def savepdf(path):
    #subprocess.Popen(path, shell=True)
    pyperclip.copy(str(path.parent))
    subprocess.Popen('{}'.format(path), shell=True)
    
    time.sleep(5)

    pgui.keyDown('ctrl')
    pgui.keyDown('shift')
    pgui.keyDown('alt')
    pgui.keyDown('e')
    pgui.keyUp('ctrl')
    pgui.keyUp('shift')
    pgui.keyUp('alt')
    pgui.keyUp('e')

    pgui.keyDown('alt')
    pgui.keyDown('d')
    pgui.keyUp('alt')
    pgui.keyUp('d')

    pgui.keyDown('ctrl')
    pgui.keyDown('v')
    pgui.keyUp('ctrl')
    pgui.keyUp('v')

    pgui.typewrite(['enter'])

    pgui.keyDown('alt')
    pgui.keyDown('t')
    pgui.keyUp('alt')
    pgui.keyUp('t')

    pgui.typewrite(['down','w','enter'])

    time.sleep(3)

    pgui.keyDown('alt')
    pgui.keyDown('s')
    pgui.keyUp('alt')
    pgui.keyUp('s')

    time.sleep(2.5)

    pgui.keyDown('alt')
    pgui.keyDown('space')
    pgui.keyUp('alt')
    pgui.keyUp('space')

    pgui.typewrite(['c'])

    time.sleep(3)

if __name__ == "__main__":
    first_dir = os.getcwd()
    music_name_path = pathlib.Path('./').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('./',name1.name).glob('*')
        for name2 in practice_number:
            Save_Path = name2.resolve()
            Midi_Folders = pathlib.Path('{}/'.format(Save_Path)).glob('*.mid')
            for Midi_Folder in Midi_Folders:
                Do_check = list(pathlib.Path('{}/'.format(name2)).glob('{}.WAV'.format(Midi_Folder.stem)))
                print(Midi_Folder)
                
                if len(Do_check) == 0:
                    savepdf(Midi_Folder) 


        
