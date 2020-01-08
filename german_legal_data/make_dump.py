from elasticsearch.helpers import scan
from tqdm import tqdm
from util import data_io

from esutil.es_util import build_es_client


def elastic_scan(
    es_client,
    index,
    query,  # {"_source":["id","name","content.features"]},
    batch_size=100,
    scroll_timeout="1m",
    limit=None,
):
    scan_iterator = scan(
        es_client, query=query, index=index, scroll=scroll_timeout, size=batch_size
    )
    for counter, hit in enumerate(scan_iterator):
        if limit is not None and counter > limit:
            break
        yield hit

def process(d):
    d = {k:d[k] for k in ['date','aktenzeichen','zitiervorschlag','entscheidungsdatum','content']}
    return d

if __name__ == '__main__':
    es_client = build_es_client(host="gunther")
    TYPE = "decision"
    INDEX = "juris"
    body = {
      "query": {
        "match_phrase": {
          "zitiervorschlag": "BVerfG"
        }
      }
    }
    hits_g = elastic_scan(
        es_client,
        index=INDEX,
        query=body,
        batch_size=100,
        # limit=100,
    )
    docs = (process(d['_source']) for d in tqdm(hits_g))

    # docs = (process(d) for d in data_io.read_jsonl('BverfG_juris.jsonl.gz'))
    data_io.write_jsonl('BverfG_juris_content.jsonl.gz',docs)
