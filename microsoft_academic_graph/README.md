# Microsoft Academic Graph

![entity-relationship-diagram.png](https://docs.microsoft.com/en-us/academic-services/graph/media/erd/entity-relationship-diagram.png)
## instering data in sql-database

### postgres
    populating: authors took ~15 hours!!
    256_683_554it [14:51:10, 4800.50it/s]
    
### sqlite
    populating: authors -> ~1hour
    skipping: 3800000 rows took: 0.18
    252883554it [1:15:32, 55787.75it/s]

#### number of authors from berlin
    SELECT count(*)
    FROM
    (
    SELECT DISTINCT t1.id
    FROM public.authors t1
    LEFT JOIN public.affiliations t2 ON t2.id = t1.last_known_affiliation
    WHERE t2.normalized_name like '%berlin%'
    ) dings;