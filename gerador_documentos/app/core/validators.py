"""Validation utilities: CPF, CEP, name normalization, required fields."""

import re
import unicodedata


PREPOSITIONS = {"da", "de", "do", "das", "dos", "e"}


def normalize_name(name: str) -> str:
    """Apply Title Case preserving lowercase prepositions (da, de, do, das, dos, e)."""
    if not name:
        return name
    words = name.strip().split()
    result = []
    for i, word in enumerate(words):
        if word.lower() in PREPOSITIONS and i > 0:
            result.append(word.lower())
        else:
            result.append(word.capitalize())
    return " ".join(result)


def normalize_cep(cep: str) -> str:
    """Normalize CEP to NNNNN-NNN format."""
    digits = re.sub(r"\D", "", cep)
    if len(digits) == 8:
        return f"{digits[:5]}-{digits[5:]}"
    return cep


def validate_cpf(cpf: str) -> bool:
    """Validate CPF check digits. Returns True if valid."""
    digits = re.sub(r"\D", "", cpf)
    if len(digits) != 11:
        return False
    if digits == digits[0] * 11:
        return False

    # First check digit
    total = sum(int(digits[i]) * (10 - i) for i in range(9))
    remainder = total % 11
    expected = 0 if remainder < 2 else 11 - remainder
    if int(digits[9]) != expected:
        return False

    # Second check digit
    total = sum(int(digits[i]) * (11 - i) for i in range(10))
    remainder = total % 11
    expected = 0 if remainder < 2 else 11 - remainder
    if int(digits[10]) != expected:
        return False

    return True


def normalize_filename(name: str) -> str:
    """Normalize name for filename: CamelCase, no spaces, no accents, no special chars.

    All words are capitalized (including prepositions like da, de, do) and joined
    without separators. Accents and special characters are removed.
    Example: "João da Silva Souza" → "JoaoDaSilvaSouza"
    """
    if not name:
        return ""
    # Remove accents
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
    # Split into words and capitalize each
    words = ascii_str.split()
    camel = "".join(word.capitalize() for word in words)
    # Remove any remaining non-alphanumeric characters
    camel = re.sub(r"[^a-zA-Z0-9]", "", camel)
    return camel


REQUIRED_FIELDS_MANUAL = [
    "nome_completo",
    "nacionalidade",
    "estado_civil",
    "rg",
    "cpf",
    "logradouro_numero",
    "bairro",
    "cidade",
    "uf",
    "cep",
    "parte_contraria",
]

REQUIRED_COLUMNS_EXCEL = [
    "Nome Completo",
    "Nacionalidade",
    "Estado Civil",
    "RG",
    "CPF",
    "Endereço (Logradouro e Número)",
    "Bairro",
    "Cidade",
    "UF",
    "CEP",
    "Parte Contrária / Réu",
]
