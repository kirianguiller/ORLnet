import pydub
import glob
import os
import pandas as pd

N_TO_PROCESS = 17000
path_project_data = '../data/'
path_source_data = "/home/wran/corpus/mozilla_voices/"
# languages = ['ru', 'nl', 'de']
# languages = ['nl']
languages = ['ru']

for lang in languages:
    path_dest_lang = os.path.join(path_project_data, lang)
    path_source_lang = os.path.join(path_source_data, lang)

    path_source_clips = os.path.join(path_source_lang, 'clips')

    print(path_dest_lang)
    print(path_source_lang)
    print(path_source_clips)

    if not os.path.exists(path_dest_lang):
        os.makedirs(path_dest_lang)

    path_validated_tsv = os.path.join(path_source_lang, 'validated.tsv')
    validated_tsv = pd.read_csv(path_validated_tsv, sep='\t')

    for index, row in validated_tsv.iterrows():
        path_mp3_src = os.path.join(path_source_clips, row.path)
        path_mp3_dest = os.path.join(path_dest_lang, row.path)
        path_dest_wav = path_mp3_dest.replace('.mp3', '.wav')
        path_dest_txt = path_mp3_dest.replace('.mp3', '.txt')
        sound = pydub.AudioSegment.from_mp3(path_mp3_src)
        sound.export(path_dest_wav, format='wav')
        with open(path_dest_txt, 'w', encoding='utf-8') as f:
            f.write(row.sentence)

        if index % 10 == 0:
            print(index)

        if index > N_TO_PROCESS:
            break

