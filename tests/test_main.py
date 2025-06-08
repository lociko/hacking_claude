"""
Tests for the main CLI application.
"""

import pytest
import sys
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, 'app')
from app.main import main


def test_main_basic_functionality():
    """Test basic main function execution."""
    with patch('sys.argv', ['main.py']):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = main()
            assert result == 0
            assert "Hello from Python CLI!" in fake_out.getvalue()


def test_main_verbose_mode():
    """Test main function with verbose flag."""
    with patch('sys.argv', ['main.py', '--verbose']):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = main()
            assert result == 0
            output = fake_out.getvalue()
            assert "Verbose mode enabled" in output
            assert "Hello from Python CLI!" in output


def test_main_version():
    """Test version argument."""
    with patch('sys.argv', ['main.py', '--version']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0