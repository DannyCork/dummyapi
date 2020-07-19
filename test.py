import requests
import random
import sys

baseurl = "http://dummy.restapiexample.com/api/v1"
employees_url = f"{baseurl}/employees"
headers = {"user-agent": "fake-browser/0.1"}
name = "testname" + str(random.random())
age = random.randint(18, 80)


def create_employee(name, age):
    """
    Creates an employee using a random name and age by POSTing to the create endpoint. 
    :param name name of employee to create.
    :param age of employee.
    :return id of newly created employee.
    """
    create_url = f"{baseurl}/create"
    body = {"name": name, "salary": "123", "age": age}
    response = requests.post(create_url, body, headers=headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["data"]["name"] == name
    assert response_json["data"]["age"] == age

    return response_json["data"]["id"]


def get_employee(employee_id):
    """
    Retrieves an employee created in previous test.
    :param employee_id id of employee to read.
    """
    employee_url = f"{baseurl}/employee/{employee_id}"

    response = requests.get(employee_url, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["data"]["name"] == name
    assert response_json["data"]["age"] == age


def update_employee(employee_id):
    """
    Updates an employee that was created in test_create_employee().
    :param name name of employee to update.
    """
    updated_salary = random.randint(80000, 90000)
    update_url = f"{baseurl}/update/{employee_id}"
    body = {"salary": updated_salary}

    response = requests.put(update_url, body, headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["data"]["salary"] == updated_salary


def delete_employee(employee_id):
    """
    Deletes the employee passed in as employee_id
    :param employee_id id of employee to delete.
    """
    delete_url = f"{baseurl}/delete/{employee_id}"
    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 200


def get_all_employees():
    """
    Tests a ramdom employee (id 1..24) from employees endpoint.
    """
    response = requests.get(employees_url, headers=headers)
    assert response.status_code == 200

    randomEmployee = random.randint(1, 24)
    response_json = response.json()
    selectedEmployee = response_json["data"][randomEmployee]

    assert selectedEmployee["employee_name"] is not None
    assert int(selectedEmployee["employee_salary"]) is not None
    assert int(selectedEmployee["employee_age"]) > 1

id = create_employee(name, age)
get_employee(id)
update_employee(id)
delete_employee(id)
