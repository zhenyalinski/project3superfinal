import csv
import logging

from app import db
from app.db.models import User, Song, Location
#from faker import Faker

def test_adding_user(application, filepath=None, list_of_locations=None, current_user=None):
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        #showing how to add a record
        #create a record
        user = User('zv3@njit.edu', 'testtest')
        #add it to get ready to be committed
        db.session.add(user)
        #call the commit
        #db.session.commit()
        #assert that we now have a new user
        #assert db.session.query(User).count() == 1
        #finding one user record by email
        user = User.query.filter_by(email='zv3@njit.edu').first()
        log.info(user)
        #asserting that the user retrieved is correct
        assert user.email == 'zv3@njit.edu'
        #this is how you get a related record ready for insert
        user.songs = [Song("test", "smap", "1900", "pop"), Song("test2", "te", "1800", "Folk")]
        #commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        #changing the title of the song
        song1.title = "SuperSongTitle"
        #saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        #checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0

        user.locations = [Location("Houston", "29.7863", "-95.3889", "5464251")]
        db.session.commit()
        assert db.session.query(Location).count() == 1
        location1 = Location.query.filter_by(title='Houston').first()
        assert location1.title == "Houston"
        location1.title = "Houston"
        db.session.commit()

        def test_add_user(client, application):
            application.app_context()
            application.config['WTF_CSRF_ENABLED'] = False
            log = logging.getLogger("myApp")
            data = {
                'email': "zv3@njit.edu",
                'password': "12345678"
            }
            response = client.post('/users/new', follow_redirects=True, data=data)
            log.info("response inside user_test / test_add_user: ")

            # log.info(response.status_code)
            # log.info(response.data)
            assert response.status_code == 200
            # verify response with assert calls
