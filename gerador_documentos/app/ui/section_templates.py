"""Template status section with optional per-session override."""

import os
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_label, create_body_label, create_aux_label,
    create_secondary_button,
)
from app.core.template_loader import (
    TEMPLATE_FILES, load_template, load_default_templates, TemplateInfo,
)

DOC_TYPE_LABELS = {
    "procuracao": "Procuração",
    "declaracao": "Declaração",
    "contrato": "Contrato",
}


class SectionTemplates(ctk.CTkFrame):
    """Section showing template status and per-session override controls."""

    def __init__(self, parent, on_templates_changed=None):
        super().__init__(parent, fg_color=FUNDO)
        self.on_templates_changed = on_templates_changed
        self.templates: dict[str, TemplateInfo] = {}
        self.custom_paths: dict[str, str] = {}
        self._expanded = False

        self._build_ui()

    def _build_ui(self):
        # Section title
        title = create_section_label(self, "Templates")
        title.pack(fill="x", padx=10, pady=(10, 5))

        # Status line
        self.status_label = create_body_label(self, "")
        self.status_label.pack(fill="x", padx=10)

        # Warning label (hidden by default)
        self.warning_label = ctk.CTkLabel(
            self, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=STATUS_WARN, anchor="w",
        )

        # Expandable section
        self.expand_btn = ctk.CTkButton(
            self, text="Usar modelo diferente nesta sessão ▾",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            fg_color="transparent", hover_color="#ddd9d0",
            text_color=ACENTO, anchor="w",
            command=self._toggle_expand,
        )
        self.expand_btn.pack(fill="x", padx=10, pady=(2, 0))

        # Expandable content
        self.expand_frame = ctk.CTkFrame(self, fg_color=FUNDO)
        self.selectors = {}
        for doc_type in ["procuracao", "declaracao", "contrato"]:
            row = ctk.CTkFrame(self.expand_frame, fg_color=FUNDO)
            row.pack(fill="x", padx=10, pady=2)

            label = ctk.CTkLabel(
                row, text=f"{DOC_TYPE_LABELS[doc_type]}:",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=BODY_TEXT_COLOR, width=100, anchor="w",
            )
            label.pack(side="left")

            status = ctk.CTkLabel(
                row, text="Usando padrão",
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
                text_color=AUX_TEXT_COLOR, anchor="w",
            )
            status.pack(side="left", padx=(5, 10), expand=True, fill="x")

            btn = create_secondary_button(
                row, "Selecionar...",
                command=lambda dt=doc_type: self._select_custom(dt),
                width=100, height=28,
                font=(FONT_FAMILY, FONT_SIZE_SMALL),
            )
            btn.pack(side="right")

            reset_btn = ctk.CTkButton(
                row, text="✕", width=28, height=28,
                fg_color="transparent", hover_color="#ddd9d0",
                text_color=NEUTRO,
                command=lambda dt=doc_type: self._reset_custom(dt),
            )
            reset_btn.pack(side="right", padx=(0, 5))

            self.selectors[doc_type] = {"status": status, "btn": btn, "reset": reset_btn}

    def _toggle_expand(self):
        self._expanded = not self._expanded
        if self._expanded:
            self.expand_frame.pack(fill="x", padx=0, pady=(0, 5))
            self.expand_btn.configure(text="Usar modelo diferente nesta sessão ▴")
        else:
            self.expand_frame.pack_forget()
            self.expand_btn.configure(text="Usar modelo diferente nesta sessão ▾")

    def _select_custom(self, doc_type: str):
        filepath = filedialog.askopenfilename(
            title=f"Selecionar template para {DOC_TYPE_LABELS[doc_type]}",
            filetypes=[("Word Document", "*.docx")],
        )
        if filepath:
            info = load_template(filepath, doc_type, is_custom=True)
            self.templates[doc_type] = info
            self.custom_paths[doc_type] = filepath
            self._update_selector_status(doc_type)
            self._update_status_line()
            if self.on_templates_changed:
                self.on_templates_changed()

    def _reset_custom(self, doc_type: str):
        if doc_type in self.custom_paths:
            del self.custom_paths[doc_type]
            # Reload from default
            from app.core.config_manager import get_templates_folder
            folder = get_templates_folder()
            if folder:
                filepath = os.path.join(folder, TEMPLATE_FILES[doc_type])
                self.templates[doc_type] = load_template(filepath, doc_type)
            else:
                self.templates[doc_type] = TemplateInfo(doc_type=doc_type, path="")
            self._update_selector_status(doc_type)
            self._update_status_line()
            if self.on_templates_changed:
                self.on_templates_changed()

    def _update_selector_status(self, doc_type: str):
        sel = self.selectors[doc_type]
        info = self.templates.get(doc_type)
        if info and info.is_custom:
            name = os.path.basename(info.path)
            sel["status"].configure(text=f"Personalizado: {name}", text_color=ACENTO)
        else:
            sel["status"].configure(text="Usando padrão", text_color=AUX_TEXT_COLOR)

    def load_defaults(self, folder: str):
        """Load default templates from the given folder."""
        if folder and os.path.isdir(folder):
            defaults = load_default_templates(folder)
            for doc_type, info in defaults.items():
                if doc_type not in self.custom_paths:
                    self.templates[doc_type] = info
        else:
            for doc_type in TEMPLATE_FILES:
                if doc_type not in self.custom_paths:
                    self.templates[doc_type] = TemplateInfo(doc_type=doc_type, path="")

        self._update_status_line()
        for doc_type in self.selectors:
            self._update_selector_status(doc_type)

        if self.on_templates_changed:
            self.on_templates_changed()

    def _update_status_line(self):
        all_loaded = all(
            t.loaded for t in self.templates.values()
        ) if self.templates else False

        any_custom = bool(self.custom_paths)

        if not self.templates or not any(t.loaded for t in self.templates.values()):
            # No templates loaded
            self.status_label.configure(
                text="⚠ Templates não carregados — configure a pasta em Preferências",
                text_color=STATUS_WARN,
            )
            self.warning_label.pack_forget()
            return

        if all_loaded and not any_custom:
            self.status_label.configure(
                text="✔ Usando modelos padrão",
                text_color=STATUS_OK,
            )
        else:
            parts = []
            for doc_type in ["procuracao", "declaracao", "contrato"]:
                info = self.templates.get(doc_type)
                label = DOC_TYPE_LABELS[doc_type]
                if info and info.is_custom:
                    parts.append(f"{label}: modelo personalizado")
                elif info and info.loaded:
                    parts.append(f"{label}: padrão")
                else:
                    parts.append(f"{label}: não carregado")
            self.status_label.configure(
                text="✔ " + " | ".join(parts),
                text_color=STATUS_OK,
            )

        # Check for missing placeholders warnings
        warnings = []
        for doc_type, info in self.templates.items():
            if info.missing_placeholders:
                label = DOC_TYPE_LABELS[doc_type]
                warnings.append(
                    f"{label}: placeholders ausentes: {', '.join(info.missing_placeholders)}"
                )
            if info.error:
                label = DOC_TYPE_LABELS[doc_type]
                warnings.append(f"{label}: {info.error}")

        if warnings:
            self.warning_label.configure(text="⚠ " + " | ".join(warnings))
            self.warning_label.pack(fill="x", padx=10, after=self.status_label)
        else:
            self.warning_label.pack_forget()
