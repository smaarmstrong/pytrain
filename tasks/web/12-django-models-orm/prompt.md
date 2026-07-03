# Django: models and ORM queries

In `solution.py`, define two Django models and four query helpers. No
views, no urls — this task is pure ORM, graded against an in-memory
SQLite database the grader creates for you (no migrations needed).

## Setup boilerplate (keep it)

The starter configures Django settings when the file is run standalone
and guards with `if not settings.configured:` — the grader configures
Django itself first, so the guard must stay.

## Models

Both models need `class Meta: app_label = "solution"` (they live outside
a Django app).

- `Author` — `name = models.CharField(max_length=100, unique=True)`
- `Book` — `title` (CharField, max_length 200),
  `author` (ForeignKey to Author, `on_delete=models.CASCADE`,
  `related_name="books"`), `year` (IntegerField),
  `pages` (IntegerField)

## Query helpers

1. `add_book(author_name, title, year, pages)` — get-or-create the
   author by name, create and return the `Book`.

2. `books_between(start, end)` — list of **titles** of books with
   `start <= year <= end` (inclusive), ordered by year ascending, ties
   by title ascending. Use queryset filtering (`year__gte` / `__lte` or
   `range`), not Python loops.

3. `prolific_authors(min_books)` — list of **names** of authors with at
   least `min_books` books, ordered by name ascending. Use
   `annotate(Count(...))`, not Python counting.

4. `average_pages(author_name)` — the average `pages` of that author's
   books as a `float`, or `None` if the author doesn't exist or has no
   books. Use `aggregate(Avg(...))`.

Example:

```python
add_book("Le Guin", "A Wizard of Earthsea", 1968, 205)
add_book("Le Guin", "The Dispossessed", 1974, 341)
books_between(1970, 1980)      # ["The Dispossessed"]
prolific_authors(2)            # ["Le Guin"]
average_pages("Le Guin")       # 273.0
average_pages("Nobody")        # None
```
