"""Template selection section — direct file selection of .docx templates."""

import os
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_title, create_body_label, create_aux_label,
    create_primary_button, create_secondary_button, create_card,
)
from app.core.template_loader import (
    TEMPLATE_FILES, load_template, TemplateInfo,
)

DOC_TYPE_LABELS = {
    "procuracao": "Procuração",
    "declaracao": "Declaração de Hipossuficiência",
    "contrato": "Contrato de Prestação de Serviços",
}

# Reverse map: filename → doc_type
_FILENAME_TO_DOCTYPE = {v: k for k, v in TEMPLATE_FILES.items()}


class SectionTemplates(ctk.CTkFrame):
    """Section for selecting template files directly."""

    def __init__(self, parent, on_templates_changed=None):
        super().__init__(parent, fg_color="transparent")
        self.on_templates_changed = on_templates_changed
        self.templates: dict[str, TemplateInfo] = {}

        self._build_ui()

    def _build_ui(self):
        card = create_card(self)
        card.pack(fill="x", padx=0, pady=0)

        # Header row with title + button
        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=16, pady=(12, 6))

        title = create_section_title(header_row, "Templates")
        title.pack(side="left")

        self.select_btn = create_primary_button(
            header_row, "Selecionar arquivos",
            command=self._select_files, width=160,
        )
        self.select_btn.pack(side="right")

        # Status line
        self.status_label = create_body_label(card, "Nenhum template selecionado")
        self.status_label.configure(text_color=AUX_TEXT_COLOR)
        self.status_label.pack(fill="x", padx=16)

        # Per-template status labels
        self.template_statuses = {}
        for doc_type in ["procuracao", "declaracao", "contrato"]:
            lbl = ctk.CTkLabel(
                card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=AUX_TEXT_COLOR, anchor="w",
            )
            self.template_statuses[doc_type] = lbl

        # Warning label (hidden by default)
        self.warning_label = ctk.CTkLabel(
            card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=STATUS_WARN, anchor="w",
        )

        # Bottom padding
        self._card_pad = ctk.CTkFrame(card, fg_color="transparent", height=8)
        self._card_pad.pack(fill="x")

    def _select_files(self):
        """Open file dialog to select template .docx files."""
        filepaths = filedialog.askopenfilenames(
            title="Selecionar arquivos de template (.docx)",
            filetypes=[("Word Document", "*.docx")],
        )
        if not filepaths:
            return

        recognized = {}
        for filepath in filepaths:
            basename = os.path.basename(filepath)
            doc_type = _FILENAME_TO_DOCTYPE.get(basename)
            if doc_type:
                info = load_template(filepath, doc_type)
                recognized[doc_type] = info

        # Merge with existing (overwrite recognized ones)
        self.templates.update(recognized)
        self._update_display()

        if self.on_templates_changed:
            self.on_templates_changed()

    def _update_display(self):
        """Update status labels based on loaded templates."""
        loaded_count = sum(1 for t in self.templates.values() if t.loaded)
        total = len(TEMPLATE_FILES)

        # Hide all per-template labels first
        for lbl in self.template_statuses.values():
            lbl.pack_forget()
        self.warning_label.pack_forget()

        if loaded_count == 0:
            self.status_label.configure(
                text="Nenhum template selecionado",
                text_color=AUX_TEXT_COLOR,
            )
            return

        if loaded_count == total:
            self.status_label.configure(
                text=f"✔ {loaded_count}/{total} templates carregados",
                text_color=STATUS_OK,
            )
        else:
            self.status_label.configure(
                text=f"⚠ {loaded_count}/{total} templates carregados",
                text_color=STATUS_WARN,
            )

        # Show per-template status
        for doc_type in ["procuracao", "declaracao", "contrato"]:
            lbl = self.template_statuses[doc_type]
            label_name = DOC_TYPE_LABELS[doc_type]
            info = self.templates.get(doc_type)
            if info and info.loaded:
                fname = os.path.basename(info.path)
                lbl.configure(
                    text=f"  ✔ {label_name}: {fname}",
                    text_color=STATUS_OK,
                )
            else:
                lbl.configure(
                    text=f"  ✕ {label_name}: não selecionado",
                    text_color=AVISO,
                )
            lbl.pack(fill="x", padx=16, after=self.status_label)

        # Show warnings for missing placeholders
        warnings = []
        for doc_type, info in self.templates.items():
            if info.missing_placeholders:
                label_name = DOC_TYPE_LABELS[doc_type]
                warnings.append(
                    f"{label_name}: placeholders ausentes: {', '.join(info.missing_placeholders)}"
                )
            if info.error:
                label_name = DOC_TYPE_LABELS[doc_type]
                warnings.append(f"{label_name}: {info.error}")

        if warnings:
            self.warning_label.configure(text="⚠ " + " | ".join(warnings))
            self.warning_label.pack(fill="x", padx=16, pady=(2, 0))
