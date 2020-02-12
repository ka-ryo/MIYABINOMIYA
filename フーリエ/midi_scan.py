import pretty_midi
import numpy as np
import os.path
import pathlib

def main(midi_file_name):
    hight = 128
    width = 150
    np.set_printoptions(threshold=np.inf)
    
    #midiデータを読み込む
    midi_file = pretty_midi.PrettyMIDI(str(midi_file_name))

    #midiデータ（ピアノ）をNumpyで保存
    midi_numpy = midi_file.get_piano_roll()

    if midi_numpy.shape[1] > 150 and "ori" in (str(midi_file_name)) :
        print(os.path.splitext(midi_file_name)[0])
        #print(midi_numpy.shape)
    """
    if midi_numpy.shape[1] != width:
        print(width-midi_numpy.shape[1])
        zero_array = np.zeros((hight,width-midi_numpy.shape[1]))
        midi_numpy=np.hstack((midi_numpy,zero_array))
    
    
    #intへ変更
    int64_midi_numpy = midi_numpy.astype(np.int64)

    print(np.shape(midi_numpy))

    bool_midi_file = (midi_numpy > 0)
    one_hot_vector_midi = bool_midi_file.astype(np.int)
    #print(one_hot_vector_midi.ndim)
    #print(one_hot_vector_midi.T)

    #txt保存
    
    np.savetxt('{}.txt'.format(os.path.splitext(midi_file_name)[0]),one_hot_vector_midi,fmt="%2.1d")
    input()
    return one_hot_vector_midi
    """
if __name__ == '__main__':
    #originalとpracticeのパスを取得する
    first_dir = os.getcwd()
    #結果のフォルダーパス
    Result_Path = pathlib.Path('Result')
    #クラスのフォルダーパス
    Class_Folder_Paths = pathlib.Path(Result_Path).glob('[0-9]')
    
    for Class_Folder_Path in Class_Folder_Paths:
        #曲の名前のフォルダーパス
        Music_name_paths =pathlib.Path(Class_Folder_Path).glob('*')
        for Music_name_path in Music_name_paths:
            #練習曲の番号のパス
            Music_Number_Paths = pathlib.Path(Music_name_path).glob('*')
            for Music_Number_Path in Music_Number_Paths:
                Original_Path = list(pathlib.Path(Music_Number_Path).glob('original*mid'))[0].resolve()
                Practice_Path = list(pathlib.Path(Music_Number_Path).glob('practice*mid'))[0].resolve()
                os.chdir(Music_Number_Path)  
                main(Original_Path)
                main(Practice_Path)
                os.chdir(first_dir)


    