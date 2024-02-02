import pymysql.cursors
import pymysql
import pandas as pd

# Connect to the database
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='password',
                            db='world',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


def database_query(dabase, table):

    
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"Select * from {dabase}.{table} limit 50"
        cursor.execute(sql)
        result = cursor.fetchall()
        dataset = pd.DataFrame.from_dict(result)
        print(dataset)
    return dataset


def tablenames(database):
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"show tables in {database}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    tables = []
    for value in result:
        tables.append(value[f'Tables_in_{database}'])
    return tables


def database_names():
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"show databases"
        cursor.execute(sql)
        result = cursor.fetchall()
        database_names_list = []
        for value in result:
            database_names_list.append(value['Database'])
        # Invalid database names:
        invalid_dbs = ['information_schema', 'mysql', 'performance_schema', 'sys']
        valid_dbs = set(database_names_list) - set(invalid_dbs)
        return list(valid_dbs)
    
