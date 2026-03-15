"""Tab 1: Excel / Microsoft Forms data source."""

import os
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_title, create_body_label, create_aux_label,
    create_primary_button, create_secondary_button, create_card,
)
from app.core.excel_reader import read_excel
from app.core.validators import validate_cpf


class TabExcel(ctk.CTkFrame):
    """Excel data source tab with client table and selection."""

    def __init__(self, parent, on_data_changed=None):
        super().__init__(parent, fg_color="transparent")
        self.on_data_changed = on_data_changed
        self.excel_data = None
        self.client_vars = []
        self.filepath = ""

        self._build_ui()

    def _build_ui(self):
        card = create_card(self)
        card.pack(fill="both", expand=True, padx=0, pady=0)

        # File selector row
        file_row = ctk.CTkFrame(card, fg_color="transparent")
        file_row.pack(fill="x", padx=16, pady=(12, 8))

        btn = create_primary_button(file_row, "Selecionar arquivo", command=self._select_file, width=160)
        btn.pack(side="left")

        self.file_label = create_aux_label(file_row, "Nenhum arquivo selecionado")
        self.file_label.pack(side="left", padx=10)

        # Error/warning area
        self.error_label = ctk.CTkLabel(
            card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=ERRO, anchor="w", wraplength=680,
        )

        # Buttons row
        self.btn_row = ctk.CTkFrame(card, fg_color="transparent")

        self.select_all_btn = create_secondary_button(
            self.btn_row, "Selecionar todos",
            command=self._select_all, width=130, height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        )
        self.select_all_btn.pack(side="left", padx=(0, 5))

        self.deselect_all_btn = create_secondary_button(
            self.btn_row, "Desmarcar todos",
            command=self._deselect_all, width=130, height=28,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        )
        self.deselect_all_btn.pack(side="left")

        # Scrollable table area
        self.table_frame = ctk.CTkScrollableFrame(
            card, fg_color=CARD_BG, border_color=CARD_BORDER,
            border_width=1, corner_radius=ENTRY_RADIUS,
        )

    def _select_file(self):
        filepath = filedialog.askopenfilename(
            title="Selecionar planilha de clientes",
            filetypes=[("Excel", "*.xlsx")],
        )
        if filepath:
            self.filepath = filepath
            self.file_label.configure(text=os.path.basename(filepath))
            self._load_data(filepath)

    def _load_data(self, filepath: str):
        self.client_vars.clear()
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.error_label.pack_forget()
        self.btn_row.pack_forget()
        self.table_frame.pack_forget()

        self.excel_data = read_excel(filepath)

        if self.excel_data["errors"]:
            self.error_label.configure(text="⚠ " + " | ".join(self.excel_data["errors"]))
            self.error_label.pack(fill="x", padx=16, pady=(5, 0))

        clients = self.excel_data["clients"]
        if not clients:
            if not self.excel_data["errors"]:
                self.error_label.configure(text="Nenhum cliente encontrado na planilha.")
                self.error_label.pack(fill="x", padx=16, pady=(5, 0))
            return

        self.btn_row.pack(fill="x", padx=16, pady=(5, 4))
        self.table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        # Header row
        header = ctk.CTkFrame(self.table_frame, fg_color=ENTRY_BG)
        header.pack(fill="x", pady=(0, 2))

        ctk.CTkLabel(header, text="", width=40).pack(side="left")
        ctk.CTkLabel(
            header, text="Nome", font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=TEXTO, width=200, anchor="w",
        ).pack(side="left", padx=5)
        ctk.CTkLabel(
            header, text="CPF", font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=TEXTO, width=120, anchor="w",
        ).pack(side="left", padx=5)
        ctk.CTkLabel(
            header, text="Parte Contrária", font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=TEXTO, width=200, anchor="w",
        ).pack(side="left", padx=5)
        ctk.CTkLabel(
            header, text="Status", font=(FONT_FAMILY, FONT_SIZE_SMALL, "bold"),
            text_color=TEXTO, width=100, anchor="w",
        ).pack(side="left", padx=5)

        row_warnings = self.excel_data.get("row_warnings", {})

        for row_num, cliente in clients:
            var = ctk.BooleanVar(value=True)
            self.client_vars.append((row_num, cliente, var))

            has_warning = row_num in row_warnings
            cpf_valid = validate_cpf(cliente.cpf) if cliente.cpf else False

            row_frame = ctk.CTkFrame(
                self.table_frame,
                fg_color=CARD_BG if not has_warning else "#fff8ee",
                border_color=CARD_BORDER if not has_warning else AVISO,
                border_width=1 if has_warning else 0,
                corner_radius=2,
            )
            row_frame.pack(fill="x", pady=1)

            cb = ctk.CTkCheckBox(
                row_frame, text="", variable=var, width=40,
                fg_color=DOMINANTE, hover_color=BTN_PRIMARY_HOVER,
                command=self._on_selection_changed,
            )
            cb.pack(side="left")

            ctk.CTkLabel(
                row_frame, text=cliente.nome_completo[:30],
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=TEXTO, width=200, anchor="w",
            ).pack(side="left", padx=5)

            cpf_color = TEXTO if cpf_valid else AVISO
            ctk.CTkLabel(
                row_frame, text=cliente.cpf,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=cpf_color, width=120, anchor="w",
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row_frame, text=cliente.parte_contraria[:25] if cliente.parte_contraria else "",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=TEXTO, width=200, anchor="w",
            ).pack(side="left", padx=5)

            status_parts = []
            if has_warning:
                status_parts.append("⚠ Campos")
            if not cpf_valid and cliente.cpf:
                status_parts.append("CPF inválido")
            status_text = " | ".join(status_parts) if status_parts else "✔"
            status_color = AVISO if status_parts else STATUS_OK

            ctk.CTkLabel(
                row_frame, text=status_text,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=status_color, width=100, anchor="w",
            ).pack(side="left", padx=5)

        self._on_selection_changed()

    def _select_all(self):
        for _, _, var in self.client_vars:
            var.set(True)
        self._on_selection_changed()

    def _deselect_all(self):
        for _, _, var in self.client_vars:
            var.set(False)
        self._on_selection_changed()

    def _on_selection_changed(self):
        if self.on_data_changed:
            self.on_data_changed()

    def get_selected_clients(self):
        """Return list of selected Cliente objects."""
        return [cliente for _, cliente, var in self.client_vars if var.get()]

    def has_data(self) -> bool:
        """Return True if any client is selected."""
        return any(var.get() for _, _, var in self.client_vars)
