"""Tab 2: Manual data entry form."""

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_label, create_body_label, create_entry,
    create_secondary_button, set_entry_error,
)
from app.models.cliente import Cliente
from app.core.validators import REQUIRED_FIELDS_MANUAL, validate_cpf


UF_LIST = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO",
]

FIELD_DEFS = [
    # (group, field_name, label, required, is_uf_dropdown)
    ("Dados Pessoais", "nome_completo", "Nome Completo *", True, False),
    ("Dados Pessoais", "nacionalidade", "Nacionalidade *", True, False),
    ("Dados Pessoais", "estado_civil", "Estado Civil *", True, False),
    ("Dados Pessoais", "profissao", "Profissão", False, False),
    ("Dados Pessoais", "rg", "RG *", True, False),
    ("Dados Pessoais", "cpf", "CPF *", True, False),
    ("Endereço", "logradouro_numero", "Logradouro e Número *", True, False),
    ("Endereço", "complemento", "Complemento", False, False),
    ("Endereço", "bairro", "Bairro *", True, False),
    ("Endereço", "cidade", "Cidade *", True, False),
    ("Endereço", "uf", "UF *", True, True),
    ("Endereço", "cep", "CEP *", True, False),
    ("Contato", "email", "E-mail", False, False),
    ("Contato", "telefone", "Telefone(s)", False, False),
    ("Dados do Caso", "parte_contraria", "Parte Contrária / Réu *", True, False),
]


class TabManual(ctk.CTkFrame):
    """Manual data entry tab with grouped form fields."""

    def __init__(self, parent, on_data_changed=None):
        super().__init__(parent, fg_color=FUNDO)
        self.on_data_changed = on_data_changed
        self.entries: dict[str, ctk.CTkEntry | ctk.CTkComboBox] = {}
        self.cpf_warning_label = None

        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color=FUNDO)
        scroll.pack(fill="both", expand=True, padx=10, pady=5)

        current_group = None
        for group, field_name, label, required, is_uf in FIELD_DEFS:
            if group != current_group:
                current_group = group
                group_label = create_section_label(scroll, group)
                group_label.pack(fill="x", padx=5, pady=(10, 2))

            row = ctk.CTkFrame(scroll, fg_color=FUNDO)
            row.pack(fill="x", padx=5, pady=2)

            lbl = ctk.CTkLabel(
                row, text=label, font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                text_color=BODY_TEXT_COLOR, width=200, anchor="w",
            )
            lbl.pack(side="left")

            if is_uf:
                widget = ctk.CTkComboBox(
                    row, values=UF_LIST,
                    font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                    fg_color=ENTRY_BG, border_color=ENTRY_BORDER,
                    text_color=BODY_TEXT_COLOR,
                    button_color=DOMINANTE, button_hover_color=ACENTO,
                    dropdown_fg_color=ENTRY_BG, dropdown_text_color=BODY_TEXT_COLOR,
                    dropdown_hover_color=ACENTO,
                    corner_radius=4, border_width=1,
                    state="readonly",
                )
                widget.set("")
                widget.pack(side="left", fill="x", expand=True)
            else:
                widget = create_entry(row, placeholder=label.replace(" *", ""))
                widget.pack(side="left", fill="x", expand=True)
                widget.bind("<KeyRelease>", lambda e: self._on_field_changed())

            self.entries[field_name] = widget

            # CPF warning label
            if field_name == "cpf":
                self.cpf_warning_label = ctk.CTkLabel(
                    scroll, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    text_color=AVISO, anchor="w",
                )

        # Clear button
        btn_row = ctk.CTkFrame(scroll, fg_color=FUNDO)
        btn_row.pack(fill="x", padx=5, pady=(15, 10))

        clear_btn = create_secondary_button(btn_row, "Limpar", command=self.clear_form, width=100)
        clear_btn.pack(side="left")

    def _on_field_changed(self):
        # Validate CPF on change
        cpf_entry = self.entries.get("cpf")
        if cpf_entry and self.cpf_warning_label:
            cpf_val = cpf_entry.get().strip()
            if cpf_val and not validate_cpf(cpf_val):
                self.cpf_warning_label.configure(text="⚠ CPF com dígitos verificadores inválidos")
                self.cpf_warning_label.pack(fill="x", padx=5, pady=(0, 2))
            else:
                self.cpf_warning_label.pack_forget()

        if self.on_data_changed:
            self.on_data_changed()

    def clear_form(self):
        """Reset all form fields."""
        for field_name, widget in self.entries.items():
            if isinstance(widget, ctk.CTkComboBox):
                widget.set("")
            else:
                widget.delete(0, "end")
                set_entry_error(widget, False)
        if self.cpf_warning_label:
            self.cpf_warning_label.pack_forget()
        if self.on_data_changed:
            self.on_data_changed()

    def validate(self) -> list[str]:
        """Validate required fields. Returns list of missing field names."""
        missing = []
        for group, field_name, label, required, is_uf in FIELD_DEFS:
            widget = self.entries[field_name]
            if required:
                val = widget.get().strip() if hasattr(widget, 'get') else ""
                if not val:
                    missing.append(field_name)
                    if isinstance(widget, ctk.CTkEntry):
                        set_entry_error(widget, True)
                else:
                    if isinstance(widget, ctk.CTkEntry):
                        set_entry_error(widget, False)
        return missing

    def get_client(self) -> Cliente | None:
        """Build a Cliente from the form data. Returns None if required fields missing."""
        missing = self.validate()
        if missing:
            return None

        kwargs = {}
        for field_name, widget in self.entries.items():
            kwargs[field_name] = widget.get().strip() if hasattr(widget, 'get') else ""

        return Cliente(**kwargs)

    def has_data(self) -> bool:
        """Return True if at least the name field is filled."""
        nome = self.entries.get("nome_completo")
        if nome:
            return bool(nome.get().strip())
        return False
