# semantic-scholar in elastic search
* ~460 GB
* took ~7 hours to build the index
*  
### during indexing one can check which files have not yet been indexed
    GET s2papers_state/_search
    {
      "query": {
        "bool": {
          "must": {
            "term":{"done":false}
          }
          
        }
      }
    }
    
### during indexing check which files are currently indexed      
    GET s2papers_state/_search
    {
      "query": {
        "range": {
          "line": {
            "gte": 10,
            "lte": 1000000
          }
        }
      },
      "size": 200
    }
    
### ~97 mio papers (exact 97922977) do have an abstract

    GET s2papers/_count
    {
      "query": {
        "exists": {
          "field": "paperAbstract"
        }
      }
    }