import pytest
import json

search_mauriceharris = [{'job': 'Development worker, international aid', 'company': 'King-Howarth', 'ssn': 'ZZ299609T', \
                'residence': 'Studio 62i\nFrost alley\nSouth Jean\nN3W 2QA', 'current_location': [44.5767695, 129.747714], \
                'blood_group': '0+', 'website': ['https://webb.com/', 'https://jones-williams.com/', 'http://www.williams.biz/'],\
                'username': 'mauriceharris', 'name': 'Donald Holden', 'sex': 'F', 'address': 'Studio 5\nTucker squares\nHutchinsonburgh\nS86 2GH',\
                'mail': 'fishercheryl@gmail.com', 'birthdate': '1998-03-04'}, 
                {'job': 'Exhibition designer', 'company': 'Berry, Grant and Anderson','ssn': 'ZZ489841T', \
                'residence': 'Flat 59\nBarlow harbors\nWilliamsside\nM1 3YU', 'current_location': [-88.463234, -74.274428], \
                'blood_group': 'A+', 'website': ['https://griffiths.com/', 'http://www.cunningham.net/'], \
                'username': 'mauriceharris', 'name': 'Harriet Armstrong', 'sex': 'F', 'address': '09 Charlie motorway\nNorth Paigeville\nM1T 0PD', \
                'mail': 'marc07@gmail.com', 'birthdate': '1988-02-13'}]
    
endpoint_error = b'["Endpoint does not exist"]\n'
method_not_implement = b'{"message": "The method is not allowed for the requested URL."}\n'
username_not_found = b'["username not found"]\n'

def test_unimplemented_endpoint(app_t):
    response = app_t.get("/abc")
    assert response.status_code == 404
    assert response.data == endpoint_error
    response2 = app_t.post("/people")
    assert response2.status_code == 405
    assert response2.data == method_not_implement

def test_search(app_t):
    """
    test for searching by username, test exist one and absent one
    """

    response = app_t.get("/search/abc")
    assert response.status_code == 500
    assert response.data == username_not_found
    response2 = app_t.get("/search/mauriceharris")
    assert response2.status_code ==200
    assert json.loads(response2.data)["data"] == search_mauriceharris

def test_pagination(app_t, dl_t):
    """
    test for pagination using pass parameter by url and default value
    """

    response = app_t.get("/people?page=0&pageSize=5")
    expected = dl_t.data[0:5]
    assert response.status_code == 200
    assert json.loads(response.data)["data"] == expected
    response = app_t.get("/people")
    expected = dl_t.data[0:1000]
    assert response.status_code == 200
    assert json.loads(response.data)["data"] == expected

def test_delete(app_t):
    """
    test delete for exist and double delete for ensure delete the target
    """

    target = "mauriceharris"
    response = app_t.delete("/people/{}".format(target))
    assert response.status_code == 200
    assert json.loads(response.data)["data"] == "Delete {}".format(target)
    response2 = app_t.delete("/people/{}".format(target))
    assert response2.status_code == 500
    assert response2.data == username_not_found

def test_pagination_after_delete(app_t, db_t):
    """
    test the pagination consistancy after delete,
    twong is the first appear username
    """

    target = "twong"
    response = app_t.get("/people")
    expected = db_t.searchRange(0,10)
    assert response.status_code == 200
    assert json.loads(response.data)["data"] == expected 
    response2 = app_t.delete("/people/{}".format(target))
    assert response2.status_code == 200
    assert json.loads(response2.data)["data"] == "Delete {}".format(target) 
    response3 = app_t.get("/people")
    expected = db_t.searchRange(0,10)
    assert response3.status_code == 200
    assert json.loads(response3.data)["data"] == expected 
     
    