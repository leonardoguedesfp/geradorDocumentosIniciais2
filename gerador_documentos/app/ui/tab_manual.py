"""Tab 2: Manual data entry form with 2-column grid layout."""

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_title, create_body_label, create_entry,
    create_secondary_button, create_field_label, create_card, set_entry_error,
)
from app.models.cliente import Cliente
from app.core.validators import REQUIRED_FIELDS_MANUAL, validate_cpf


UF_LIST = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO",
]

# Fields definition: (group, field_name, label, required, is_uf_dropdown)
# Fields in the same group with consecutive indices are paired in 2-column grid
FIELD_GROUPS = [
    ("Dados Pessoais", [
        ("nome_completo", "Nome Completo *", True, False),
        ("cpf", "CPF *", True, False),
        ("nacionalidade", "Nacionalidade *", True, False),
        ("estado_civil", "Estado Civil *", True, False),
        ("profissao", "Profissão", False, False),
        ("rg", "RG *", True, False),
    ]),
    ("Endereço", [
        ("logradouro_numero", "Logradouro e Número *", True, False),
        ("complemento", "Complemento", False, False),
        ("bairro", "Bairro *", True, False),
        ("cidade", "Cidade *", True, False),
        ("uf", "UF *", True, True),
        ("cep", "CEP *", True, False),
    ]),
    ("Contato", [
        ("email", "E-mail", False, False),
        ("telefone", "Telefone(s)", False, False),
    ]),
    ("Dados do Caso", [
        ("parte_contraria", "Parte Contrária / Réu *", True, False),
    ]),
]


class TabManual(ctk.CTkFrame):
    """Manual data entry tab with grouped form fields in 2-column grid."""

    def __init__(self, parent, on_data_changed=None):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed
        self.entries: dict[str, ctk.CTkEntry | ctk.CTkComboBox] = {}
        self.cpf_warning_label = None

        self._build_ui()

    def _build_ui(self):
        card = create_card(self)
        card.pack(fill="both", expand=True, padx=0, pady=0)

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=16, pady=(8, 12))

        for group_name, fields in FIELD_GROUPS:
            # Group title
            group_label = create_section_title(scroll, group_name)
            group_label.pack(fill="x", pady=(12, 6))

            # Build fields in pairs (2-column grid)
            i = 0
            while i < len(fields):
                row = ctk.CTkFrame(scroll, fg_color="transparent")
                row.pack(fill="x", pady=2)

                # First field in pair
                field_name, label, required, is_uf = fields[i]
                self._create_field(row, field_name, label, required, is_uf, side="left")

                # Second field in pair (if exists)
                i += 1
                if i < len(fields):
                    field_name2, label2, required2, is_uf2 = fields[i]
                    self._create_field(row, field_name2, label2, required2, is_uf2, side="left")
                    i += 1
                else:
                    i += 1

            # CPF warning after Dados Pessoais group
            if group_name == "Dados Pessoais":
                self.cpf_warning_label = ctk.CTkLabel(
                    scroll, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
                    text_color=AVISO, anchor="w",
                )

        # Clear button
        btn_row = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_row.pack(fill="x", pady=(16, 8))

        clear_btn = create_secondary_button(btn_row, "Limpar", command=self.clear_form, width=100)
        clear_btn.pack(side="left")

    def _create_field(self, parent, field_name, label, required, is_uf, side="left"):
        """Create a single field (label + entry) in a column container."""
        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.pack(side=side, fill="x", expand=True, padx=(0, 8))

        lbl = create_field_label(col, label)
        lbl.pack(fill="x")

        if is_uf:
            widget = ctk.CTkComboBox(
                col, values=UF_LIST,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                fg_color=ENTRY_BG, border_color=ENTRY_BORDER,
                text_color=BODY_TEXT_COLOR,
                button_color=DOMINANTE, button_hover_color=BTN_PRIMARY_HOVER,
                dropdown_fg_color=CARD_BG, dropdown_text_color=BODY_TEXT_COLOR,
                dropdown_hover_color=BTN_SECONDARY_HOVER,
                corner_radius=ENTRY_RADIUS, border_width=1,
                state="readonly",
            )
            widget.set("")
            widget.pack(fill="x")
        else:
            widget = create_entry(col, placeholder=label.replace(" *", ""))
            widget.pack(fill="x")
            widget.bind("<KeyRelease>", lambda e: self._on_field_changed())

        self.entries[field_name] = widget

    def _on_field_changed(self):
        cpf_entry = self.entries.get("cpf")
        if cpf_entry and self.cpf_warning_label:
            cpf_val = cpf_entry.get().strip()
            if cpf_val and not validate_cpf(cpf_val):
                self.cpf_warning_label.configure(text="⚠ CPF com dígitos verificadores inválidos")
                self.cpf_warning_label.pack(fill="x", pady=(0, 2))
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
        for group_name, fields in FIELD_GROUPS:
            for field_name, label, required, is_uf in fields:
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
