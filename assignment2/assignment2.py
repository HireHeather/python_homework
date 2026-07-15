#Task 2:Read a CSV File

import csv

def read_employees():
    employees = {}
    rows = []

    try:
        with open("../csv/employees.csv", "r") as file:
            csv_reader = csv.reader(file)

            employees["fields"] = next(csv_reader)

            for row in csv_reader:
                rows.append(row)

            employees["rows"] = rows

    except Exception as e:
        print(e)

    return employees

employees = read_employees()

print(employees)

#Task 3: Find the Index Column 
def column_index(column_name):
    return employees["fields"].index(column_name)
employee_id_column = column_index("employee_id")

#Task 4: Find Employee First Name
def first_name(row_number):
    first_name_column = column_index("first_name")
    name = employees["rows"][row_number][first_name_column]
    return name

#Task 5: Find the Employee: a Function in a Function

def employee_find(employee_id):

    def employee_match(row):
    
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))

    return matches

#Task 6: Find the Employee with a Lambda

def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

#Task 7: Sort the Rows by last_name Using a Lambda

def sort_by_last_name():
    last_name_column = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_column])
    return employees["rows"]

#Task 8: Create a dict for an Employee.
def employee_dict(row):
    employee = {}

    for i in range(len(employees["fields"])):
        if employees["fields"][i] != "employee_id":
            employee[employees["fields"][i]] = row[i]

    return employee
#Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    all_employees = {}

    for row in employees["rows"]:
        employee = employee_dict(row)
        all_employees[row[employee_id_column]] = employee

    return all_employees

#Task 10: Use the os Module

import os
def get_this_value():
    return os.getenv("THISVALUE")

#Task 11: Creating Your Own Module

import custom_module

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


set_that_secret("pug")
print(custom_module.secret)

#Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    minutes1 = {}
    minutes2 = {}

    rows1 = []
    rows2 = []

    with open("../csv/minutes1.csv", "r") as file:
        csv_reader = csv.reader(file)

        minutes1["fields"] = next(csv_reader)

        for row in csv_reader:
            rows1.append(tuple(row))

    with open("../csv/minutes2.csv", "r") as file:
        csv_reader = csv.reader(file)

        minutes2["fields"] = next(csv_reader)

        for row in csv_reader:
            rows2.append(tuple(row))

    minutes1["rows"] = rows1
    minutes2["rows"] = rows2

    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print(minutes1)
print(minutes2)

#Task 13: Create minutes_set
def create_minutes_set():
    attendees = set()

    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    attendees = minutes1_set.union(minutes2_set)

    return attendees


minutes_set = create_minutes_set()

#Task 14: Convert to datetime

from datetime import datetime
def create_minutes_list():
    minutes_list = list(minutes_set)
    minutes_list = list(
    map(
        lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
        minutes_list
    )
)

    return minutes_list

minutes_list = create_minutes_list()

print(minutes_list)

#Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])

    converted_minutes = list(
        map(
            lambda x: (x[0], x[1].strftime("%B %d, %Y")),
            minutes_list
        )
    )

    with open("./minutes.csv", "w", newline="") as file:
        csv_writer = csv.writer(file)

        csv_writer.writerow(minutes1["fields"])

        for row in converted_minutes:
            csv_writer.writerow(row)
        return converted_minutes

write_sorted_list()

        


