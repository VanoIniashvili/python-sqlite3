# database managment with sqlite

this project provides a basic example of managing a sqlite database using python and the sqlite3 module. it demonstrates how to create tables, populate them with random data, and perform various queries to retrieve information.

<br/>

## installation

#### install modules

```bash
pip install requirements.txt
```

#### run the script

```bash
python3 main.py
```

<br/>

## usage

### create tables: 
 -  the create_tables method creates book and author tables if they don't already exist.

### populate database:
 -  The populate_db method inserts random data into the book and author tables.

### check and populate database:
 - The ensure_db_populated method verifies the number of records in each table and repopulates if needed.

### queries:

 -  books_with_max_pages(): finds and prints books with the maximum number of pages.

 -  average_pages_in_books(): calculates and prints the average number of pages in books.

 -  youngest_author(): retrieves and prints the youngest author.

 -  authors_with_no_books(): lists authors who haven't written any books.

 -  top_authors_by_book_count(): lists the top authors by the number of books written.
