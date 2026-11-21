from pathlib import Path

def save_returns(books):

    with open("returns.log", "a", encoding="utf-8") as log:

        for book in books:
            log.write(book + "\n")


def process(day_file):

    try:
        with open(day_file, "r", encoding="utf-8") as file:

            books = file.read().splitlines()

        save_returns(books)

    except FileNotFoundError as error:

        with open("errors.log", "a", encoding="utf-8") as log:
            log.write(str(error) + "\n")

        print("File missing:", day_file)


if __name__ == "__main__":

    days = {
        "day1.txt": ["Book A", "Book B"],
        "day2.txt": ["Book C"],
        "day3.txt": ["Book D", "Book E"]
    }

    for filename, books in days.items():

        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(books))

    open("returns.log", "w").close()
    open("errors.log", "w").close()

    process("day1.txt")
    process("day2.txt")
    process("day3.txt")
    process("missing.txt")

    print("\nReturned Books:")

    with open("returns.log", "r", encoding="utf-8") as file:
        print(file.read())

    print("Error Log:")

    with open("errors.log", "r", encoding="utf-8") as file:
        print(file.read())
