from pathlib import Path

from tqdm import tqdm
from util import data_io

from esutil.es_util import build_es_client

home = str(Path.home())


def build_body(d):
    return """
        {
          "query": {
            "bool": {
              "must": [
                {
                  "match_phrase": {
                    "aktenzeichen": "%s"
                  }
                },
                {
                  "match_phrase": {
                    "zitiervorschlag": "%s"
                  }
                },
                {
                  "range": {
                    "date": {
                      "gte": "%s",
                      "lte": "%s"
                    }
                  }
                }
              ]
            }
          },
          "size": 20,
          "_source": {
            "excludes": "content"
          }
        }
        """%(
        d["file_number"], d["type"],d['date'],d['date']
    )

if __name__ == "__main__":
    file = home + "/data/cases.json.gz"

    es_client = build_es_client(host="guntherhamachi")
    TYPE = "decision"
    INDEX = "juris"


    def not_found_generator():
        for d in tqdm(data_io.read_jsonl(file)):
            body = build_body(d)
            r = es_client.search(index=INDEX, body=body, size=3)
            if r['hits']['total']['value'] < 1:
                yield d

    data_io.write_jsonl('failed_to_find.jsonl',not_found_generator())
