class book:
    def __init__(self, author, title, year, b_id):
        self.author = author
        self.title = title
        self.year = year
        self.id = b_id
        self.likes = 0

    def __str__(self):
        return "%d - %s - %s - %s [likes:%d]" % (self.id, self.author, self.title, self.year, self.likes)

    def put_like(self):
        self.likes += 1

    def add_likes(self):
        self.likes = 0

    def set_title(self, title):
        if title is not None:
            if type(title) is str:
                if title != "":
                    self.title = title
                    return 0
        return 1

    def set_author(self, author):
        if author is not None:
            if type(author) is str:
                if author != "":
                    self.author = author
                    return 0
        return 1

    def set_year(self, year):
        if year is not None:
            if type(year) is str:
                if year != "":
                    self.year = year
                return 0
        return 1
