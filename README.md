A simple Python desktop application for organizing ideas and tasks on a virtual sticky-note board.

Create notes, drag them around the wall, edit their text, and choose colors. Notes save automatically on your computer and return when you reopen the app.

## Features

- Create notes with multiline text.
- Drag notes around the board.
- Edit notes by double-clicking them.
- Delete notes with confirmation.
- Choose yellow, green, blue, or pink.
- Automatically save note text, colors, and positions.

## Getting Started

This version runs from Python source. **A standalone Windows executable is not included yet.**

You need Python 3 with Tkinter installed. No additional third-party Python packages are required.

1. Select **Code → Download ZIP** on this repository.
2. Extract the downloaded folder.
3. Open a terminal in the folder containing `sticky_wall.py`.
4. Run:

```bash
py sticky_wall.py
```

If your installation uses the `python` command instead:

```bash
python sticky_wall.py
```

## How to Use

| Action | Instructions |
| --- | --- |
| Create a note | Click **+ New note**, enter text, then click **Save note**. |
| Save from the editor | Click **Save note** or press **Ctrl+Enter**. |
| Move a note | Click and hold a note, then drag it. |
| Edit a note | Double-click it, or select it and click **Edit**. |
| Change its color | Select a note and click a color button. |
| Delete a note | Select it, click **Delete**, and confirm. |
| Cancel editing | Click **Cancel** or press **Esc**. |

Long notes show a shortened preview on the board. Open the editor to read or edit the full text.

## How the Code Works

The application uses Python’s standard library:

- **Tkinter** creates the window, buttons, editor, and canvas.
- **Dictionaries** store each note’s text, position, and color.
- **Functions** handle actions such as creating, editing, deleting, and saving.
- **Mouse events** track clicks and dragging.
- **JSON** stores notes between sessions.
- **pathlib** and **os** manage the save location.

Each note has a unique ID and a dictionary resembling this:

```python
{
    "text": "Practice Python",
    "x": 40,
    "y": 40,
    "color": "#FBE59A"
}
```

Most actions follow the same process:

1. Update the note’s dictionary.
2. Update its appearance on the canvas.
3. Save the updated data.

The application writes a temporary file before replacing the existing save. If a saved file cannot be read, it displays an error and disables saving to avoid overwriting that file.

## Where Notes Are Saved

On Windows, notes are stored at:

```text
%LOCALAPPDATA%\StickyWall\notes.json
```

Paste `%LOCALAPPDATA%\StickyWall` into File Explorer’s address bar to find the folder.

Notes stay on your computer. The application makes no network requests and does not upload notes to GitHub. The save file is readable JSON and is **not encrypted**.

Only open one instance of the app at a time. Multiple instances do not synchronize and could overwrite each other’s changes.

## How This Project Was Created

I developed this project as a beginner computer science student learning how to turn Python coursework into a desktop application.

I chose the app’s features and worked through development in stages, starting with draggable notes and then adding editing, deletion, colors, and saving.

**This project was built with substantial assistance from ChatGPT/Codex**, including generated code, explanations, debugging, and automated storage tests. My role included defining the requirements, running the application on Windows, and reporting problems during development.

For example, testing revealed that the editor’s Save button could be hidden below the text box. The layout was revised to reserve space for the buttons, and a Ctrl+Enter shortcut was added.

This is an ongoing learning project. I am working through the code to understand its functions, data structures, and event handling. It is not presented as entirely independently written software.

## Testing

Run the included storage tests with:

```bash
py -m unittest test_storage.py
```

The tests check:

- Saving and loading note data, including multiline and accented text.
- Saving an empty board after deleting notes.
- Rejecting invalid saved data without modifying the original file.

These tests cover file storage, not every graphical interaction. To check the interface, create a note, edit it, change its color, move it, and restart the app to confirm your changes remain.

## Current Limitations

- Requires Python to run; no packaged `.exe` yet.
- No search, linked notes, completion tracking, or reminders.
- No cloud synchronization.
- Deletion has a confirmation prompt but no undo.
- Intended for one running instance at a time.

The project is intentionally small so I can understand and explain its behavior before adding more features.
