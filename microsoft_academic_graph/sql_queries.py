from time import time
import sys
sys.path.append('.')
from sqlalchemy import select
from sqlalchemy_util.sqlalchemy_methods import get_tables_by_reflection, get_sqlalchemy_base_engine


def search_for_author(sqlalchemy_base,sqlalchemy_engine, author_name = 'suse brettin'):
    tables = get_tables_by_reflection(sqlalchemy_base.metadata, sqlalchemy_engine)
    table = tables['authors']
    start = time()
    result = list(sqlalchemy_engine.execute(select([table]).where(table.c.normalized_name == author_name)))
    print(result)
    print('took: %0.2f seconds' % (time() - start))
    return result


if __name__ == '__main__':
    # host = 'gunther'
    host = '172.17.0.1' # host from inside of docker-container

    sqlalchemy_base, sqlalchemy_engine = get_sqlalchemy_base_engine(host=host)
    search_for_author(sqlalchemy_base,sqlalchemy_engine)

    from database_schema import sqlalchemy_engine,sqlalchemy_base
    search_for_author(sqlalchemy_base,sqlalchemy_engine)

    import os
    start = time()
    os.system('cd /docker-share/data/MAG && zcat Authors.txt.gz | rg "suse brettin"')
    print('rg took %0.2f seconds'%(time()-start))

    '''
    [('2777955847', 20909, 'suse brettin', 'Suse Brettin', None, 1, 0, datetime.datetime(2018, 1, 5, 0, 0))]
    took: 8.74 seconds
    [('2777955847', 20909, 'suse brettin', 'Suse Brettin', None, 1, 0, '2018-01-05')]
    took: 40.37 seconds
    2777955847      20909   suse brettin    Suse Brettin            1       0       2018-01-05
    rg took 106.75 seconds
    '''