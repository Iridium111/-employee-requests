
def test_create_request(client, author, executor):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': author['id'],
                                     'executor_id': executor['id']
                                 })
    request_data = create_request.json()
    assert create_request.status_code == 201
    assert request_data['status'] == 'CREATED'
    assert request_data['description'] == 'test_description'
    assert request_data['author']['id'] == author['id']
    assert request_data['executor']['id'] == executor['id']
    assert request_data['number'] is not None

def test_create_request_author_not_found(client, executor):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': 777,
                                     'executor_id': executor['id']
                                 })
    assert create_request.status_code == 404
    assert create_request.json()['detail'] == 'Author not found.'

def test_create_request_executor_not_found(client, author):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': author['id'],
                                     'executor_id': 777
                                 })
    assert create_request.status_code == 404
    assert create_request.json()['detail'] == 'Executor not found.'

def test_get_requests(client, author, executor):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': author['id'],
                                     'executor_id': executor['id']
                                 })
    assert create_request.status_code == 201
    response = client.get('/api/v1/requests')
    assert response.status_code == 200

    data = response.json()
    assert data[0]['description'] == 'test_description'
    assert data[0]['author']['id'] == author['id']
    assert data[0]['executor']['id'] == executor['id']

def test_update_request(client, author, executor):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': author['id'],
                                     'executor_id': executor['id']
                                 })
    assert create_request.status_code == 201
    request_id = create_request.json()['id']

    update_request = client.patch(f'/api/v1/requests/{request_id}',
                                   json={
                                       'description': 'test'
                                   })
    assert update_request.status_code == 200
    assert update_request.json()['description'] == 'test'
    assert update_request.json()['author']['id'] == author['id']
    assert update_request.json()['executor']['id'] == executor['id']

def test_update_request_not_found(client):
    update_request = client.patch(f'/api/v1/requests/{777}',
                                  json={
                                      'description': 'test'
                                  })
    assert update_request.status_code == 404
    assert update_request.json()['detail'] == 'Request not found.'

def test_update_request_executor(client, department, created_request):
    create_executor = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test',
                                      'position': 'test',
                                      'department_id': department['id']
                                  })
    assert create_executor.status_code == 201
    executor_id = create_executor.json()['id']

    update_request = client.patch(f'/api/v1/requests/{created_request["id"]}',
                                  json={
                                      'executor_id': executor_id
                                  })
    assert update_request.status_code == 200
    assert update_request.json()['executor']['id'] == executor_id

def test_update_request_executor_not_found(client, created_request):
    update_request = client.patch(f'/api/v1/requests/{created_request["id"]}',
                                  json={
                                      'executor_id': 777
                                  })
    assert update_request.status_code == 404
    assert update_request.json()['detail'] == 'Executor not found.'

def test_delete_request(client, created_request):
    delete_request = client.delete(f'/api/v1/requests/{created_request["id"]}',)
    assert delete_request.status_code == 200

    check_delete_request = client.get(f'/api/v1/requests')
    assert check_delete_request.status_code == 200

    list_data = check_delete_request.json()
    assert list_data == []

def test_delete_request_not_found(client):
    delete_request = client.delete(f'/api/v1/requests/{777}')

    assert delete_request.status_code == 404
    assert delete_request.json()['detail'] == 'Request not found.'

def test_change_status_created_to_in_progress(client, created_request):
    update_status_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'IN_PROGRESS'
                                         })
    assert update_status_request.status_code == 200
    assert update_status_request.json()['status'] == 'IN_PROGRESS'

def test_change_status_created_to_cancelled(client, created_request):
    update_status_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'CANCELLED'
                                         })
    assert update_status_request.status_code == 200
    assert update_status_request.json()['status'] == 'CANCELLED'

def test_change_status_in_progress_to_done(client, created_request):
    update_status_in_progress_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'IN_PROGRESS'
                                         })
    assert update_status_in_progress_request.status_code == 200
    assert update_status_in_progress_request.json()['status'] == 'IN_PROGRESS'

    update_status_done_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                              json={
                                                  'status': 'DONE'
                                              })
    assert update_status_done_request.status_code == 200
    assert update_status_done_request.json()['status'] == 'DONE'

def test_change_status_in_progress_to_cancelled(client, created_request):
    update_status_in_progress_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                                     json={
                                                         'status': 'IN_PROGRESS'
                                                     })
    assert update_status_in_progress_request.status_code == 200
    assert update_status_in_progress_request.json()['status'] == 'IN_PROGRESS'

    update_status_cancelled_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                                   json={
                                                       'status': 'CANCELLED'
                                                   })
    assert update_status_cancelled_request.status_code == 200
    assert update_status_cancelled_request.json()['status'] == 'CANCELLED'

def test_invalid_status_transition_created_to_done(client, created_request):
    update_status_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'DONE'
                                         })
    assert update_status_request.status_code == 400
    assert update_status_request.json()['detail'] == 'Transition from CREATED to DONE is not allowed.'

def test_invalid_status_transition_done(client, created_request):
    update_status_in_progress_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'IN_PROGRESS'
                                         })
    assert update_status_in_progress_request.status_code == 200
    assert update_status_in_progress_request.json()['status'] == 'IN_PROGRESS'

    update_status_done_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                              json={
                                                  'status': 'DONE'
                                              })
    assert update_status_done_request.status_code == 200
    assert update_status_done_request.json()['status'] == 'DONE'

    update_status_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'IN_PROGRESS'
                                         })
    assert update_status_request.status_code == 400
    assert update_status_request.json()['detail'] == 'Transition from DONE to IN_PROGRESS is not allowed.'

def test_invalid_status_transition_cancelled(client, created_request):
    update_status_in_progress_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                                     json={
                                                         'status': 'IN_PROGRESS'
                                                     })
    assert update_status_in_progress_request.status_code == 200
    assert update_status_in_progress_request.json()['status'] == 'IN_PROGRESS'

    update_status_done_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                              json={
                                                  'status': 'CANCELLED'
                                              })
    assert update_status_done_request.status_code == 200
    assert update_status_done_request.json()['status'] == 'CANCELLED'

    update_status_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                         json={
                                             'status': 'IN_PROGRESS'
                                         })
    assert update_status_request.status_code == 400
    assert update_status_request.json()['detail'] == 'Transition from CANCELLED to IN_PROGRESS is not allowed.'

def test_change_status_request_not_found(client):
    update_status_request = client.patch(f'/api/v1/requests/{777}/status',
                                         json={
                                             'status': "IN_PROGRESS"
                                         })
    assert update_status_request.status_code == 404
    assert update_status_request.json()['detail'] == 'Request not found.'

def test_change_wrong_status(client, created_request):
    update_status_in_progress_request = client.patch(f'/api/v1/requests/{created_request["id"]}/status',
                                                     json={
                                                         'status': 'BANANA'
                                                     })
    assert update_status_in_progress_request.status_code == 422
    detail = update_status_in_progress_request.json()['detail']
    assert detail[0]['input'] == 'BANANA'
    assert detail[0]['loc'] == ['body', 'status']



