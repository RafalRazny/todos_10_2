import sqlite3
from sqlite3 import Error


def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by the db_file
   :param db_file: todos_database.db
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
   except Error as e:
       print(e)

   return conn


class TodosSQLite:
    def __init__(self):
        conn = create_connection("todos_database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM todos_database.db")
        rows = cur.fetchall()
        return rows


    def select_all(self, conn, table):
        """
        Query all rows in the todos
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows


    def select_where(self, conn, table, **query):
        """
        Query tasks from table with data from **query dict
        :param conn: the Connection object
        :param table: table name
        :param query: dict of attributes and values
        :return:
        """
        cur = conn.cursor()
        qs = []
        values = ()
        for k, v in query.items():
            qs.append(f"{k}=?")
            values += (v,)
        q = " AND ".join(qs)
        cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
        rows = cur.fetchall()
        return rows


    def add_todo(self, conn, todo):
        """
        Create a new projekt into the projects table
        :param conn:
        :param projekt:
        :return: projekt id
        """
        sql = '''INSERT INTO projects(id, title, description, done)
             VALUES(?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, todo)
        conn.commit()
        return cur.lastrowid


    def update(self, conn, table, id, **kwargs):
        """
        update title, description, and done of a todo
        :param conn:
        :param table: table name
        :param id: row id
        :return:
        """
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)


    def delete_where(self, conn, table, **kwargs):
        """
        Delete from table where attributes from
        :param conn:  Connection to the SQLite database
        :param table: table name
        :param kwargs: dict of attributes and values
        :return:
        """
        qs = []
        values = tuple()
        for k, v in kwargs.items():
            qs.append(f"{k}=?")
        values += (v,)
        q = " AND ".join(qs)

        sql = f'DELETE FROM {table} WHERE {q}'
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("Deleted")

    def delete_all(conn, table):
        """
        Delete all rows from table
        :param conn: Connection to the SQLite database
        :param table: table name
        :return:
        """
        sql = f'DELETE FROM {table}'
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("Deleted")

    if __name__ == "__main__":
        conn = create_connection("todos_database.db")
        delete_where(conn, "todos", id=3)
        delete_all(conn, "todos")

todos = TodosSQLite()