import pprint

class Book:
    isbn: str
    title: str
    subtitle: str
    authors: [str]
    publisher: str
    publisher_date: str
    description: str
    page_count: str
    image_links: [str]

    def __init__(self, isbn: str, title: str, subtitle: str, authors: [str], publisher: str, publisher_date: str,
                 description: str, page_count: str, image_links: [str]):
        self.isbn = isbn
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.publisher = publisher
        self.publisher_date = publisher_date
        self.description = description
        self.page_count = page_count
        self.image_links = image_links

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False
