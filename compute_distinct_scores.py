import pandas as pd
import nltk
from nltk import bigrams
import numpy as np


def compute_distinct_score(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if len(token) > 1]  # same as unigrams
    unigram_count = len(set(tokens))
    bi_tokens = bigrams(tokens)
    bigram_count = 0
    for _ in set(bi_tokens):
        bigram_count += 1
    return np.mean([unigram_count, bigram_count])


if __name__ == "__main__":
    input_file = "data/real_tox_dexperts.csv"
    out_file = input_file

    df = pd.read_csv(input_file)

    distinct_scores = []
    for i, row in df.iterrows():
        score = compute_distinct_score(row["gen"].lower())
        distinct_scores.append(score)

    print("Mean", np.mean(distinct_scores))
    df["distinct_score"] = distinct_scores
    df.to_csv(out_file, index=False)
