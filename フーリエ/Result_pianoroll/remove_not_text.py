import pretty_midi
import numpy as np
import os.path
import pathlib

#ピアノロール以外のファイルを削除します
    
if __name__ == '__main__':
    #結果のフォルダーパス
    Result_Paths = pathlib.Path('').glob('[0-9]')

    for Result_Path in Result_Paths:
        #曲の名前のフォルダーパス
        Music_name_paths =pathlib.Path(Result_Path).glob('*')
        for Music_name_path in Music_name_paths:
            #練習曲の番号のパス
            Music_Number_Paths = pathlib.Path(Music_name_path).glob('*')
            for Music_Number_Path in Music_Number_Paths:
                file_names = pathlib.Path(Music_Number_Path).glob('*')
                for file_name in file_names:
                    if ('txt' in str(file_name)) and (('original' in str(file_name)) or ('practice' in str(file_name))):
                        print(file_name)
                    else:
                        os.remove(file_name)
                


    