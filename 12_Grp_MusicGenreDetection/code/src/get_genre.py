import numpy as np
import torch
import sys

from collections import Counter
from sklearn.preprocessing import LabelEncoder

from librosa.core import load
from librosa.feature import melspectrogram
from librosa import power_to_db

from model import genreNet
from config import MODELPATH
from config import GENRES

import warnings

warnings.filterwarnings("ignore")


def main(argv):

    if len(argv) != 1:
        print("Usage: python3 get_genre.py audiopath")
        exit()

    le = LabelEncoder().fit(GENRES)
    # ------------------------------- #
    ## LOAD TRAINED GENRENET MODEL
    net = genreNet()
    net.load_state_dict(torch.load(MODELPATH, map_location="cpu"))
    # ------------------------------- #
    ## LOAD AUDIO
    audio_path = argv[0]
    y, sr = load(audio_path, mono=True, sr=22050)
    # ------------------------------- #
    ## GET CHUNKS OF AUDIO SPECTROGRAMS
    S = melspectrogram(y, sr).T
    S = S[: -1 * (S.shape[0] % 128)]
    num_chunk = S.shape[0] / 128
    data_chunks = np.split(S, num_chunk)
    # ------------------------------- #
    ## CLASSIFY SPECTROGRAMS
    genres = list()
    for i, data in enumerate(data_chunks):
        data = torch.FloatTensor(data).view(1, 1, 128, 128)
        preds = net(data)
        pred_val, pred_index = preds.max(1)
        pred_index = pred_index.data.numpy()
        pred_val = np.exp(pred_val.data.numpy()[0])
        pred_genre = le.inverse_transform(pred_index).item()
        if pred_val >= 0.5:
            genres.append(pred_genre)
    # ------------------------------- #
    s = float(sum([v for k, v in dict(Counter(genres)).items()]))
    pos_genre = sorted(
        [(k, v / s * 100) for k, v in dict(Counter(genres)).items()],
        key=lambda x: x[1],
        reverse=True,
    )
    for genre, pos in pos_genre:
        print("%10s: \t%.2f\t%%" % (genre, pos))
    return


if __name__ == "__main__":
    main(sys.argv[1:])
