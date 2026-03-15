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


def create_card(parent, **kwargs) -> ctk.CTkFrame:
    """Create a white card with border."""
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD_BG,
        border_color=CARD_BORDER,
        border_width=1,
        corner_radius=CARD_RADIUS,
        **kwargs,
    )
    return card


def create_centered_container(parent) -> ctk.CTkFrame:
    """Create a centered container with max width."""
    outer = ctk.CTkFrame(parent, fg_color="transparent")
    outer.pack(fill="both", expand=True)

    container = ctk.CTkFrame(outer, fg_color="transparent", width=MAX_CONTENT_WIDTH)
    container.pack(expand=True, fill="both", padx=max(10, 0))

    return container


def create_primary_button(parent, text, command=None, **kwargs) -> ctk.CTkButton:
    """Create a primary action button."""
    font = kwargs.pop("font", (FONT_FAMILY, FONT_SIZE_NORMAL))
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=BTN_PRIMARY_BG,
        hover_color=BTN_PRIMARY_HOVER,
        text_color=BTN_PRIMARY_FG,
        font=font,
        corner_radius=6,
        **kwargs,
    )
    return btn


def create_secondary_button(parent, text, command=None, **kwargs) -> ctk.CTkButton:
    """Create a secondary (outline) button."""
    font = kwargs.pop("font", (FONT_FAMILY, FONT_SIZE_NORMAL))
    btn = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        fg_color=BTN_SECONDARY_BG,
        hover_color=BTN_SECONDARY_HOVER,
        text_color=BTN_SECONDARY_FG,
        border_color=BTN_SECONDARY_BORDER,
        border_width=1,
        font=font,
        corner_radius=6,
        **kwargs,
    )
    return btn


def create_section_title(parent, text) -> ctk.CTkLabel:
    """Create a section title: small, uppercase, letter-spaced, DOMINANTE color."""
    label = ctk.CTkLabel(
        parent,
        text=text.upper(),
        font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
        text_color=SECTION_TITLE_COLOR,
        anchor="w",
    )
    return label


# Keep old name as alias for compatibility
create_section_label = create_section_title


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


def create_field_label(parent, text) -> ctk.CTkLabel:
    """Create a field label: small font, NEUTRO color."""
    label = ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT_FAMILY, FONT_SIZE_FIELD_LABEL),
        text_color=FIELD_LABEL_COLOR,
        anchor="w",
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
        corner_radius=ENTRY_RADIUS,
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
