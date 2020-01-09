from esutil.es_util import build_es_client
import pandas as pd


def fields_must_not_exist(fields):
    body = '''
    {
      "query": {
        "bool": {
          "must_not": [
          %s
          ]
        }
      }
    }
    ''' % (','.join(['{"exists": {"field": "%s"}}' % f for f in fields]))
    return body


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
    # import tabulate
    # print(tabulate.tabulate(df.sort_values(by=['count'], ascending=False),tablefmt='github'))
    print(df.sort_values(by=['count'], ascending=False))

    parsed_fields = [f for f, c in counts.items() if c < counts['Tenor']]
    print('parsed_fields: %s'%str(parsed_fields))
    num_no_fields = es_client.count(doc_type=TYPE, index=INDEX, body=fields_must_not_exist(parsed_fields))['count']
    print('number of documents with no parsed_fields: %d'%num_no_fields)
    # no_fields = es_client.search(index=INDEX, body=fields_must_not_exist(parsed_fields))
    # hits = es_client.search(index=INDEX, body=fields_must_not_exist(['zitiervorschlag']))['hits']['hits']
