import music21 as m21
import os
import pathlib
import subprocess
import shutil

def Split(filename,save):
    print(save)
    print(filename)
    shutil.move("./{}".format(filename), './{}'.format(save))
    #returncode = subprocess.Popen("{}".format(filename), shell=True)


if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    music_name_path = pathlib.Path('./').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('./',name1.name).glob('*')
        for name2 in practice_number:
            
            Save_Path = './{}/{}'.format(name1.name,name2.name)
            
            Original =  list(pathlib.Path('./{}/{}/120/'.format(name1.name,name2.name)).glob('original.*'))
            Practice =  list(pathlib.Path('./{}/{}/120/'.format(name1.name,name2.name)).glob('Practice.*'))
            Do_check = list(pathlib.Path('./{}/{}/120/'.format(name1.name,name2.name)).glob('*.xml'))
            if(len(Original) != 0 and len(Practice) != 0):
                Original_path=Original[0].resolve()
                Practice_path=Practice[0].resolve() 
                Split(Original[0],Save_Path)
                Split(Practice[0],Save_Path)
                shutil.rmtree("{}/120".format(Save_Path))
                shutil.rmtree("{}/500".format(Save_Path))
                os.chdir(first_dir)
            