import book
import pickle


def update_bib(bib: dict):
    for each_book in bib.keys():
        bib[each_book] = update_book(bib[each_book])


def update_book(abook):
    try:
        if abook.likes is None:
            abook.likes = 0
    except AttributeError:
        abook.add_likes()
    return abook


class bookDB:
    def __init__(self, name):
        self.name = name
        try:
            f = open('bd_dump' + name, 'rb')
            self.bib = pickle.load(f)
            update_bib(self.bib)
            f.close()
        except IOError:
            self.bib = {}

    def save(self):
        f = open('bd_dump' + self.name, 'wb')
        pickle.dump(self.bib, f)
        f.close()

    def addBook(self, author, title, year):
        b_id = len(self.bib)
        self.bib[b_id] = book.book(author, title, year, b_id)
        self.save()

    def showBook(self, b_id):
        return self.bib[b_id]

    def listAllBooks(self):
        return list(self.bib.values())

    def listBooksAuthor(self, author_name):
        ret_value = []
        for b in self.bib.values():
            if b.author == author_name:
                ret_value.append(b)
        return ret_value

    def listBooksYear(self, year):
        ret_value = []
        for b in self.bib.values():
            if str(b.year) == str(year):
                ret_value.append(b)
        return ret_value
