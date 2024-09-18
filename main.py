import sqlite3
import random
from datetime import date
from faker import Faker

fake = Faker()

class Database:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT,
            category TEXT,
            pages INTEGER,
            release_date TEXT,
            author_id INTEGER
        )
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            birth_place TEXT
        )
        ''')


    def populate_db(self):
        categories = ['fantasy', 'thriller', 'fiction', 'mystery', 'science fiction', 'horror', 'adventure', 'history',
                      'comedy', 'romance', 'biography']
        book_release_date_start = date(year=1980, month=1, day=1)
        author_birth_date_start = date(year=1880, month=1, day=1)
        author_birth_date_end = date(year=1966, month=1, day=1)

        for i in range(1, 1001):
            book_name = f'bookName_{i}'
            category = random.choice(categories)
            pages = random.randint(70, 500)
            release_date = fake.date_between(start_date=book_release_date_start, end_date='now')
            author_id = random.randint(1, 500)
            self.cur.execute('''
                INSERT INTO book (book_name, category, pages, release_date, author_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (book_name, category, pages, release_date, author_id))

        for _ in range(1, 501):
            first_name = f'firstName_{random.randint(1, 250)}'
            last_name = f'lastName_{random.randint(1, 250)}'
            birth_date = fake.date_between(start_date=author_birth_date_start, end_date=author_birth_date_end)
            birth_place = f'Country_{random.randint(1, 195)}'
            self.cur.execute('''
                INSERT INTO author (first_name, last_name, birth_date, birth_place)
                VALUES (?, ?, ?, ?)
            ''', (first_name, last_name, birth_date, birth_place))

        self.con.commit()

    def ensure_db_populated(self):
        self.cur.execute('''
            SELECT
                (SELECT COUNT(*) FROM book),
                (SELECT COUNT(*) FROM author)
        ''')
        counts = self.cur.fetchone()
        book_table = counts[0]
        author_table = counts[1]

        if not (book_table == 1000 and author_table == 500):
            self.cur.execute('DELETE FROM book')
            self.cur.execute('DELETE FROM author')
            self.populate_db()


    def books_with_most_pages(self):
        self.cur.execute('''
            SELECT MAX(pages) FROM book
        ''')
        max_pages = self.cur.fetchone()[0]

        self.cur.execute('''
            SELECT * FROM book
            WHERE pages = ?
        ''', (max_pages,))

        books = self.cur.fetchall()
        for book in books:
            print(book)


    def average_pages_in_books(self):
        self.cur.execute('''
            SELECT pages FROM book
        ''')

        pages = [book_pages[0] for book_pages in self.cur.fetchall()]

        total_pages = sum(pages)
        books_count = len(pages)
        avg = total_pages / books_count
        print(avg)


    def youngest_author(self):
        self.cur.execute('''
            SELECT * 
            FROM author
            ORDER BY birth_date DESC
        ''')
        print(self.cur.fetchone())


    def authors_with_no_books(self):
        self.cur.execute('SELECT id FROM author')
        authors_id = set(row[0] for row in self.cur.fetchall())

        self.cur.execute('SELECT author_id FROM book')
        author_ids_with_books = set(row[0] for row in self.cur.fetchall())

        author_ids_without_books = authors_id - author_ids_with_books

        if author_ids_without_books:
            query = 'SELECT * FROM author WHERE id IN ({})'.format(','.join('?' for _ in author_ids_without_books))
            self.cur.execute(query, tuple(author_ids_without_books))
            authors_without_book = self.cur.fetchall()
            for author in authors_without_book:
                print(author)
        else:
            print('there\'s no author without a book')


    def top_authors_by_book_count(self):
        self.cur.execute('''
            SELECT author_id FROM book
        ''')

        count = {}
        for id in self.cur.fetchall():
            id = id[0]
            if id not in count:
                count[id] = 0
            count[id] += 1

        authors_with_most_books = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
        first_five_author_with_most_books = {k: authors_with_most_books[k] for k in list(authors_with_most_books)[:5]}

        self.cur.execute('SELECT * FROM author WHERE id IN ({})'.format(','.join('?' for _ in first_five_author_with_most_books.keys())), tuple(first_five_author_with_most_books.keys()))
        for author in self.cur.fetchall():
            print(author)



db = Database('database.sqlite3')
db.ensure_db_populated()
print('books with the most pages:')
db.books_with_most_pages()
print('----------------------------\naverage pages in books:')
db.average_pages_in_books()
print('----------------------------\nyoungest author:')
db.youngest_author()
print('----------------------------\nauthors with no book:')
db.authors_with_no_books()
print('----------------------------\nauthors with more than three books:')
db.top_authors_by_book_count()
