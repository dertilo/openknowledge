from time import time
import sys
sys.path.append('.')
from typing import Iterable
from commons import data_io, util_methods
from sqlalchemy import Integer, Float, Table

from sqlalchemy_util.sqlalchemy_methods import count_rows
from tqdm import tqdm

from openknowledge.microsoft_academic_graph.database_schema import sqlalchemy_engine, Author


def convert_types(val, type):
    if isinstance(type, Integer) and len(val)>0:
        return int(val)
    elif isinstance(type, Float):
        return float(val)
    elif isinstance(val,str):
        return val.replace('\x00', '') if len(val)>0 else None
    else:
        return None

def skip_numrows(table:Table,data_g:Iterable):
    start = time()
    numrows = count_rows(sqlalchemy_engine,table)
    print('skipping: %d rows took: %0.2f'%(numrows,time()-start))
    [next(data_g) for _ in range(numrows)]

def insert_in_table(conn, table:Table, data:Iterable, batch_size=10000):
    def insert_batch(rows):
        conn.execute(table.insert(), rows)
    util_methods.consume_batchwise(insert_batch, data, batch_size)

def populate_table(table, line_g):
    cols = [c.name for c in table.c]
    types = [c.type for c in table.c]

    def line_to_dict(line):
        s = line.replace('\r', '').split('\t')
        try:
            d = {k: convert_types(v, t) for k, v, t in zip(cols, s, types)}
        except Exception:
            d = {k: v for k, v, t in zip(cols, s, types)}
            raise Exception('error parsing: %s'%str(d))
        return d

    data_g = (line_to_dict(line) for line in line_g)
    with sqlalchemy_engine.connect() as conn:
        insert_in_table(conn, table, data_g, batch_size=1000_000)

if __name__ == '__main__':
    data_path = '/docker-share/data/MAG/'
    for schema in [Author]:
        table = schema.__table__
        table_name = schema.__tablename__
        print('populating: %s'%table_name)
        lines_g = data_io.read_lines(data_path + '%s.txt.gz' % table_name.capitalize())
        skip_numrows(table,lines_g)
        g = tqdm(lines_g)
        populate_table(table,g)

'''

number of papers: 214100980 (zcat /docker-share/data/MAG/Papers.txt.gz | wc -l)

populating: papers took ~15 hours!!
skipping: 7_610_000 rows took: 0.54
206_402_980 it [14:49:40, 3866.65it/s] -> why so slow?
'''