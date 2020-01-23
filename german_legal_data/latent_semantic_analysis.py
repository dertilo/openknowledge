from time import time

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from util import data_io

from openknowledge.wordcloud_methods import word_cloud_pdf


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join(
            [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        )
        print(message)


if __name__ == "__main__":
    file = "BverfG_juris.jsonl.gz"
    # print(Counter(k for d in data_io.read_jsonl(file) for k in d.keys()))
    p = "Orientierungssatz"
    data = [d[p] for d in data_io.read_jsonl(file) if p in d]
    texts = [" ".join(l) for l in data]
    print("%d texts" % len(texts))

    vectorizer = TfidfVectorizer(
        min_df=3,
        # tokenizer=lambda x: x,
        # preprocessor=lambda x: x,
        lowercase=False,
        sublinear_tf=False,
        max_features=5000,
        max_df=0.75,
    )
    tf = vectorizer.fit_transform(texts)

    pca = TruncatedSVD(n_components=20, random_state=42)

    t0 = time()
    X = pca.fit_transform(tf.toarray())
    print("LDA took: %0.2f" % (time() - t0))
    feature_names = vectorizer.get_feature_names()
    print_top_words(pca, feature_names, 20)

    n_top_words = 40
    l2f2w = {
        str(k): {feature_names[i]: c[i] for i in c.argsort()[: -n_top_words - 1 : -1]}
        for k, c in enumerate(pca.components_)
    }
    word_cloud_pdf(l2f2w)
