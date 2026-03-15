"""Main application window."""

import os
import subprocess
import sys
import threading
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_header, create_primary_button, create_secondary_button,
    create_section_title, create_body_label, create_aux_label,
    create_card,
)
from app.ui.section_templates import SectionTemplates
from app.ui.tab_excel import TabExcel
from app.ui.tab_manual import TabManual
from app.ui.preferences_window import PreferencesWindow
from app.core.config_manager import load_config, get_templates_folder, get_output_folder
from app.core.placeholder_engine import generate_documents, data_extenso, DOC_TYPE_SUFFIXES
from app.core.validators import validate_cpf, normalize_cep


DOC_LABELS = {
    "procuracao": "Procuração",
    "declaracao": "Declaração de Hipossuficiência",
    "contrato": "Contrato",
}


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("Gerador de Documentos — Ricardo Passos Advocacia")
        self.geometry("900x750")
        self.configure(fg_color=FUNDO)
        self.minsize(800, 650)

        ctk.set_appearance_mode("light")

        self.config = load_config()
        self._active_tab = "excel"

        self._build_ui()
        self._load_initial_state()

    def _build_ui(self):
        # Header
        header = create_header(self)

        # Gear icon for preferences
        gear_btn = ctk.CTkButton(
            header, text="⚙", width=40, height=40,
            fg_color="transparent", hover_color=BTN_PRIMARY_HOVER,
            text_color=HEADER_FG,
            font=(FONT_FAMILY, 20),
            command=self._open_preferences,
        )
        gear_btn.pack(side="right", padx=15)

        # Scrollable main content
        main_scroll = ctk.CTkScrollableFrame(self, fg_color=FUNDO)
        main_scroll.pack(fill="both", expand=True)

        # Centered container with max width
        content = ctk.CTkFrame(main_scroll, fg_color="transparent")
        content.pack(fill="x", expand=True, padx=max((900 - MAX_CONTENT_WIDTH) // 2, 16), pady=12)

        # --- Template section ---
        self.section_templates = SectionTemplates(
            content, on_templates_changed=self._on_templates_changed,
        )
        self.section_templates.pack(fill="x", pady=(0, 8))

        # --- Data source tabs ---
        tab_card = create_card(content)
        tab_card.pack(fill="both", expand=True, pady=(0, 8))

        tab_header = ctk.CTkFrame(tab_card, fg_color="transparent")
        tab_header.pack(fill="x")

        self.tab_excel_btn = ctk.CTkButton(
            tab_header, text="Excel / Forms",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            fg_color=TAB_ACTIVE_BG, text_color=TAB_ACTIVE_FG,
            hover_color=BTN_PRIMARY_HOVER, corner_radius=0, height=36,
            command=lambda: self._switch_tab("excel"),
        )
        self.tab_excel_btn.pack(side="left")

        self.tab_manual_btn = ctk.CTkButton(
            tab_header, text="Dados Manuais",
            font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            fg_color=TAB_INACTIVE_BG, text_color=TAB_INACTIVE_FG,
            hover_color=BTN_SECONDARY_HOVER, corner_radius=0, height=36,
            command=lambda: self._switch_tab("manual"),
        )
        self.tab_manual_btn.pack(side="left")

        self.tab_content = ctk.CTkFrame(tab_card, fg_color="transparent")
        self.tab_content.pack(fill="both", expand=True, padx=0, pady=0)

        self.tab_excel = TabExcel(self.tab_content, on_data_changed=self._update_generate_button)
        self.tab_manual = TabManual(self.tab_content, on_data_changed=self._update_generate_button)

        self.tab_excel.pack(fill="both", expand=True)

        # --- Bottom section: document selection + generate ---
        bottom_card = create_card(content)
        bottom_card.pack(fill="x", pady=(0, 8))

        doc_row = ctk.CTkFrame(bottom_card, fg_color="transparent")
        doc_row.pack(fill="x", padx=16, pady=(12, 8))

        doc_label = create_section_title(doc_row, "Documentos a gerar")
        doc_label.pack(fill="x", pady=(0, 6))

        checks_row = ctk.CTkFrame(bottom_card, fg_color="transparent")
        checks_row.pack(fill="x", padx=16)

        self.doc_vars = {}
        self.doc_checks = {}
        for doc_type, label in DOC_LABELS.items():
            var = ctk.BooleanVar(value=True)
            self.doc_vars[doc_type] = var
            cb = ctk.CTkCheckBox(
                checks_row, text=label, variable=var,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                text_color=BODY_TEXT_COLOR,
                fg_color=DOMINANTE, hover_color=BTN_PRIMARY_HOVER,
                command=self._update_generate_button,
            )
            cb.pack(side="left", padx=(0, 15))
            self.doc_checks[doc_type] = cb

        # Output folder warning
        self.output_warning = ctk.CTkLabel(
            bottom_card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=AVISO, anchor="w",
        )

        # Generate button row
        gen_row = ctk.CTkFrame(bottom_card, fg_color="transparent")
        gen_row.pack(fill="x", padx=16, pady=(12, 12))

        self.generate_btn = create_primary_button(
            gen_row, "Gerar Documentos", command=self._generate, width=200, height=40,
        )
        self.generate_btn.pack(side="left")

        self.generate_tooltip = create_aux_label(gen_row, "")
        self.generate_tooltip.pack(side="left", padx=10)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            bottom_card, fg_color=ENTRY_BG, progress_color=STATUS_OK, height=8,
        )
        self.progress.set(0)

        # Result label
        self.result_label = ctk.CTkLabel(
            bottom_card, text="", font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            text_color=STATUS_OK, anchor="w", wraplength=680,
        )

        self.open_folder_btn = create_secondary_button(
            bottom_card, "Abrir pasta", command=self._open_output_folder, width=120,
        )

    def _load_initial_state(self):
        templates_folder = get_templates_folder(self.config)
        self.section_templates.load_defaults(templates_folder)
        self._update_generate_button()

    def _switch_tab(self, tab_name: str):
        self._active_tab = tab_name
        if tab_name == "excel":
            self.tab_manual.pack_forget()
            self.tab_excel.pack(fill="both", expand=True)
            self.tab_excel_btn.configure(
                fg_color=TAB_ACTIVE_BG, text_color=TAB_ACTIVE_FG,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            )
            self.tab_manual_btn.configure(
                fg_color=TAB_INACTIVE_BG, text_color=TAB_INACTIVE_FG,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            )
        else:
            self.tab_excel.pack_forget()
            self.tab_manual.pack(fill="both", expand=True)
            self.tab_manual_btn.configure(
                fg_color=TAB_ACTIVE_BG, text_color=TAB_ACTIVE_FG,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"),
            )
            self.tab_excel_btn.configure(
                fg_color=TAB_INACTIVE_BG, text_color=TAB_INACTIVE_FG,
                font=(FONT_FAMILY, FONT_SIZE_NORMAL),
            )
        self._update_generate_button()

    def _on_templates_changed(self):
        """Update document checkboxes based on loaded templates."""
        for doc_type, cb in self.doc_checks.items():
            template = self.section_templates.templates.get(doc_type)
            if template and template.loaded:
                cb.configure(state="normal")
            else:
                cb.configure(state="disabled")
                self.doc_vars[doc_type].set(False)
        self._update_generate_button()

    def _update_generate_button(self):
        """Update the generate button state and tooltip."""
        reasons = []

        any_doc = any(v.get() for v in self.doc_vars.values())
        if not any_doc:
            reasons.append("Nenhum documento selecionado")

        if self._active_tab == "excel":
            if not self.tab_excel.has_data():
                reasons.append("Nenhum cliente selecionado")
        else:
            if not self.tab_manual.has_data():
                reasons.append("Preencha os dados do cliente")

        output_folder = get_output_folder(self.config)
        if not output_folder or not os.path.isdir(output_folder):
            reasons.append("Pasta de saída não configurada")
            self.output_warning.configure(
                text="⚠ Pasta de saída não configurada — defina em Preferências"
            )
            self.output_warning.pack(fill="x", padx=16, pady=(4, 0))
        else:
            self.output_warning.pack_forget()

        if reasons:
            self.generate_btn.configure(state="disabled")
            self.generate_tooltip.configure(text=" | ".join(reasons))
        else:
            self.generate_btn.configure(state="normal")
            self.generate_tooltip.configure(text="")

    def _open_preferences(self):
        PreferencesWindow(self, on_save=self._on_preferences_saved)

    def _on_preferences_saved(self, config: dict):
        self.config = config
        templates_folder = get_templates_folder(config)
        self.section_templates.load_defaults(templates_folder)
        self._update_generate_button()

    def _generate(self):
        """Generate documents for selected clients."""
        self.generate_btn.configure(state="disabled")
        self.result_label.pack_forget()
        self.open_folder_btn.pack_forget()
        self.progress.pack(fill="x", padx=16, pady=(5, 0))
        self.progress.set(0)

        output_folder = get_output_folder(self.config)
        templates = self.section_templates.templates
        doc_types = [dt for dt, var in self.doc_vars.items() if var.get()]

        if self._active_tab == "excel":
            clients = self.tab_excel.get_selected_clients()
        else:
            client = self.tab_manual.get_client()
            if client is None:
                self.generate_btn.configure(state="normal")
                self.progress.pack_forget()
                return
            clients = [client]

        if not clients:
            self.generate_btn.configure(state="normal")
            self.progress.pack_forget()
            return

        def do_generate():
            all_results = []
            existing_files = set()
            total = len(clients) * len(doc_types)
            done = 0

            for cliente in clients:
                data = cliente.to_placeholder_dict()
                data["DATA_EXTENSO"] = data_extenso()

                data["CPF"] = data.get("CPF", "")
                cep_raw = cliente.cep.strip()
                if cep_raw:
                    data["ENDERECO_COMPLETO"] = cliente.endereco_completo()
                    cep_norm = normalize_cep(cep_raw)
                    data["ENDERECO_COMPLETO"] = data["ENDERECO_COMPLETO"].replace(
                        f"CEP {cep_raw}", f"CEP {cep_norm}"
                    )

                results = generate_documents(
                    data, templates, doc_types, output_folder, existing_files,
                )
                all_results.append((cliente.nome_completo, results))
                done += len(doc_types)
                self.progress.set(done / total if total > 0 else 1)

            self.after(0, lambda: self._show_results(all_results, output_folder))

        thread = threading.Thread(target=do_generate, daemon=True)
        thread.start()

    def _show_results(self, all_results, output_folder):
        """Display generation results."""
        self.progress.pack_forget()
        self.generate_btn.configure(state="normal")

        success_count = 0
        fail_count = 0
        details = []

        for nome, results in all_results:
            for r in results:
                if r["success"]:
                    success_count += 1
                    details.append(f"✔ {os.path.basename(r['path'])}")
                else:
                    fail_count += 1
                    doc_label = DOC_LABELS.get(r["doc_type"], r["doc_type"])
                    details.append(f"✕ {nome} — {doc_label}: {r['error']}")

        if fail_count == 0:
            msg = f"✔ {success_count} documento(s) gerado(s) com sucesso!\n" + "\n".join(details)
            self.result_label.configure(text=msg, text_color=STATUS_OK)
        else:
            msg = (
                f"✔ {success_count} sucesso(s) | ✕ {fail_count} falha(s)\n"
                + "\n".join(details)
            )
            self.result_label.configure(text=msg, text_color=AVISO)

        self.result_label.pack(fill="x", padx=16, pady=(5, 0))
        self.open_folder_btn.pack(padx=16, pady=(5, 12), anchor="w")
        self._output_folder_for_open = output_folder

    def _open_output_folder(self):
        folder = getattr(self, "_output_folder_for_open", "")
        if folder and os.path.isdir(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
