from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_page(self):
        """Test Home Page"""
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('numPlays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)


    def test_word(self):
        """Test if word is valid"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["M", "A", "Z", "E", "O"], 
                                 ["C", "B", "N", "A", "L"], 
                                 ["W", "E", "U", "T", "Q"], 
                                 ["X", "T", "O", "E", "Z"], 
                                 ["Y", "H", "T", "E", "P"]]
        response = self.client.get('/check-word?word=maze')
        self.assertEqual(response.json['result'], 'ok')


    def test_invalid_word(self):
        """Test Dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')


    def test_not_real(self):
        """Test if word is on the board"""
        self.client.get('/')
        response = self.client.get(
            '/check-word?word=kjhkbkytvy')
        self.assertEqual(response.json['result'], 'not-word')