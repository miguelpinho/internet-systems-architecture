from flask import Flask, render_template, request, jsonify
import bookDB

app = Flask(__name__)
db = bookDB.bookDB("mylib")


# Main Page
@app.route('/')
def hello_world():
    count = len(db.listAllBooks())
    return render_template("mainPage.html", count_books=count)


# Web Site
@app.route('/addBooksForm')
def add_Book_Form():
    return render_template("addBookTemplate.html")


@app.route("/listAllBooks")
def list_all_books():
    return render_template("listBooksTemplate.html", title="Listing Every Book:", content=db.listAllBooks())


@app.route("/showBookForm")
def show_Search_Id_Form():
    return render_template("generalFormTemplate.html", query="ById")


@app.route("/listBooksAuthorForm")
def show_Search_Author_Form():
    return render_template("generalFormTemplate.html", query="ByAuthor")


@app.route("/listBooksYear")
def show_Search_Year_Form():
    return render_template("generalFormTemplate.html", query="ByYear")


@app.route('/addBook', methods=['POST', 'GET'])
def add_Book():
    if request.method == "GET":
        imm_dict = request.args
    else:
        imm_dict = request.form
    title = imm_dict['Title']
    author = imm_dict['Author']
    year = imm_dict['Year']
    db.addBook(author, title, year)
    return render_template("mainPage.html", count_books=len(db.listAllBooks()), op_result="book_added")


@app.route('/search')
def search():
    imm_dict = request.args
    query = imm_dict["query"]
    if query == "ById":
        bid = imm_dict['BookId']
        return render_template("bookPageTemplate.html", book=db.showBook(int(bid)))
    elif query == "ByAuthor":
        author = imm_dict['Author']
        return render_template("listBooksTemplate.html", title=f"Listing all the books from:{author}",
                               content=db.listBooksAuthor(author))
    else:
        year = imm_dict['Year']
        return render_template("listBooksTemplate.html", title=f"Listing books from the year {year}",
                               content=db.listBooksYear(year))


# API
@app.route('/api')
def api_home():
    data = {
        'Status': 'Api is functional',
        'Docs'  : ''
    }
    resp = jsonify(data)
    resp.status_code = 200
    return resp


@app.route('/api/books')
def api_books():
    # Return the list of all books
    list_of_books = db.listAllBooks()
    data = {"Books": {}}
    for book in list_of_books:
        book_data = {"Id": book.id, "Title": book.title}
        data["Books"][book.id] = book_data
    resp = jsonify(data)
    return resp


@app.route('/api/authors')
def api_authors():
    list_of_books = db.listAllBooks()
    data = {"Authors": {}}
    for book in list_of_books:
        try:
            entry = data["Authors"][book.author]
            entry["Book Count"] += 1
        except KeyError:
            data["Authors"][book.author] = {"Book Count": 1}

    resp = jsonify(data)
    return resp


@app.route('/api/books/<int:bid>')
def api_book(bid):
    book = db.showBook(bid)
    data = {"Book": {"Id": book.id, "Author": book.author, "Title": book.title, "Year": book.year}}
    resp = jsonify(data)
    return resp


@app.route('/api/books/<int:bid>/like', methods=['GET', 'POST'])
def api_book_post_like(bid):
    book = db.showBook(bid)
    if request.method == 'POST':
        book.put_like()
        db.save()
    data = {"Book": {"Id": book.id, "Likes": book.likes}}
    resp = jsonify(data)
    return resp


@app.route('/api/books/<int:bid>/edit', methods=['PUT'])
def api_book_put_edit(bid):
    book = db.showBook(bid)
    new_data = request.json
    book.set_title(new_data["Title"])
    book.set_author(new_data["Author"])
    book.set_year(new_data["Year"])
    db.save()
    return "OK"


@app.route('/api/books/year/<int:year>')
def api_books_year(year):
    list_of_books = db.listBooksYear(str(year))
    data = {"Books": {}, "Year": year}
    for book in list_of_books:
        if str(book.year) == str(year):
            book_data = {"Id": book.id, "Title": book.title}
            data["Books"][book.id] = book_data
    resp = jsonify(data)
    return resp


@app.route('/api/authors/<string:author>')
@app.route('/api/authors/<string:author>/<string:modifier>')
@app.route('/api/authors/<string:author>/year/<int:year>')
def api_author(author, modifier="", year=-1):
    list_of_books = db.listBooksAuthor(author)

    data = {"Author": author, "Author Books Count": len(list_of_books)}

    if modifier == "list":
        data["Books"] = {}
        for book in list_of_books:
            book_data = {"Id": book.id, "Title": book.title}
            data["Books"][book.id] = book_data
    if year != -1:
        data["Books"] = {}
        data["Year"] = year
        for book in list_of_books:
            if str(book.year) == str(year):
                book_data = {"Id": book.id, "Title": book.title}
                data["Books"][book.id] = book_data

    resp = jsonify(data)
    return resp


if __name__ == '__main__':
    app.run()
