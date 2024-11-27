from django.db import connection


def _dictfetchone(cursor):
    if cursor.description is None:
        return None
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None


def _dictfetchall(cursor):
    if cursor.description is None:
        return []
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def query_one(statement, *args):
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO basdat")
        cursor.execute(statement, args)
        return _dictfetchone(cursor)


def query_all(statement, *args):
    with connection.cursor() as cursor:
        cursor.execute("SET SEARCH_PATH TO basdat")
        cursor.execute(statement, args)
        return _dictfetchall(cursor)
