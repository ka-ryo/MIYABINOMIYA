import music21 as m21
import os
import pathlib


def Split(filename):
    #original
    
    midi_data = m21.converter.parse("{}.mid".format(filename))
    fn = midi_data.write('musicxml',"./{}.xml".format(filename))
    piece= m21.converter.parse("{}.xml".format(filename))

    measure = 0
    for syousetu in piece[1]:
        if measure != 0:
            syousetu.write('midi',"./{}_{}.mid".format(filename,measure))
        measure=measure+1



if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    #print(first_dir)
    music_name_path = pathlib.Path('Dataset').glob('*')
    for name1 in music_name_path:
        practice_number = pathlib.Path('Dataset/',name1.name).glob('*')
        for name2 in practice_number:
            print(name2)
            Save_Path = 'Dataset/{}/{}/'.format(name1.name,name2.name)
            Original =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('original.*'))
            Practice =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('Practice.*'))
            Do_check =  list(pathlib.Path('Dataset/{}/{}/'.format(name1.name,name2.name)).glob('original_1.*'))
            if(len(Original) != 0 and len(Practice) != 0 and len(Do_check) == 0):
                Original_path=Original[0].resolve()
                Practice_path=Practice[0].resolve()
                print(Practice_path)
                os.chdir(Save_Path)    
                Split("original")
                Split("practice")
                os.chdir(first_dir)