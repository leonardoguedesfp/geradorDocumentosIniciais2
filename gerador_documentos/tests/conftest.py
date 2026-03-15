"""Shared fixtures for all tests."""

import os
import sys
import json
import tempfile
import shutil

import pytest

# Ensure gerador_documentos is in sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def tmp_dir():
    """Create a temporary directory, cleaned up after test."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def templates_dir(tmp_dir):
    """Create a temporary directory with the three template files from __templates_padrao__."""
    src = os.path.join(os.path.dirname(__file__), "..", "..", "__templates_padrao__")
    src = os.path.abspath(src)
    for fname in [
        "Procuracao_TEMPLATE.docx",
        "Declaracao_Hipossuficiencia_TEMPLATE.docx",
        "Contrato_Prestacao_Servicos_TEMPLATE.docx",
    ]:
        src_file = os.path.join(src, fname)
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(tmp_dir, fname))
    return tmp_dir


@pytest.fixture
def output_dir(tmp_dir):
    """Create a dedicated output directory."""
    out = os.path.join(tmp_dir, "output")
    os.makedirs(out)
    return out


@pytest.fixture
def config_file(tmp_dir):
    """Create a temporary config.json path."""
    return os.path.join(tmp_dir, "config.json")


@pytest.fixture
def sample_client_data():
    """Return sample client data dict for placeholder substitution."""
    return {
        "NOME_COMPLETO": "João da Silva Souza",
        "NACIONALIDADE": "brasileiro",
        "ESTADO_CIVIL": "solteiro",
        "PROFISSAO": "analista de sistemas",
        "RG": "1234567",
        "CPF": "529.982.247-25",
        "ENDERECO_COMPLETO": "Rua das Flores, 123 — Asa Sul, Brasília (DF), CEP 70000-000",
        "EMAIL": "joao@email.com",
        "TELEFONE": "(61) 99999-0000",
        "PARTE_CONTRARIA": "Empresa XYZ Ltda",
        "DATA_EXTENSO": "15 de março de 2026",
    }
