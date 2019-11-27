import pydub
import glob
import os
import pandas as pd

N_TO_PROCESS = 30
languages = ['ru', 'nl', 'de']

for lang in languages:
    path_to_data = '../data/{}_small'.format(lang)
    path_source_data = "/home/wran/Plurital/full_data_voice_language_recognizer/{}/clips/".format(lang)
    path_clips = os.path.join(path_to_data, 'clips')

    if not os.path.exists(path_clips):
        os.makedirs(path_clips)

    path_validated_tsv = os.path.join(path_to_data, 'validated.tsv')
    validated_tsv = pd.read_csv(path_validated_tsv, sep='\t')

    for n in range(N_TO_PROCESS):
        row = validated_tsv.iloc[n]
        path_src = os.path.join(path_source_data, row.path)
        path_dest = os.path.join(path_clips,row.path)
        path_dest_wav = path_dest.replace('.mp3', '.wav')
        path_dest_txt = path_dest.replace('.mp3', '.txt')
        sound = pydub.AudioSegment.from_mp3(path_src)
        sound.export(path_dest_wav, format='wav')
        with open(path_dest_txt, 'w', encoding='utf-8') as f:
            f.write(row.sentence)

