# ISBN Service
Responsible for efficient, extensive ISBN lookup. Several ISBN databases are exhausted before returning a 
failed lookup. Cache always takes priority over 3rd party due to the ISBN standard's constant nature.

```
isbn_service/
├── __init__.py
├── isbn_service.py
├── google_books_api.py
├── cache.py
├── exceptions.py
└── tests/
    ├── unit/
    |   ├── __init__.py
    |   └── test_isbn.py
    └── integration/
        └── __init__.py
```

### Usage
The goal of this service is to require the user only use a single function from a single class. 
`ISBNService` will handle prioritizing lookup databases and cache along with failure, input validation, 
and any other issues resulting from 3rd party 
interaction.
```python
from isbn_service.isbn_service import ISBNService
from isbn_service.exceptions import ISBNNotFound, InvalidISBN

isbn_service = ISBNService("GOOGLE_BOOKS_API_KEY")
try:
    book = isbn_service.lookup("1234567890")
except ISBNNotFound:
    # Handle exception
except InvalidISBN:
    # Handle exception
```