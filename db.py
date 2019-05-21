import sqlite3

class db:

    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def create_tables(conn):
        try:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    created_at TEXT,
                    url TEXT,
                    comment TEXT,
                    UNIQUE(id))
            ''')
            conn.commit()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pull_request(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    title TEXT,
                    url TEXT,
                    commits INTEGER,
                    additions INTEGER,
                    deletions INTEGER,
                    changed_files INTEGER,
                    created_at TEXT,
                    UNIQUE(id))
            ''')

            conn.commit()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS issues(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    title TEXT,
                    url TEXT,
                    body TEXT,
                    created_at TEXT,
                    UNIQUE(id))
            ''')

            conn.commit()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pushes(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    commits TEXT,
                    created_at TEXT,
                    UNIQUE(id))
            ''')

            conn.commit()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS branches(
                    id INTEGER PRIMARY KEY,
                    author TEXT,
                    created_at TEXT,
                    branch_name TEXT,
                    UNIQUE(id))
            ''')

            conn.commit()

        except Error as e:
            print(e)

    def insert_comment(conn, data):
        cur = conn.cursor()
        cur.execute('''SELECT id FROM comments WHERE id=?''', (data[0],))
        result = cur.fetchone()

        if result is None:
            cur.execute('''
            INSERT INTO comments(id, author, created_at, url, comment)
            VALUES(?,?,?,?,?)''', (data[0], data[1], data[2], data[3], data[4]))
            conn.commit()
        else :
            return False

    def insert_pull_requests(conn, data):
        cur = conn.cursor()
        cur.execute('''SELECT id FROM pull_request WHERE id=?''', (data[0],))
        result = cur.fetchone()

        if result is None:
            cur.execute('''
            INSERT INTO pull_request(id, author, title, url, commits, additions, deletions, changed_files, created_at)
            VALUES(?,?,?,?,?,?,?,?,?)''', (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
            conn.commit()
        else :
            return False

    def insert_issue(conn, data):
        cur = conn.cursor()
        cur.execute('''SELECT id FROM issues WHERE id=?''', (data[0],))
        result = cur.fetchone()

        if result is None:
            cur.execute('''
            INSERT INTO issues(id, author, title, url, body, created_at)
            VALUES(?,?,?,?,?,?)''', (data[0], data[1], data[2], data[3], data[4], data[5]))
            conn.commit()
        else :
            return False

    def insert_push(conn, data):
        cur = conn.cursor()
        cur.execute('''SELECT id FROM pushes WHERE id=?''', (data[0],))
        result = cur.fetchone()

        if result is None:
            cur.execute('''
            INSERT INTO pushes(id, author, commits, created_at)
            VALUES(?,?,?,?)''', (data[0], data[1], data[2], data[3]))
            conn.commit()
        else :
            return False

    def insert_branch(conn, data):
        cur = conn.cursor()
        cur.execute('''SELECT id FROM branches WHERE id=?''', (data[0],))
        result = cur.fetchone()

        if result is None:
            cur.execute('''
            INSERT INTO branches(id, author, created_at, branch_name)
            VALUES(?,?,?,?)''', (data[0], data[1], data[2], data[3]))
            conn.commit()
        else :
            return False
