"""Preferences window for configuring template and output folders."""

import os
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_label, create_body_label, create_primary_button,
    create_secondary_button, create_entry,
)
from app.core.config_manager import load_config, save_config


class PreferencesWindow(ctk.CTkToplevel):
    """Preferences/settings window."""

    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.on_save = on_save
        self.title("Preferências — Ricardo Passos Advocacia")
        self.geometry("600x350")
        self.configure(fg_color=FUNDO)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.config = load_config()
        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 600) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 350) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        title = create_section_label(self, "Preferências")
        title.pack(fill="x", padx=20, pady=(20, 15))

        # Templates folder
        tf_label = create_body_label(self, "Pasta de templates padrão:")
        tf_label.pack(fill="x", padx=20, pady=(0, 2))

        tf_row = ctk.CTkFrame(self, fg_color=FUNDO)
        tf_row.pack(fill="x", padx=20, pady=(0, 5))

        self.tf_entry = create_entry(tf_row, placeholder="Selecione a pasta dos templates")
        self.tf_entry.pack(side="left", fill="x", expand=True)
        tf_val = self.config.get("templates_folder", "")
        if tf_val:
            self.tf_entry.insert(0, tf_val)

        tf_browse = create_secondary_button(
            tf_row, "Procurar...", command=self._browse_templates, width=100,
        )
        tf_browse.pack(side="left", padx=(5, 0))

        tf_test = ctk.CTkButton(
            tf_row, text="Testar", width=60,
            fg_color=ACENTO, hover_color=DOMINANTE, text_color="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            command=lambda: self._test_folder(self.tf_entry, "templates"),
        )
        tf_test.pack(side="left", padx=(5, 0))

        self.tf_status = ctk.CTkLabel(
            self, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=AUX_TEXT_COLOR, anchor="w",
        )
        self.tf_status.pack(fill="x", padx=20, pady=(0, 10))

        # Output folder
        of_label = create_body_label(self, "Pasta de saída:")
        of_label.pack(fill="x", padx=20, pady=(0, 2))

        of_row = ctk.CTkFrame(self, fg_color=FUNDO)
        of_row.pack(fill="x", padx=20, pady=(0, 5))

        self.of_entry = create_entry(of_row, placeholder="Selecione a pasta de saída")
        self.of_entry.pack(side="left", fill="x", expand=True)
        of_val = self.config.get("output_folder", "")
        if of_val:
            self.of_entry.insert(0, of_val)

        of_browse = create_secondary_button(
            of_row, "Procurar...", command=self._browse_output, width=100,
        )
        of_browse.pack(side="left", padx=(5, 0))

        of_test = ctk.CTkButton(
            of_row, text="Testar", width=60,
            fg_color=ACENTO, hover_color=DOMINANTE, text_color="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
            command=lambda: self._test_folder(self.of_entry, "output"),
        )
        of_test.pack(side="left", padx=(5, 0))

        self.of_status = ctk.CTkLabel(
            self, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=AUX_TEXT_COLOR, anchor="w",
        )
        self.of_status.pack(fill="x", padx=20, pady=(0, 15))

        # Buttons
        btn_row = ctk.CTkFrame(self, fg_color=FUNDO)
        btn_row.pack(fill="x", padx=20, pady=(10, 20))

        save_btn = create_primary_button(btn_row, "Salvar", command=self._save, width=120)
        save_btn.pack(side="right")

        cancel_btn = create_secondary_button(
            btn_row, "Cancelar", command=self.destroy, width=120,
        )
        cancel_btn.pack(side="right", padx=(0, 10))

    def _browse_templates(self):
        folder = filedialog.askdirectory(title="Selecionar pasta de templates")
        if folder:
            self.tf_entry.delete(0, "end")
            self.tf_entry.insert(0, folder)

    def _browse_output(self):
        folder = filedialog.askdirectory(title="Selecionar pasta de saída")
        if folder:
            self.of_entry.delete(0, "end")
            self.of_entry.insert(0, folder)

    def _test_folder(self, entry, folder_type: str):
        path = entry.get().strip()
        status_label = self.tf_status if folder_type == "templates" else self.of_status

        if not path:
            status_label.configure(text="⚠ Nenhum caminho informado", text_color=AVISO)
            return

        if not os.path.isdir(path):
            status_label.configure(text="✕ Pasta não encontrada ou inacessível", text_color=ERRO)
            return

        if folder_type == "templates":
            from app.core.template_loader import check_templates_folder
            status = check_templates_folder(path)
            missing = [k for k, v in status.items() if not v]
            if missing:
                labels = {"procuracao": "Procuração", "declaracao": "Declaração", "contrato": "Contrato"}
                names = [labels.get(m, m) for m in missing]
                status_label.configure(
                    text=f"⚠ Pasta acessível, mas faltam: {', '.join(names)}",
                    text_color=AVISO,
                )
            else:
                status_label.configure(text="✔ Pasta acessível, todos os templates encontrados", text_color=STATUS_OK)
        else:
            # Test write access
            try:
                test_file = os.path.join(path, ".gerador_test")
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
                status_label.configure(text="✔ Pasta acessível e com permissão de escrita", text_color=STATUS_OK)
            except OSError:
                status_label.configure(text="✕ Pasta sem permissão de escrita", text_color=ERRO)

    def _save(self):
        self.config["templates_folder"] = self.tf_entry.get().strip()
        self.config["output_folder"] = self.of_entry.get().strip()
        save_config(self.config)

        if self.on_save:
            self.on_save(self.config)

        self.destroy()
