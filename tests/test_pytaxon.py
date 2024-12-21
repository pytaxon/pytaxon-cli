import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from collections import defaultdict
from pytaxon import Pytaxon

@pytest.fixture
def pytaxon_instance():
    """Fixture para criar uma instância da classe Pytaxon."""
    return Pytaxon(source_id=1)

@patch("requests.post")
def test_connect_to_api_success(mock_post, pytaxon_instance):
    """Testa a conexão bem-sucedida com a API."""
    mock_post.return_value.status_code = 200
    with patch("time.sleep", return_value=None):  # Evita o delay nos testes
        pytaxon_instance.connect_to_api()

@patch("pandas.read_csv")
@patch("pandas.read_excel")
def test_read_spreadsheet_csv(mock_read_csv, mock_read_excel, pytaxon_instance):
    """Testa a leitura de um arquivo CSV."""
    mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    mock_read_excel.side_effect = ValueError("Não deveria ser chamado")
    file_path = "test_file.csv"
    with patch("os.path.basename", return_value=file_path):
        result = pytaxon_instance.read_spreadshet(file_path)
        assert isinstance(result, pd.DataFrame)

@patch("pandas.read_excel")
def test_read_spreadsheet_excel(mock_read_excel, pytaxon_instance):
    """Testa a leitura de um arquivo Excel."""
    mock_read_excel.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    file_path = "test_file.xlsx"
    with patch("os.path.basename", return_value=file_path):
        result = pytaxon_instance.read_spreadshet(file_path)
        assert isinstance(result, pd.DataFrame)

def test_read_spreadsheet_invalid_extension(pytaxon_instance):
    """Testa o comportamento ao tentar ler um arquivo com extensão inválida."""
    file_path = "tests/invalid_file.txt"
    with pytest.raises(ValueError):
        pytaxon_instance.read_spreadshet(file_path)

def test_read_columns_success(pytaxon_instance):
    """Testa a leitura de colunas existentes no DataFrame."""
    pytaxon_instance._original_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    column_vars = "col1, col2"
    with patch("builtins.print") as mock_print:
        pytaxon_instance.read_columns(column_vars)
        mock_print.assert_called_with("Columns choosed.")
