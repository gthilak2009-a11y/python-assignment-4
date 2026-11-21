import os
import csv
from collections import defaultdict

def process_attendance(folder):

    attendance = defaultdict(lambda: {"P": 0, "A": 0})
    damaged = []

    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            path = os.path.join(folder, filename)

            try:
                with open(path, "r", encoding="utf-8") as file:

                    for line_number, line in enumerate(file, 1):

                        try:
                            parts = line.strip().split(",")

                            if len(parts) != 3:
                                raise ValueError("Invalid fields")

                            reg_no, date, status = parts

                            if status not in ["P", "A"]:
                                raise ValueError("Invalid status")

                            attendance[reg_no][status] += 1

                        except ValueError as error:
                            damaged.append(
                                [filename, line_number, str(error)]
                            )

            except (FileNotFoundError, PermissionError) as error:
                damaged.append([filename, "-", str(error)])

    os.makedirs("reports", exist_ok=True)

    with open("reports/attendance.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Register Number", "Percentage"])

        for reg_no, data in attendance.items():

            total = data["P"] + data["A"]
            percentage = data["P"] / total * 100

            writer.writerow([reg_no, round(percentage, 2)])

    with open("reports/below_75.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Register Number", "Percentage"])

        for reg_no, data in attendance.items():

            total = data["P"] + data["A"]
            percentage = data["P"] / total * 100

            if percentage < 75:
                writer.writerow([reg_no, round(percentage, 2)])

    with open("reports/damaged_lines.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Filename", "Line Number", "Error"])
        writer.writerows(damaged)

    print("Attendance reports generated successfully!")


process_attendance("daily_files")
