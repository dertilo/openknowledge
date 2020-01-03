from util import data_io

from esutil.es_streaming_bulk import populate_es_streaming_bulk
from esutil.es_util import build_es_client

if __name__ == '__main__':
    from pathlib import Path
    home = str(Path.home())
    file = home+'/data/juris/htmls/31-12-2012_to_06-01-2013.jsonl.gz'
    data = list(data_io.read_jsonl(file))

    INDEX_NAME = "juris"
    TYPE = "decision"
    es_client = build_es_client()

    # es_client.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    es_client.indices.create(index=INDEX_NAME, ignore=400)


    populate_es_streaming_bulk(
        es_client, [file], INDEX_NAME, TYPE, limit=10_000
    )