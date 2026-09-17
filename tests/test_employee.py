def test_get_employees(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 201
    response = client.get('/api/v1/employees')
    data = response.json()
    assert data[0]['department']['id'] == department['id']
    assert data[0]['department']['name'] == department['name']

def test_create_employee(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    employee_data = create_employee.json()
    assert create_employee.status_code == 201
    assert employee_data['fullname'] == 'test'
    assert employee_data['position'] == 'manager'
    assert employee_data['department']['name'] == 'test_department'
    assert employee_data['department']['id'] == department['id']

def test_check_wrong_department(client):
    result = client.post('/api/v1/employees',
                          json={
                              'fullname': 'test',
                              'position': 'manager',
                              'department_id': 777
                          })
    assert result.status_code == 404
    assert result.json()['detail'] == "Department not found."

def test_update_employee(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 201
    employee_id = create_employee.json()['id']

    update_employee = client.patch(f'/api/v1/employees/{employee_id}',
                                   json={
                                       'position': 'IT'
                                   })
    result = update_employee.json()
    assert update_employee.status_code == 200
    assert result['fullname'] == "test"
    assert result['position'] == 'IT'
    assert result['department']['name'] == 'test_department'
    assert result['department']['id'] == department['id']

def test_change_department(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 201
    employee_id = create_employee.json()['id']

    create_department = client.post('/api/v1/departments',
                                    json={
                                        'name': 'another department'
                                    })
    assert create_department.status_code == 201
    change_department_id = create_department.json()['id']

    change_department_to_employee = client.patch(f'/api/v1/employees/{employee_id}',
                                                 json={
                                                     'department_id': change_department_id
                                                 })

    result = change_department_to_employee.json()
    assert change_department_to_employee.status_code == 200
    assert result['fullname'] == 'test'
    assert result['position'] == 'manager'
    assert result['department']['id'] == change_department_id
    assert result['department']['name'] == 'another department'

def test_change_wrong_department_to_employee(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 201
    employee_id = create_employee.json()['id']

    change_department_to_employee = client.patch(f'/api/v1/employees/{employee_id}',
                                                 json={
                                                     'department_id': 777
                                                 })
    assert change_department_to_employee.status_code == 404
    assert change_department_to_employee.json()['detail'] == 'Department not found.'

def test_change_wrong_employee(client, department):
    update_wrong_employee = client.patch(f'/api/v1/employees/{7777}',
                                         json={
                                             'fullname': 'test',
                                             'position': 'IT',
                                             'department_id': department['id']
                                         })

    assert update_wrong_employee.status_code == 404
    assert update_wrong_employee.json()['detail'] == 'Employee not found.'

def test_delete_employee(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'manager',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 201
    employee_id = create_employee.json()['id']

    delete_employee = client.delete(f'/api/v1/employees/{employee_id}')
    assert delete_employee.status_code == 200

    check_deleted_employee = client.get('/api/v1/employees/')
    list_data = check_deleted_employee.json()
    assert check_deleted_employee.status_code == 200
    assert list_data == []

def test_delete_wrong_employee(client):
    delete_wrong_employee = client.delete(f'/api/v1/employees/{999}')
    assert delete_wrong_employee.status_code == 404
    assert delete_wrong_employee.json()['detail'] == 'Employee not found.'

def test_create_employee_validation_error(client, department):
    create_employee = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'department_id': department['id']
                                  })
    assert create_employee.status_code == 422





