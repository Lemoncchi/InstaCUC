import unittest

from flask import abort

from instacuc import app, db
from instacuc.models import Message
from instacuc.commands import forge, initdb


class InstaCUCTestCase(unittest.TestCase):

    def setUp(self):
        app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all()
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        self.assertFalse(app is None)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/nothing')
        data = response.get_data(as_text=True)
        self.assertIn('404 Error', data)
        self.assertIn('Go Back', data)
        self.assertEqual(response.status_code, 404)

    def test_500_page(self):
        # create route to abort the request with the 500 Error
        @app.route('/500')
        def internal_server_error_for_test():
            abort(500)

        response = self.client.get('/500')
        data = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 500)
        self.assertIn('500 Error', data)
        self.assertIn('Go Back', data)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Insta CUC', data)
    
    def test_create_message(self):
        import io
        with open('uploads/example_CUC/0Q0A1580.JPG', 'rb') as test_post_img:
            with io.BytesIO(test_post_img.read()) as imgBytesIO:
                response = self.client.post('/', content_type='multipart/form-data', data=dict(
                    name='Peter',
                    body='Hello, world.',
                    hidden_message='Hello, hidden.',
                    photo=(imgBytesIO, '0Q0A1580.JPG'),
                    # fake=True
                ), follow_redirects=True)
                data = response.get_data(as_text=True)
                self.assertIn('Your message have been sent to the world!', data)
                self.assertIn('Hello, world.', data)
    
    def test_create_message_with_hidden_Chinese(self):
        import io
        with open('uploads/example_CUC/0Q0A1580.JPG', 'rb') as test_post_img:
            with io.BytesIO(test_post_img.read()) as imgBytesIO:
                response = self.client.post('/', content_type='multipart/form-data', data=dict(
                    name='Peter',
                    body='Hello, world.',
                    hidden_message='测试中文隐藏信息',
                    photo=(imgBytesIO, '0Q0A1580.JPG'),
                    # fake=True
                ), follow_redirects=True)
                data = response.get_data(as_text=True)
                import os
                os.remove('uploads/0Q0A1580.jpg')  # 测试后删除图片
                self.assertIn('由于目前使用的水印算法会有部分误码，中文编码嵌入后解码效果惨不忍睹，所以目前只能输入英文 (⋟﹏⋞)', data)

    def test_form_validation(self):
        response = self.client.post('/', data=dict(
            name=' ',
            body='Hello, world.'
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('This field is required.', data)

    def test_forge_command(self):
        result = self.runner.invoke(forge)
        self.assertIn('Created 5 fake messages.', result.output)
        self.assertEqual(Message.query.count(), 5)

    def test_forge_command_with_count(self):
        result = self.runner.invoke(forge, ['--count', '50'])
        self.assertIn('Created 50 fake messages.', result.output)
        self.assertEqual(Message.query.count(), 50)

    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

    def test_initdb_command_with_drop(self):
        result = self.runner.invoke(initdb, ['--drop'], input='y\n')
        self.assertIn('This operation will delete the database, do you want to continue?', result.output)
        self.assertIn('Drop tables.', result.output)


if __name__ == '__main__':
    unittest.main()
