from typing import Dict
from matplotlib import pyplot as plt
from wordcloud import WordCloud


def plot_wordcloud(feat2weight, title):
    def color_fun(word, font_size, position, orientation,
                  font_path, random_state):
        return 'rgb(0,0,0)'

    wordcloud = WordCloud(min_font_size=19, background_color='white', width=1600, height=1600,
                          color_func=color_fun).generate_from_frequencies(feat2weight)
    # Display the generated image:
    # the matplotlib way:
    fig = plt.figure(figsize=(9, 9), dpi=180)
    plt.title(title)
    plt.imshow(wordcloud)  # interpolation='bilinear'
    plt.axis("off")
    return fig


def print_pdf(feat2weight, title, pdf):
    fig = plot_wordcloud(feat2weight, title)
    pdf.savefig(fig)
    plt.close(fig)


def word_cloud_pdf(
        l2f2w:Dict[str,Dict[str,float]],
        pdf_file='/tmp/word_clouds.pdf'
    ):
    from matplotlib.backends.backend_pdf import PdfPages

    with PdfPages(pdf_file) as pdf:
        for label, f2w in l2f2w.items():
            print('------------     supporting: %s  -----------------'%label)
            fw = sorted(((f, w) for f, w in f2w.items()), key=lambda x: -x[1])[:9]
            for f, w in fw:
                print('%s:\t%0.2f' % (f, w))
            print('------------     contradicting: %s  -----------------'%label)
            fw = sorted(((f, w) for f, w in f2w.items()), key=lambda x: x[1])[:9]
            for f, w in fw:
                print('%s:\t%0.2f' % (f, w))

            feat2weight = {f: w for f, w in f2w.items() if w>0.0}
            print_pdf(feat2weight, label, pdf)
            feat2weight = {f: -w for f, w in f2w.items() if w<0.0}
            if len(feat2weight)>0:
                print_pdf(feat2weight, 'contradicting %s' % label, pdf)
            print('plottet %s' % label)

def plot_wordclouds(
        l2f2w:Dict[str,Dict[str,float]],
    ):

    for label, f2w in l2f2w.items():
        feat2weight = {f: w for f, w in f2w.items() if w>0.0}
        plot_wordcloud(feat2weight, label)
        feat2weight = {f: -w for f, w in f2w.items() if w<0.0}
        if len(feat2weight)>0:
            plot_wordcloud(feat2weight, 'contradicting %s' % label)
        plt.show()