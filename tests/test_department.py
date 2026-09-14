def test_get_departments(client):
    create_test_departments = client.post('/api/v1/departments',
                           json={
                               "name": "test_department"
                           },)
    assert create_test_departments.status_code == 201

    response = client.get('api/v1/departments',)
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == 'test_department'

def test_create_department(client):
    response = client.post('/api/v1/departments',
                           json={
                               "name": "test_department"
                           },)

    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'test_department'

def test_update_department(client):
    create_test_department = client.post('/api/v1/departments',
                                         json={
                                             'name': 'test_department'
                                         },)

    created_data = create_test_department.json()
    response_id = created_data['id']

    response = client.patch(f'/api/v1/departments/{response_id}',
                            json={
                                'name': 'test_update_department'
                            },)
    updated_data = response.json()

    assert response.status_code == 200
    assert updated_data['name'] == 'test_update_department'
    assert updated_data['id'] == response_id

def test_delete_department(client):
    create_test_department = client.post('api/v1/departments',
                                         json={
                                             'name': 'test_department'
                                         },)
    created_data = create_test_department.json()
    response_id = created_data['id']

    response = client.delete(f'/api/v1/departments/{response_id}')

    deleted_data = response.json()

    assert response.status_code == 200
    assert deleted_data['id'] == response_id

    check_delete_department = client.get('/api/v1/departments/')

    list_data = check_delete_department.json()

    assert check_delete_department.status_code == 200
    assert list_data == []




