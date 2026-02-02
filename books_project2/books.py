from fastapi import FastAPI, Path, Query, HTTPException
from Book import *
from starlette import status

app = FastAPI()

BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "Good book", 5, 2010),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "Great book", 5, 2000),
    Book(3, "Master Endpoints", "codingwithroby", "Awesome book", 5, 2020),
    Book(4, "HP1", "Author 1", "Book description 1", 3, 2024),
    Book(5, "HP2", "Author 2", "Book description 2", 2, 2024),
    Book(6, "HP3", "Author 3", "Book description 3", 2.5, 2026)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found!")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.get("/books/bydate/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    is_book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            is_book_found = True
            break

    if not is_book_found:
        raise HTTPException(status_code=404, detail="Book not found!")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_book_found = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            is_book_found = True
            break

    if not is_book_found:
        raise HTTPException(status_code=404, detail="Book not found!")



