def read_attendance(filename):
    records = []

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) == 3:
                records.append(parts)

    return records


def calculate_percentage(records):
    data = {}

    for reg, date, status in records:
        data.setdefault(reg, {"P": 0, "A": 0})
        if status in ["P", "A"]:
            data[reg][status] += 1

    result = {}

    for reg, values in data.items():
        total = values["P"] + values["A"]
        result[reg] = values["P"] / total * 100 if total else 0

    return result


def absent_three_days(records):
    students = {}

    for reg, date, status in records:
        students.setdefault(reg, []).append((date, status))

    result = []

    for reg, entries in students.items():
        streak = 0

        for date, status in sorted(entries):
            streak = streak + 1 if status == "A" else 0

            if streak >= 3:
                result.append(reg)
                break

    return result


def write_report(data, filename):
    with open(filename, "w") as file:
        for reg, percentage in data.items():
            file.write(f"{reg}: {percentage:.2f}%\n")


if __name__ == "__main__":

    records = read_attendance("attendance.txt")

    percentage = calculate_percentage(records)

    write_report(percentage, "percentage_report.txt")

    absent = absent_three_days(records)

    with open("three_day_absentees.txt", "w") as file:
        for student in absent:
            file.write(student + "\n")

    print("Reports generated successfully!")
