import music21 as m21
import os
import pathlib
import shutil


def Split(filename):
    print(filename)
    #original
    original_midi_data = m21.converter.parse("{}/original.mid".format(filename))
    original_midi_data.write('musicxml',"{}/original.xml".format(filename))
    original_piece= m21.converter.parse("{}/original.xml".format(filename))
    print("original pass")
    #practice
    practice_midi_data = m21.converter.parse("{}/practice.mid".format(filename))
    practice_midi_data.write('musicxml',"{}/practice.xml".format(filename))
    practice_piece= m21.converter.parse("{}/practice.xml".format(filename))

    if len(original_piece[1]) != len(practice_piece[1]):
       shutil.rmtree("{}".format(filename))
    



if __name__ == "__main__":
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    #print(first_dir)
    music_name_path = pathlib.Path('./').glob('[a-zA-Z0-9]*')

    for name1 in music_name_path:
        practice_numbers = pathlib.Path('./',name1.name).glob('*')
        for practice_number in practice_numbers:
            Save_Path = practice_number.resolve()
            Midi_Folders = pathlib.Path('{}/'.format(Save_Path)).glob('*.mid')
            Split(practice_number)

    