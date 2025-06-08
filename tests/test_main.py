#!/usr/bin/env python3
"""
Unit tests for the CLI application.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import sys
import json
import os
from io import StringIO
import argparse
import requests
from app.main import main


class TestCLIApplication(unittest.TestCase):
    """Test cases for the CLI application."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_response_data = {
            "id": "123456",
            "title": "Test Security Report",
            "state": "resolved",
            "severity": "high"
        }

    @patch('sys.argv')
    @patch('builtins.print')
    def test_version_argument(self, mock_print, mock_argv):
        """Test --version argument."""
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--version'][index]
        mock_argv.__len__ = lambda self: 2

        with self.assertRaises(SystemExit) as cm:
            main()

        # argparse exits with code 0 for --version
        self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    def test_successful_report_fetch(self, mock_print, mock_get, mock_argv):
        """Test successful report fetching."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--report', '123456'][index]
        mock_argv.__len__ = lambda self: 3

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct URL
        mock_get.assert_called_once_with('https://hackerone.com/reports/123456.json')

        # Verify the JSON was printed
        expected_json = json.dumps(self.mock_response_data, indent=2)
        mock_print.assert_called_with(expected_json)

        self.assertEqual(result, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    def test_failed_report_fetch(self, mock_print, mock_get, mock_argv):
        """Test failed report fetching (non-200 status code)."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--report', '999999'][index]
        mock_argv.__len__ = lambda self: 3

        # Mock failed HTTP response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct URL
        mock_get.assert_called_once_with('https://hackerone.com/reports/999999.json')

        # Verify error message was printed
        mock_print.assert_called_with("Failed to fetch report")

        self.assertEqual(result, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    @patch.dict(os.environ, {}, clear=True)
    def test_verbose_and_report_together(self, mock_print, mock_get, mock_argv):
        """Test verbose flag with report argument."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--verbose', '--report', '123456'][index]
        mock_argv.__len__ = lambda self: 4

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify verbose messages, environment variables, and JSON were printed
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call("Environment variables:"),
            unittest.mock.call("  VERBOSE: Not set"),
            unittest.mock.call("  H1_API_TOKEN: Not set"),
            unittest.mock.call(json.dumps(self.mock_response_data, indent=2))
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    @patch.dict(os.environ, {}, clear=True)
    def test_short_flags(self, mock_print, mock_get, mock_argv):
        """Test short flag versions (-v, -r)."""
        # Mock command line arguments with short flags
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '-v', '-r', '123456'][index]
        mock_argv.__len__ = lambda self: 4

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify verbose messages, environment variables, and JSON were printed
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call("Environment variables:"),
            unittest.mock.call("  VERBOSE: Not set"),
            unittest.mock.call("  H1_API_TOKEN: Not set"),
            unittest.mock.call(json.dumps(self.mock_response_data, indent=2))
        ]
        mock_print.assert_has_calls(expected_calls)

        self.assertEqual(result, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    def test_requests_exception(self, mock_print, mock_get, mock_argv):
        """Test handling of requests exceptions."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--report', '123456'][index]
        mock_argv.__len__ = lambda self: 3

        # Mock requests.get to raise an exception
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with self.assertRaises(requests.exceptions.ConnectionError):
            main()

    @patch('sys.argv')
    def test_help_argument(self, mock_argv):
        """Test --help argument."""
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--help'][index]
        mock_argv.__len__ = lambda self: 2

        with self.assertRaises(SystemExit) as cm:
            main()

        # argparse exits with code 0 for --help
        self.assertEqual(cm.exception.code, 0)

    @patch('sys.argv')
    @patch('builtins.print')
    def test_missing_report_argument(self, mock_print, mock_argv):
        """Test behavior when --report argument is missing."""
        # Mock command line arguments without --report
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py'][index]
        mock_argv.__len__ = lambda self: 1

        result = main()

        # Verify error message was printed and exit code is 1
        mock_print.assert_called_with("Error: --report argument is required")
        self.assertEqual(result, 1)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    @patch.dict(os.environ, {'H1_API_TOKEN': 'test_token_123'}, clear=True)
    def test_api_token_header(self, mock_print, mock_get, mock_argv):
        """Test that API_TOKEN header is added when H1_API_TOKEN env var is set."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--report', '123456'][index]
        mock_argv.__len__ = lambda self: 3

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify the API was called with correct headers
        mock_get.assert_called_once_with(
            'https://hackerone.com/reports/123456.json',
            headers={'API_TOKEN': 'test_token_123'}
        )

        self.assertEqual(result, 0)

    @patch('sys.argv')
    @patch('requests.get')
    @patch('builtins.print')
    @patch.dict(os.environ, {'H1_API_TOKEN': 'test_token_123', 'VERBOSE': '1'}, clear=True)
    def test_verbose_mode_with_env_vars(self, mock_print, mock_get, mock_argv):
        """Test verbose mode shows environment variables."""
        # Mock command line arguments
        mock_argv.__getitem__ = lambda self, index: ['cli_app.py', '--report', '231502v'][index]
        mock_argv.__len__ = lambda self: 3

        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data
        mock_get.return_value = mock_response

        result = main()

        # Verify verbose output includes environment variables
        expected_calls = [
            unittest.mock.call("Verbose mode enabled"),
            unittest.mock.call("Environment variables:"),
            unittest.mock.call("  VERBOSE: 1"),
            unittest.mock.call("  H1_API_TOKEN: Set"),
            unittest.mock.call(json.dumps(self.mock_response_data, indent=2))
        ]
        mock_print.assert_has_calls(expected_calls)

        # Verify API called with token
        mock_get.assert_called_once_with(
            'https://hackerone.com/reports/231502v.json',
            headers={'API_TOKEN': 'test_token_123'}
        )

        self.assertEqual(result, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests that test the full flow."""

    @patch('requests.get')
    @patch.dict(os.environ, {}, clear=True)
    def test_full_workflow_integration(self, mock_get):
        """Test the complete workflow with mocked HTTP requests."""
        # Mock successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "integration_test",
            "title": "Integration Test Report"
        }
        mock_get.return_value = mock_response

        # Capture stdout
        captured_output = StringIO()

        with patch('sys.stdout', captured_output), \
                patch('sys.argv', ['cli_app.py', '--verbose', '--report', 'test123']):
            result = main()

            output = captured_output.getvalue()

            # Verify verbose message is in output
            self.assertIn("Verbose mode enabled", output)
            self.assertIn("Environment variables:", output)

            # Verify JSON is in output
            self.assertIn("integration_test", output)
            self.assertIn("Integration Test Report", output)

            self.assertEqual(result, 0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
