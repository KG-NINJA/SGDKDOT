"""Utilities for applying a Mega Drive–inspired theme to the GUI."""


def apply_style(root):
    """Apply Mega Drive–inspired colors and fonts to a Tkinter root window.

    Parameters
    ----------
    root : tkinter.Misc
        The root window or widget to which the theme should be applied.
    """
    if root is None:
        return

    palette = {
        "background": "#000000",  # deep black
        "foreground": "#00AEEF",  # bright cyan
        "accent": "#E60012",      # classic red accent
    }
    default_font = ("Courier New", 10, "bold")

    root.configure(bg=palette["background"])
    root.option_add("*Foreground", palette["foreground"])
    root.option_add("*Background", palette["background"])
    root.option_add("*Font", default_font)

    try:
        from tkinter import ttk

        style = ttk.Style(root)
        style.theme_use("default")
        style.configure(
            ".",
            background=palette["background"],
            foreground=palette["foreground"],
            font=default_font,
        )
        style.configure(
            "TButton",
            background=palette["accent"],
            foreground=palette["foreground"],
            font=default_font,
        )
    except Exception:
        # ttk might not be available or a display may not be initialized.
        # Continue silently if styling cannot be fully applied.
        pass

