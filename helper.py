from datetime import date


def validate_author_inputs(author_name, birth_date, date_of_death):
    """
    Validates the input of the user. First checks if all fields are set.
    Afterwards the date fields are checked if they make sense.
    Returns a list of errors.
    """

    validation_errors = []

    # first checking if all input fields are set
    if not author_name:
        validation_errors.append("Author name cannot be empty")
    if not birth_date:
        validation_errors.append("Birthdate cannot be empty")

    if len(validation_errors) > 0:
        return validation_errors

    date_birth = date.fromisoformat(birth_date)
    date_today = date.today()

    if date_birth >= date_today:
        validation_errors.append("Date of birth must be in the past.")
    if date_of_death:
        date_death = date.fromisoformat(date_of_death)
        if date_death > date_today:
            validation_errors.append("Date of death must be in the past.")
        if date_birth >= date_death:
            validation_errors.append("Date of death must be after date of birth.")

    return validation_errors


def validate_book_inputs(isbn, title, author, publication_year):
    """
    Validates the input of the user. First checks if all fields are set.
    Afterwards the isbn field is checked if they make sense.
    Returns a list of errors.
    """

    validation_errors = []

    # first checking if all input fields are set
    if not isbn:
        validation_errors.append("ISBN cannot be empty")
    if not title:
        validation_errors.append("Title cannot be empty")
    if not author:
        validation_errors.append("Author cannot be empty")
    if not publication_year:
        validation_errors.append("Publication year cannot be empty")

    if len(validation_errors) > 0:
        return validation_errors

    if not is_valid_isbn(isbn):
        validation_errors.append("ISBN is not valid. It must be 10 or 13 digits long.")

    return validation_errors


def is_valid_isbn(isbn):
    """Checks if a isbn only contains 10 or 13 didgits"""

    clean_isbn = convert_to_clean_isbn(isbn)
    if (len(clean_isbn) == 10 or len(clean_isbn) == 13) and clean_isbn.isdigit():
        return True
    return False


def convert_to_clean_isbn(isbn):
    """Takes an isbn and returns it without - and spaces"""

    return isbn.replace("-", "").replace(" ", "")
