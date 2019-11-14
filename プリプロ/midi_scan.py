import pretty_midi
import numpy as np

def main(midi_file_name):
    np.set_printoptions(threshold=np.inf)

    #midiデータを読み込む
    midi_file = pretty_midi.PrettyMIDI(midi_file_name)

    #midiデータ（ピアノ）をNumpyで保存
    midi_numpy = midi_file.get_piano_roll()

    #intへ変更
    int64_midi_numpy = midi_numpy.astype(np.int64)

    #print(np.shape(midi_numpy))

    bool_midi_file = (midi_numpy > 0)
    one_hot_vector_midi = (bool_midi_file.astype(np.int))
    #print(one_hot_vector_midi.ndim)

    #print(one_hot_vector_midi.T)

    #txt保存
    np.savetxt('{}.txt'.format(midi_file_name),one_hot_vector_midi,fmt="%2.1d")

    return one_hot_vector_midi
if __name__ == '__main__':
    main("Long_test.mid")
    