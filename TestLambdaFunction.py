import unittest
from unittest.mock import patch, MagicMock
import lambda_function  # change this to the name of your lambda function file

class TestLambdaFunction(unittest.TestCase):
    @patch('lambda_function.psycopg2')
    def test_lambda_handler_success(self, mock_psycopg2):
        # mock Redshift connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_psycopg2.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # mock event and context
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "test-bucket",
                        },
                        "object": {
                            "key": "test-key"
                        }
                    }
                }
            ]
        }
        context = {}

        response = lambda_function.lambda_handler(event, context)

        # check if psycopg2.connect is called once
        mock_psycopg2.connect.assert_called_once()

        # check if cursor.execute is called once
        mock_cursor.execute.assert_called_once_with('CALL your_stored_procedure();')

        # check if cursor.close, conn.commit and conn.close are each called once
        mock_cursor.close.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

        # check the lambda response
        self.assertEqual(response, {
            'statusCode': 200,
            'body': 'Successfully processed S3 object test-key from bucket test-bucket and executed stored procedure.'
        })

    @patch('lambda_function.psycopg2')
    def test_lambda_handler_failure(self, mock_psycopg2):
        # mock Redshift connection
        mock_psycopg2.connect.side_effect = Exception("Unable to connect")

        # mock event and context
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "test-bucket",
                        },
                        "object": {
                            "key": "test-key"
                        }
                    }
                }
            ]
        }
        context = {}

        with self.assertRaises(Exception) as context:
            lambda_function.lambda_handler(event, context)
        
        self.assertTrue('Error connecting to Redshift' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
