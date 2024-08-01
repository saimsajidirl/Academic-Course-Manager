import unittest
from unittest.mock import patch
from flask import request
from restapi_flask import app  # Import your Flask app
class TestAddItem(unittest.TestCase):

    @patch('your_app.sos_collection.update_one')  # Mock MongoDB interaction
    def test_add_item_success(self, mock_update_one):
        data = {
            'subject_name': 'Math',
            'description': 'Calculus',
            'course_code': 'MATH101',
            'teacher_name': 'Dr. Smith'
        }
        with app.test_client() as client:
            response = client.post('/sos', json=data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json, {'message': 'Item added successfully'})
            mock_update_one.assert_called_once_with({'semester': 'Semester 1'}, {'$push': {'courses': 'Math: Calculus (MATH101, Dr. Smith)'}}, upsert=True)

    @patch('your_app.sos_collection.update_one')
    def test_add_item_missing_fields(self, mock_update_one):
        data = {'description': 'Calculus', 'course_code': 'MATH101', 'teacher_name': 'Dr. Smith'}
        with app.test_client() as client:
            response = client.post('/sos', json=data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'error': 'Missing required fields'})
            mock_update_one.assert_not_called()
class TestGetItems(unittest.TestCase):

    @patch('your_app.sos_collection.find_one')
    def test_get_items_success(self, mock_find_one):
        mock_find_one.return_value = {'courses': ['Course 1', 'Course 2']}
        with app.test_client() as client:
            response = client.get('/sos')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'courses': ['Course 1', 'Course 2']})

    @patch('your_app.sos_collection.find_one')
    def test_get_items_semester_not_found(self, mock_find_one):
        mock_find_one.return_value = None
        with app.test_client() as client:
            response = client.get('/sos')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json, {'error': 'Semester not found'})
class TestRemoveItem(unittest.TestCase):

    @patch('your_app.sos_collection.update_one')
    def test_remove_item_success(self, mock_update_one):
        with app.test_client() as client:
            response = client.delete('/sos', query_string={'selected_item': 'Course 1'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'message': 'Item removed successfully'})
            mock_update_one.assert_called_once_with({'semester': 'Semester 1'}, {'$pull': {'courses': 'Course 1'}})

    @patch('your_app.sos_collection.update_one')
    def test_remove_item_missing_item_parameter(self, mock_update_one):
        with app.test_client() as client:
            response = client.delete
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'error': 'Missing selected_item parameter'})
            mock_update_one.assert_not_called()


if __name__ == '__main__':
    unittest.main()
