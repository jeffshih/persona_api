from src.database import database
import pytest



def test_range_search(dl_t, db_t):
    """
    test the search result is equivilent to the expected result
    """
    start = 5
    end = 10
    res = db_t.searchRange(start, end)
    expected = dl_t.data[start:end]
    #print(res)
    assert(len(res) != 0)
    assert(res==expected)

def test_search_success(db_t):
    """
    test search for profile in db
    """
    expected = [{'job': 'Development worker, international aid', 'company': 'King-Howarth', 'ssn': 'ZZ299609T', \
                'residence': 'Studio 62i\nFrost alley\nSouth Jean\nN3W 2QA', 'current_location': [44.5767695, 129.747714], \
                'blood_group': '0+', 'website': ['https://webb.com/', 'https://jones-williams.com/', 'http://www.williams.biz/'],\
                'username': 'mauriceharris', 'name': 'Donald Holden', 'sex': 'F', 'address': 'Studio 5\nTucker squares\nHutchinsonburgh\nS86 2GH',\
                'mail': 'fishercheryl@gmail.com', 'birthdate': '1998-03-04'}, 
                {'job': 'Exhibition designer', 'company': 'Berry, Grant and Anderson','ssn': 'ZZ489841T', \
                'residence': 'Flat 59\nBarlow harbors\nWilliamsside\nM1 3YU', 'current_location': [-88.463234, -74.274428], \
                'blood_group': 'A+', 'website': ['https://griffiths.com/', 'http://www.cunningham.net/'], \
                'username': 'mauriceharris', 'name': 'Harriet Armstrong', 'sex': 'F', 'address': '09 Charlie motorway\nNorth Paigeville\nM1T 0PD', \
                'mail': 'marc07@gmail.com', 'birthdate': '1988-02-13'}]
    res = db_t.search("mauriceharris")
    print(res)
    assert(res == expected)

def test_search_fail(db_t):
    """
    test when searching target is invalid.
    """
    res = db_t.search("abc")
    assert(res is None)




#print(d.get("mauriceharris"))