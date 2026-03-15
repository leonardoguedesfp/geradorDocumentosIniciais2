"""Reusable UI components."""

import customtkinter as ctk

from app.ui.styles import *


def create_header(parent) -> ctk.CTkFrame:
    """Create the fixed header with 'Ricardo Passos Advocacia'."""
    header = ctk.CTkFrame(parent, fg_color=HEADER_BG, corner_radius=0, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    label = ctk.CTkLabel(
        header,
        text="Ricardo Passos Advocacia",
        font=(FONT_FAMILY, FONT_SIZE_HEADER, "bold"),
        text_color=HEADER_FG,
    )
    label.pack(side="left", padx=20, pady=10)

    return header


def create_primary_button(parent, text, command=None, **kwargs) -> ctk.CTkButton:
    """Create a primary action button."""
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=BTN_PRIMARY_BG,
        hover_color=BTN_PRIMARY_HOVER,
        text_color=BTN_PRIMARY_FG,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        corner_radius=6,
        **kwargs,
    )
    return btn


def create_secondary_button(parent, text, command=None, **kwargs) -> ctk.CTkButton:
    """Create a secondary action button."""
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=BTN_SECONDARY_BG,
        hover_color=BTN_SECONDARY_HOVER,
        text_color=BTN_SECONDARY_FG,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        corner_radius=6,
        **kwargs,
    )
    return btn


def create_section_label(parent, text) -> ctk.CTkLabel:
    """Create a section title label."""
    label = ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        text_color=SECTION_TITLE_COLOR,
        anchor="w",
    )
    return label


def create_body_label(parent, text, **kwargs) -> ctk.CTkLabel:
    """Create a body text label."""
    label = ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        text_color=BODY_TEXT_COLOR,
        anchor="w",
        **kwargs,
    )
    return label


def create_aux_label(parent, text, **kwargs) -> ctk.CTkLabel:
    """Create an auxiliary/helper text label."""
    label = ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT_FAMILY, FONT_SIZE_SMALL),
        text_color=AUX_TEXT_COLOR,
        anchor="w",
        **kwargs,
    )
    return label


def create_entry(parent, placeholder="", **kwargs) -> ctk.CTkEntry:
    """Create a styled text entry."""
    entry = ctk.CTkEntry(
        parent,
        fg_color=ENTRY_BG,
        border_color=ENTRY_BORDER,
        text_color=BODY_TEXT_COLOR,
        placeholder_text_color=AUX_TEXT_COLOR,
        placeholder_text=placeholder,
        font=(FONT_FAMILY, FONT_SIZE_NORMAL),
        corner_radius=4,
        border_width=1,
        **kwargs,
    )
    return entry


def set_entry_error(entry: ctk.CTkEntry, has_error: bool = True) -> None:
    """Set or clear error styling on an entry."""
    if has_error:
        entry.configure(border_color=ENTRY_ERROR_BORDER, border_width=2)
    else:
        entry.configure(border_color=ENTRY_BORDER, border_width=1)
