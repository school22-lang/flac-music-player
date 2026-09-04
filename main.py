#!/usr/bin/env python3
"""Main entry point for the FLAC Music Player application."""

import tkinter as tk
from ui import FlacPlayerGUI


def main():
    """
    Launch the FLAC Music Player GUI.
    """
    root = tk.Tk()
    app = FlacPlayerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
