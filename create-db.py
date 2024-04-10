import os
import sqlite3
import sys


class SearchDb:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_conn = None
        if not self.db_exists():
            res = self.create_db()
            if res:
                self.db_conn = res
            else:
                print(f"## [SearchDb::__init__] 💥 ERROR: creating database {db_name}")
                sys.exit(1)
        else:
            print(f"## [SearchDb::__init__] 👍 the database '{self.db_name}' was found")
            self.db_conn = sqlite3.connect(self.db_name)

    def db_exists(self):
        """Checks if the database file exists."""
        return os.path.isfile(self.db_name)

    def create_db(self):
        """Creates the database and any necessary tables."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Example table creation
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_item (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    subject TEXT,
                    keywords TEXT NOT NULL,
                    display TEXT NOT NULL,
                    x INTEGER NOT NULL,
                    y INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            print(f"## [SearchDb::create_db] 👍 database '{self.db_name}' created successfully")
        except sqlite3.OperationalError as error:
            print(f"## [SearchDb::create_db] 💥 ERROR: OperationalError creating database '{self.db_name}', err:{error}")
            return None
        except Exception as error:
            print(f"## [SearchDb::create_db] 💥 Unexpected ERROR: creating database '{self.db_name}', error:", error)
            return None
        finally:
            if conn:
                return conn

    def close(self):
        if self.db_conn:
            self.db_conn.close()
            print(f"## [SearchDb::close] 🏁 closed Database '{self.db_name}' successfully")

    def __del__(self):
        self.close()

    def __exit__(self):
        self.close()

    def count(self):
        if self.db_conn:
            cursor = self.db_conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM search_item')
            val = cursor.fetchone()
            if val:
                print(f"## [SearchDb::count] 📊 Total rows in search_item table: {val[0]}")
                return val[0]
            else:
                print("## [SearchDb::count] 💥 ERROR: Could not get count of search_item table")
                return 0
        return 0

    def search(self, pattern):
        if self.db_conn:
            cursor = self.db_conn.cursor()
            sql = '''
            SELECT count(*) as num_records,
                   json_group_array(
                    json_object(
                            'info', display,
                            'x', x,
                            'y', y
                        )
                    ) as records
            FROM search_item
            WHERE keywords like ?;
            '''
            cursor.execute(sql, ('%' + pattern + '%',))
            rows = cursor.fetchall()
            if rows:
                print(f"## [SearchDb::search] 🔍 Found {len(rows)} rows in search_item table with keyword '{pattern}'")
            else:
                print(f"## [SearchDb::search] ⭕ No rows found in search_item table with keyword '{pattern}'")
            return rows
        return []


if __name__ == "__main__":
    if len(sys.argv) > 1:
        dbname = sys.argv[1]
        search = "hello"
        if len(sys.argv) > 2:
            search = sys.argv[2]

        db = SearchDb(dbname)
        if db.db_conn:
            print(f"🚀 Connected to database {dbname}  successfully")
            num_records = db.count()
            if num_records > 0:
                print(f"📊 Total rows in search_item table: {num_records}")
            else:
                print("📊 No rows in search_item table")
            results = db.search(search)
            if results:
                print(f"📊 Found {len(results)} rows in search_item table with keyword '{search}'")
                for row in results:
                    print(f"num_record: {row[0]}\nrecords: {row[1]}\n")

            db.close()
        else:
            print(f"💥 Database {dbname} creation failed")
            sys.exit(1)
    else:
        print(f"Usage: {sys.argv[0]} <database_name>")
        sys.exit(1)
