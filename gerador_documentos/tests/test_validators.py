"""Tests for CPF, CEP, name normalization, and filename normalization."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.validators import (
    validate_cpf, normalize_cep, normalize_name, normalize_filename,
)


class TestValidateCPF:
    def test_valid_cpf(self):
        assert validate_cpf("529.982.247-25") is True

    def test_valid_cpf_digits_only(self):
        assert validate_cpf("52998224725") is True

    def test_invalid_cpf_wrong_digits(self):
        assert validate_cpf("529.982.247-26") is False

    def test_invalid_cpf_all_same(self):
        assert validate_cpf("111.111.111-11") is False

    def test_invalid_cpf_short(self):
        assert validate_cpf("123") is False

    def test_invalid_cpf_empty(self):
        assert validate_cpf("") is False

    def test_valid_cpf_another(self):
        assert validate_cpf("987.654.321-00") is True


class TestNormalizeCEP:
    def test_with_dash(self):
        assert normalize_cep("70000-000") == "70000-000"

    def test_without_dash(self):
        assert normalize_cep("70000000") == "70000-000"

    def test_with_spaces(self):
        assert normalize_cep(" 70000000 ") == "70000-000"

    def test_short_input(self):
        assert normalize_cep("123") == "123"


class TestNormalizeName:
    def test_title_case(self):
        # normalize_name applies Title Case but does not add accents
        assert normalize_name("joao silva") == "Joao Silva"

    def test_prepositions_lowercase(self):
        assert normalize_name("RINALDO DA SILVA SOARES") == "Rinaldo da Silva Soares"

    def test_multiple_prepositions(self):
        assert normalize_name("maria das gracas de souza") == "Maria das Gracas de Souza"

    def test_empty(self):
        assert normalize_name("") == ""

    def test_single_word(self):
        assert normalize_name("joao") == "Joao"

    def test_preposition_first(self):
        # "de" at start should be capitalized
        assert normalize_name("de souza") == "De Souza"


class TestNormalizeFilename:
    def test_basic_camelcase(self):
        assert normalize_filename("Rinaldo da Silva Soares") == "RinaldoDaSilvaSoares"

    def test_accents_removed(self):
        assert normalize_filename("João André São José") == "JoaoAndreSaoJose"

    def test_special_chars(self):
        # Parens are stripped, but "(teste)" stays attached to prior word in split
        assert normalize_filename("Maria (teste)") == "Mariateste"

    def test_special_chars_separate_words(self):
        assert normalize_filename("Maria - teste") == "MariaTeste"

    def test_empty(self):
        assert normalize_filename("") == ""

    def test_multiple_spaces(self):
        assert normalize_filename("João   da   Silva") == "JoaoDaSilva"

    def test_prepositions_capitalized(self):
        assert normalize_filename("João da Silva") == "JoaoDaSilva"
