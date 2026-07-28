#Task 3: List Comprehensions Practice
import csv

employees = []

with open("../csv/employees.csv", "r") as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        employees.append(row)
employee_names = [
    row[1] + " " + row[2]
    for row in employees[1:]
]

print(employee_names)
names_with_e = [
    name
    for name in employee_names
    if "e" in name
]

print(names_with_e)