from esutil.es_util import build_es_client
import pandas as pd

if __name__ == "__main__":
    es_client = build_es_client(host="guntherhamachi")
    TYPE = "decision"
    INDEX = "juris"
    # count = es_client.count(index=INDEX, doc_type=TYPE)["count"]
    # print(count)

    r = es_client.indices.get_mapping(index=INDEX)

    get_body = lambda f:"""
    {
      "query": {
        "exists": {
          "field": "%s"
        }
      }
    }
    """%f
    counts = {
        field: es_client.count(doc_type=TYPE, index=INDEX, body=get_body(field))["count"]
        for field in r["juris"]["mappings"]["properties"].keys()
    }

    df = pd.DataFrame(data=[{'field': k, 'count': v} for k, v in counts.items()])
    import tabulate
    print(tabulate.tabulate(df.sort_values(by=['count'], ascending=False),tablefmt='github'))
    print(df.sort_values(by=['count'], ascending=False))
