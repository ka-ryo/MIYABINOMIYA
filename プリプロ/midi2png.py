import music21 as m21
import os
import pathlib
import subprocess

def Split(filename):
    returncode = subprocess.Popen("{}.mid".format(filename), shell=True)


if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    #print(first_dir)
    music_name_path = pathlib.Path('Dataset').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            input()
            print(name2)
            Save_Path = 'Dataset/{}/{}/120'.format(name1.name,name2.name)
            Original =  list(pathlib.Path('Dataset/{}/{}/120/'.format(name1.name,name2.name)).glob('original.*'))
            Practice =  list(pathlib.Path('Dataset/{}/{}/120/'.format(name1.name,name2.name)).glob('Practice.*'))
            Do_check = list(pathlib.Path('Dataset/{}/{}/120/'.format(name1.name,name2.name)).glob('*.xml'))
            if(len(Original) != 0 and len(Practice) != 0):
                Original_path=Original[0].resolve()
                Practice_path=Practice[0].resolve()
                os.chdir(Save_Path)    
                Split("original")
                Split("practice")
                os.chdir(first_dir)