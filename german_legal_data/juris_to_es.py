import json
from datetime import datetime

from bs4 import BeautifulSoup
from util.data_io import read_jsonl

from esutil.es_streaming_bulk import populate_es_streaming_bulk
from esutil.es_util import build_es_client


def parse_content(d: dict):
    def get_label(h):
        label = json.loads(h.find("h4").attrs["data-juris-toc"])["label"]
        return label

    def get_paragraphs(h):
        if h is not None:
            paragraphs = [
                p.text for p in h.find_all("dl", class_="RspDL") if len(p.text) > 0
            ]
        else:
            paragraphs = None
        return paragraphs

    # --------------------------------------------------------------------------------
    soup = BeautifulSoup(d["content"], "html.parser")

    parsed = {
        get_label(topmore): get_paragraphs(topmore.next_sibling)
        for topmore in soup.find_all("div", class_="docLayoutMarginTopMore")
    }
    d.update(parsed)
    d["date"] = datetime.strptime(d["date"], "%d.%m.%Y").isoformat()
    return d


if __name__ == "__main__":
    from pathlib import Path

    home = str(Path.home())
    # home = '/home/tilo/gunther'
    files = [home + "/data/juris/htmls/31-12-2012_to_06-01-2013.jsonl.gz"]
    dicts_g = (parse_content(d) for file in files for d in read_jsonl(file))
    # data = list(dicts_g)

    INDEX_NAME = "juris"
    TYPE = "decision"
    es_client = build_es_client()

    es_client.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    es_client.indices.create(index=INDEX_NAME, ignore=400)

    populate_es_streaming_bulk(es_client, dicts_g, INDEX_NAME, TYPE)
