from decimal import Decimal

def process_mess_file(filename):
    total = Decimal("0.00")
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    parts = line.split(",")

                    if len(parts) != 3:
                        raise ValueError("Invalid record")

                    register_no, name, amount = parts
                    amount = Decimal(amount)

                    total += amount
                    report.append(f"{name} {amount:.2f}")

                except (ValueError, ArithmeticError) as error:
                    rejected.append((line_number, line, str(error)))

        print("MESS BILL REPORT")

        for item in report:
            print(item)

        print("Total:", total)

        print("\nRejected Lines:")
        for item in rejected:
            print(item)

    except FileNotFoundError:
        print("File not found")

    except PermissionError:
        print("Permission denied")


if __name__ == "__main__":
    process_mess_file("mess_oct.txt")
