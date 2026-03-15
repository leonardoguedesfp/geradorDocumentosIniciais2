"""Read client data from Excel files (Microsoft Forms export format)."""

from openpyxl import load_workbook

from app.models.cliente import Cliente


# Expected column headers (row 3 in the spreadsheet)
COLUMN_MAP = {
    "Nome Completo": "nome_completo",
    "Nacionalidade": "nacionalidade",
    "Estado Civil": "estado_civil",
    "Profissão": "profissao",
    "RG": "rg",
    "CPF": "cpf",
    "Endereço (Logradouro e Número)": "logradouro_numero",
    "Bairro": "bairro",
    "Cidade": "cidade",
    "UF": "uf",
    "CEP": "cep",
    "E-mail": "email",
    "Telefone(s)": "telefone",
    "Parte Contrária / Réu": "parte_contraria",
}

REQUIRED_COLUMNS = {
    "Nome Completo", "Nacionalidade", "Estado Civil", "RG", "CPF",
    "Endereço (Logradouro e Número)", "Bairro", "Cidade", "UF", "CEP",
    "Parte Contrária / Réu",
}


def _find_header_row(ws) -> int | None:
    """Find the row containing column headers by looking for 'Nome Completo'."""
    for row_num in range(1, min(ws.max_row + 1, 10)):
        for col in range(1, ws.max_column + 1):
            val = ws.cell(row=row_num, column=col).value
            if val and str(val).strip() == "Nome Completo":
                return row_num
    return None


def read_excel(filepath: str) -> dict:
    """Read client data from Excel file.

    Returns dict with:
        - "clients": list of Cliente objects
        - "errors": list of error/warning strings
        - "missing_columns": list of missing required column names
        - "row_warnings": dict mapping row number to list of warning strings
    """
    result = {
        "clients": [],
        "errors": [],
        "missing_columns": [],
        "row_warnings": {},
    }

    try:
        wb = load_workbook(filepath, read_only=True, data_only=True)
    except Exception as e:
        result["errors"].append(f"Erro ao abrir arquivo: {e}")
        return result

    ws = wb.active

    header_row = _find_header_row(ws)
    if header_row is None:
        result["errors"].append(
            "Cabeçalho não encontrado. Verifique se a planilha contém "
            "a coluna 'Nome Completo' em uma das primeiras linhas."
        )
        wb.close()
        return result

    # Build column index mapping
    col_index = {}  # field_name -> column_number
    for col in range(1, ws.max_column + 1):
        val = ws.cell(row=header_row, column=col).value
        if val and str(val).strip() in COLUMN_MAP:
            field_name = COLUMN_MAP[str(val).strip()]
            col_index[field_name] = col

    # Check for missing required columns
    found_headers = set()
    for col in range(1, ws.max_column + 1):
        val = ws.cell(row=header_row, column=col).value
        if val:
            found_headers.add(str(val).strip())

    missing = REQUIRED_COLUMNS - found_headers
    if missing:
        result["missing_columns"] = sorted(missing)
        result["errors"].append(
            f"Colunas obrigatórias ausentes: {', '.join(sorted(missing))}"
        )

    # Read data rows
    for row_num in range(header_row + 1, ws.max_row + 1):
        # Skip completely empty rows
        values = []
        for col in range(1, ws.max_column + 1):
            v = ws.cell(row=row_num, column=col).value
            values.append(v)

        if all(v is None or str(v).strip() == "" for v in values):
            continue

        # Check if this is an instruction/footer row
        first_val = str(values[0]).strip() if values[0] else ""
        if first_val.startswith("ℹ") or first_val.startswith("Instrução") or first_val.startswith("Instruções"):
            continue

        kwargs = {}
        row_warnings = []
        for field_name, col_num in col_index.items():
            cell_val = ws.cell(row=row_num, column=col_num).value
            kwargs[field_name] = str(cell_val).strip() if cell_val is not None else ""

        # Check required fields
        required_fields_map = {
            "nome_completo": "Nome Completo",
            "nacionalidade": "Nacionalidade",
            "estado_civil": "Estado Civil",
            "rg": "RG",
            "cpf": "CPF",
            "logradouro_numero": "Endereço",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "uf": "UF",
            "cep": "CEP",
            "parte_contraria": "Parte Contrária",
        }
        for field, label in required_fields_map.items():
            if not kwargs.get(field):
                row_warnings.append(f"Campo obrigatório vazio: {label}")

        if row_warnings:
            result["row_warnings"][row_num] = row_warnings

        # Only add if at least nome_completo is present
        if kwargs.get("nome_completo"):
            cliente = Cliente(**kwargs)
            result["clients"].append((row_num, cliente))

    wb.close()
    return result
