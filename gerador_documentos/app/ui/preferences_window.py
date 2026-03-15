"""Preferences window for configuring template and output folders."""

import os
from tkinter import filedialog

import customtkinter as ctk

from app.ui.styles import *
from app.ui.components import (
    create_section_title, create_body_label, create_primary_button,
    create_secondary_button, create_entry, create_field_label, create_card,
)
from app.core.config_manager import load_config, save_config


class PreferencesWindow(ctk.CTkToplevel):
    """Preferences/settings window."""

    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.on_save = on_save
        self.title("Preferências — Ricardo Passos Advocacia")
        self.geometry("620x380")
        self.configure(fg_color=FUNDO)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Load config and store each value INDEPENDENTLY
        config = load_config()
        self._templates_folder_value = config.get("templates_folder", "")
        self._output_folder_value = config.get("output_folder", "")

        self._build_ui()

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 620) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 380) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        title = create_section_title(self, "Preferências")
        title.pack(fill="x", padx=24, pady=(20, 12))

        card = create_card(self)
        card.pack(fill="x", padx=24, pady=(0, 16))

        # --- Templates folder ---
        tf_label = create_field_label(card, "Pasta de templates padrão")
        tf_label.pack(fill="x", padx=16, pady=(16, 2))

        tf_row = ctk.CTkFrame(card, fg_color="transparent")
        tf_row.pack(fill="x", padx=16, pady=(0, 4))

        self.tf_entry = create_entry(tf_row, placeholder="Selecione a pasta dos templates")
        self.tf_entry.pack(side="left", fill="x", expand=True)
        if self._templates_folder_value:
            self.tf_entry.insert(0, self._templates_folder_value)

        tf_browse = create_secondary_button(
            tf_row, "Procurar...", command=self._browse_templates, width=100,
        )
        tf_browse.pack(side="left", padx=(5, 0))

        tf_test = create_secondary_button(
            tf_row, "Testar", width=60,
            command=self._test_templates_folder,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        )
        tf_test.pack(side="left", padx=(5, 0))

        self.tf_status = ctk.CTkLabel(
            card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=AUX_TEXT_COLOR, anchor="w",
        )
        self.tf_status.pack(fill="x", padx=16, pady=(0, 12))

        # --- Output folder (completely independent) ---
        of_label = create_field_label(card, "Pasta de saída")
        of_label.pack(fill="x", padx=16, pady=(0, 2))

        of_row = ctk.CTkFrame(card, fg_color="transparent")
        of_row.pack(fill="x", padx=16, pady=(0, 4))

        self.of_entry = create_entry(of_row, placeholder="Selecione a pasta de saída")
        self.of_entry.pack(side="left", fill="x", expand=True)
        if self._output_folder_value:
            self.of_entry.insert(0, self._output_folder_value)

        of_browse = create_secondary_button(
            of_row, "Procurar...", command=self._browse_output, width=100,
        )
        of_browse.pack(side="left", padx=(5, 0))

        of_test = create_secondary_button(
            of_row, "Testar", width=60,
            command=self._test_output_folder,
            font=(FONT_FAMILY, FONT_SIZE_SMALL),
        )
        of_test.pack(side="left", padx=(5, 0))

        self.of_status = ctk.CTkLabel(
            card, text="", font=(FONT_FAMILY, FONT_SIZE_SMALL),
            text_color=AUX_TEXT_COLOR, anchor="w",
        )
        self.of_status.pack(fill="x", padx=16, pady=(0, 16))

        # --- Buttons ---
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=24, pady=(0, 20))

        save_btn = create_primary_button(btn_row, "Salvar", command=self._save, width=120)
        save_btn.pack(side="right")

        cancel_btn = create_secondary_button(
            btn_row, "Cancelar", command=self.destroy, width=120,
        )
        cancel_btn.pack(side="right", padx=(0, 10))

    def _browse_templates(self):
        """Browse for templates folder — writes ONLY to tf_entry."""
        folder = filedialog.askdirectory(title="Selecionar pasta de templates")
        if folder:
            self.tf_entry.delete(0, "end")
            self.tf_entry.insert(0, folder)

    def _browse_output(self):
        """Browse for output folder — writes ONLY to of_entry."""
        folder = filedialog.askdirectory(title="Selecionar pasta de saída")
        if folder:
            self.of_entry.delete(0, "end")
            self.of_entry.insert(0, folder)

    def _test_templates_folder(self):
        """Test templates folder independently."""
        path = self.tf_entry.get().strip()
        if not path:
            self.tf_status.configure(text="⚠ Nenhum caminho informado", text_color=AVISO)
            return
        if not os.path.isdir(path):
            self.tf_status.configure(text="✕ Pasta não encontrada ou inacessível", text_color=ERRO)
            return

        from app.core.template_loader import check_templates_folder
        status = check_templates_folder(path)
        missing = [k for k, v in status.items() if not v]
        if missing:
            labels = {"procuracao": "Procuração", "declaracao": "Declaração", "contrato": "Contrato"}
            names = [labels.get(m, m) for m in missing]
            self.tf_status.configure(
                text=f"⚠ Pasta acessível, mas faltam: {', '.join(names)}",
                text_color=AVISO,
            )
        else:
            self.tf_status.configure(
                text="✔ Pasta acessível, todos os templates encontrados",
                text_color=STATUS_OK,
            )

    def _test_output_folder(self):
        """Test output folder independently."""
        path = self.of_entry.get().strip()
        if not path:
            self.of_status.configure(text="⚠ Nenhum caminho informado", text_color=AVISO)
            return
        if not os.path.isdir(path):
            self.of_status.configure(text="✕ Pasta não encontrada ou inacessível", text_color=ERRO)
            return

        try:
            test_file = os.path.join(path, ".gerador_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            self.of_status.configure(
                text="✔ Pasta acessível e com permissão de escrita",
                text_color=STATUS_OK,
            )
        except OSError:
            self.of_status.configure(text="✕ Pasta sem permissão de escrita", text_color=ERRO)

    def _save(self):
        """Save both folder values INDEPENDENTLY to config.json."""
        # Read each entry independently
        templates_folder = self.tf_entry.get().strip()
        output_folder = self.of_entry.get().strip()

        # Build config with both keys explicitly
        config = {
            "templates_folder": templates_folder,
            "output_folder": output_folder,
        }
        save_config(config)

        if self.on_save:
            self.on_save(config)

        self.destroy()
