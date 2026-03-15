"""Placeholder substitution engine with fragmented-runs handling."""

from __future__ import annotations

import copy
import os
import re
from datetime import date

from docx import Document

from app.core.validators import normalize_filename


MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
    5: "maio", 6: "junho", 7: "julho", 8: "agosto",
    9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def data_extenso(d: date | None = None) -> str:
    """Generate date in format 'DD de mês por extenso de AAAA'."""
    if d is None:
        d = date.today()
    return f"{d.day} de {MESES[d.month]} de {d.year}"


def _replace_in_paragraph(paragraph, replacements: dict[str, str]) -> None:
    """Replace placeholders in a paragraph, handling fragmented runs.

    Strategy:
    1. Concatenate all runs text into a single string
    2. Check if any {{PLACEHOLDER}} exists
    3. If yes: perform replacements, then redistribute text across runs
       preserving the formatting of the first run that contained the placeholder
    """
    runs = paragraph.runs
    if not runs:
        return

    full_text = "".join(run.text for run in runs)

    if "{{" not in full_text:
        return

    # Perform all replacements
    new_text = full_text
    for placeholder, value in replacements.items():
        new_text = new_text.replace(f"{{{{{placeholder}}}}}", value)

    # Also replace any remaining {{...}} with empty string
    new_text = re.sub(r"\{\{\w+\}\}", "", new_text)

    if new_text == full_text:
        return

    # Redistribute text: put all text in the first run, clear the rest
    # This preserves the formatting of the first run
    if runs:
        # Find the first run that was part of a placeholder for better formatting
        # Default to first run's formatting
        runs[0].text = new_text
        for run in runs[1:]:
            run.text = ""


def _replace_in_table(table, replacements: dict[str, str]) -> None:
    """Replace placeholders in all cells of a table."""
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                _replace_in_paragraph(paragraph, replacements)


def fill_document(template_path: str, replacements: dict[str, str],
                  output_path: str) -> str:
    """Fill a template with replacements and save to output_path.

    Returns the output path on success, raises on error.
    """
    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        _replace_in_paragraph(paragraph, replacements)

    for table in doc.tables:
        _replace_in_table(table, replacements)

    doc.save(output_path)
    return output_path


DOC_TYPE_SUFFIXES = {
    "procuracao": "Procuracao",
    "declaracao": "DeclaracaoHipossuficiencia",
    "contrato": "Contrato",
}


def build_output_filename(nome_completo: str, doc_type: str,
                          existing_files: set[str] | None = None) -> str:
    """Build output filename: {NomeCamelCase}_{Documento}.docx

    If the filename already exists in existing_files, append _2, _3, etc.
    """
    nome_norm = normalize_filename(nome_completo)
    suffix = DOC_TYPE_SUFFIXES.get(doc_type, doc_type)
    base = f"{nome_norm}_{suffix}"
    filename = f"{base}.docx"

    if existing_files is None:
        return filename

    if filename not in existing_files:
        return filename

    version = 2
    while True:
        filename = f"{base}_{version}.docx"
        if filename not in existing_files:
            return filename
        version += 1


def generate_documents(
    cliente_data: dict[str, str],
    templates: dict[str, "TemplateInfo"],
    doc_types: list[str],
    output_folder: str,
    existing_files: set[str] | None = None,
) -> list[dict]:
    """Generate selected documents for a single client.

    Returns list of result dicts: {"doc_type": str, "success": bool, "path": str, "error": str}
    """
    from app.core.template_loader import TemplateInfo

    if existing_files is None:
        existing_files = set()

    # Add DATA_EXTENSO
    replacements = dict(cliente_data)
    if "DATA_EXTENSO" not in replacements:
        replacements["DATA_EXTENSO"] = data_extenso()

    results = []
    for doc_type in doc_types:
        template_info = templates.get(doc_type)
        if not template_info or not template_info.loaded:
            results.append({
                "doc_type": doc_type,
                "success": False,
                "path": "",
                "error": "Template não carregado",
            })
            continue

        filename = build_output_filename(
            replacements.get("NOME_COMPLETO", "documento"), doc_type, existing_files
        )
        output_path = os.path.join(output_folder, filename)

        # Also handle version suffix if file already exists on disk
        if os.path.exists(output_path):
            existing_files.add(filename)
            filename = build_output_filename(
                replacements.get("NOME_COMPLETO", "documento"), doc_type, existing_files
            )
            output_path = os.path.join(output_folder, filename)

        try:
            fill_document(template_info.path, replacements, output_path)
            existing_files.add(filename)
            results.append({
                "doc_type": doc_type,
                "success": True,
                "path": output_path,
                "error": "",
            })
        except Exception as e:
            results.append({
                "doc_type": doc_type,
                "success": False,
                "path": "",
                "error": str(e),
            })

    return results
