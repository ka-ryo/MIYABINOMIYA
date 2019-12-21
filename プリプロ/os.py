import pathlib
import os
import glob

music_name_path = pathlib.Path('Dataset').glob('*')
for name1 in music_name_path:
    practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
    for name2 in practice_number:
        Original =  list(pathlib.Path('Dataset/{}/{}/500/'.format(name1.name,name2.name)).glob('original.*'))
        Practice =  list(pathlib.Path('Dataset/{}/{}/500/'.format(name1.name,name2.name)).glob('Practice.*'))
        if(len(Original) != 0):
            print(Original[0].resolve())
        if(len(Practice) != 0):
            print(Practice[0].resolve())
    