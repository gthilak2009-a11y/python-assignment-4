import os
import csv

def process_registrations(folder):

    students = []
    seen = set()
    events = {}
    errors = []

    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            path = os.path.join(folder, filename)

            try:
                with open(path, "r", encoding="utf-8") as file:

                    for line_number, line in enumerate(file, 1):

                        try:
                            parts = line.strip().split(",")

                            if len(parts) != 5:
                                raise ValueError("Invalid record")

                            reg, name, dept, email, event_text = parts

                            if "@" not in email or "." not in email:
                                raise ValueError("Invalid email")

                            if reg in seen:
                                raise ValueError("Duplicate registration")

                            event_list = [
                                event.strip()
                                for event in event_text.split(";")
                                if event.strip()
                            ]

                            if not all([reg, name, dept, event_list]):
                                raise ValueError("Missing information")

                            seen.add(reg)

                            student = {
                                "Register Number": reg,
                                "Name": name,
                                "Department": dept,
                                "Email": email,
                                "Events": event_text
                            }

                            students.append(student)

                            for event in event_list:
                                events.setdefault(event, [])
                                events[event].append(student)

                        except ValueError as error:
                            errors.append(
                                f"{filename}, Line {line_number}: {error}"
                            )

            except (FileNotFoundError, PermissionError, OSError) as error:
                errors.append(f"{filename}: {error}")

    os.makedirs("fest_output", exist_ok=True)

    with open("fest_output/master_list.csv", "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Register Number",
                "Name",
                "Department",
                "Email",
                "Events"
            ]
        )

        writer.writeheader()
        writer.writerows(students)

    for event, participants in events.items():

        filename = event.replace(" ", "_") + ".csv"

        with open("fest_output/" + filename, "w", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Register Number",
                    "Name",
                    "Department",
                    "Email",
                    "Events"
                ]
            )

            writer.writeheader()
            writer.writerows(participants)

    with open("fest_output/summary.txt", "w") as file:

        file.write("COLLEGE FEST SUMMARY\n")
        file.write("--------------------\n")
        file.write(f"Total Registrations: {len(students)}\n")

        for event, participants in events.items():
            file.write(
                f"{event}: {len(participants)} participants\n"
            )

    with open("fest_output/error_log.txt", "w") as file:

        for error in errors:
            file.write(error + "\n")

    print("Fest registration processing completed!")
    print("Total students:", len(students))
    print("Total events:", len(events))
    print("Errors:", len(errors))


if __name__ == "__main__":
    process_registrations("input_files")
