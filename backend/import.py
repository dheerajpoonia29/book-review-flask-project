import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("postgres://ntcwaduvpgeowm:b5459817675574612c7cf55ba6ffbb0752457b10239c15c7084ef858b9277349@ec2-54-83-17-151.compute-1.amazonaws.com:5432/dce25fb79tcjcv"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO flights (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book : {title} , isbn = {isbn}, written by lasting {author} in year.")
    db.commit()

if __name__ == "__main__":
    main()