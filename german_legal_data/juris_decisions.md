`GET /juris/_mapping` -> to get list of fields

### 1407979 overall
`GET /juris/_count`  

### 334863 before 1990
    GET /juris/_count
    {
      "query": {
        "range": {
          "date": {
            "lte": "1990-01-01"
          }
        }
      }
    }
    
### at least 255 have no HTML-doc but a PDF
    
    GET /juris/_count
    {
      "query": {
        "multi_match": {
          "query": "Im neuen Fenster: das folgende PDF-Dokument",
          "type": "phrase"
        }
      }
    }
    
### 16197 decisions from Bundesverfassungsgericht

    GET /juris/_count
    {
      "query": {
        "match_phrase": {
          "zitiervorschlag": "BVerfG"
        }
      }
    }