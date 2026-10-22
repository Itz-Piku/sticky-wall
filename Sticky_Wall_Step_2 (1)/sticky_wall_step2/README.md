# Sticky Wall — Step 2

A small Python desktop app: create, drag, edit, delete, choose colors, and automatically save sticky notes. This is a deliberately small learning project. It uses Tkinter and JSON from Python's standard library, without third-party runtime packages.

## Run on Windows

Extract the ZIP, open this folder in VS Code, open a terminal, and run:

```text
py sticky_wall.py
```

Use `python sticky_wall.py` if that is the command your Python installation provides. This remains a source-code version that requires Python; it is not an executable or installer yet.

## Controls

- **New note:** enter text, then select Save note (or press Ctrl+Enter). Cancel discards the dialog's changes.
- **Select:** click a note. Its border indicates selection.
- **Move:** drag a note; its position saves when you release the mouse.
- **Edit:** double-click a note, or select it and press Edit. The editor supports multiple lines and opens the full text even when the wall shows a shortened preview.
- **Delete:** select a note, press Delete, then confirm.
- **Color:** select a note, then press Yellow, Green, Blue, or Pink.
- **Save:** creation, editing, deletion, colors, and released drags save automatically. Closing the app also saves.

Notes are stored in `%LOCALAPPDATA%\StickyWall\notes.json`. Paste that folder path into Windows File Explorer to inspect or back up your file. Only open one copy of the app at a time; separate instances do not synchronize.

Step 1 did not save notes, so it has no saved notes to import. Unreadable existing saves are protected: the app shows an error and disables saving instead of overwriting them. Keep a backup, repair or rename the file, then restart. Save errors are shown to you rather than reported as successful.

## Understand the new code in five small steps

### 1. The dictionary is the app's data

```python
notes = {
    'note_1': {'text': 'Practice Python', 'x': 40, 'y': 40, 'color': '#FBE59A'}
}
```

The outer key identifies a note. The inner dictionary stores its text, position, and color. Tkinter draws a picture of this data; the dictionary is what gets saved.

### 2. Selecting tells buttons which note to change

`selected` holds a tag such as `note_1`, or `None`. `select_note()` sets it, draws a border, and enables the edit/delete/color buttons. A shared canvas tag ties each note's rectangle, shadow, and text together.

### 3. Editing and colors follow the same pattern

Change the dictionary, redraw the note, then save.

```python
notes[selected]['color'] = color
draw_note(selected)
save_notes()
```

`open_editor()` creates a separate window with a Text box. Its inner function, `apply_changes()`, can access that editor's text box. This is a nested function: it keeps the small dialog's actions together. New notes get a unique numbered ID; edits keep their ID.

The color buttons use `lambda chosen=color: change_color(chosen)`. The default argument remembers each button's own color when that button is created. Without that detail, the loop's buttons could all use its last color.

### 4. Deleting removes both data and drawing

After confirmation, `wall.delete(tag)` removes the drawing and `del notes[tag]` removes the dictionary entry. Then the app saves. There is no delete undo in this version.

### 5. JSON keeps data after the program ends

`json.dumps()` converts the dictionary into text. `json.loads()` converts saved text back into a dictionary. `Path` helps work with files and folders.

`write_notes()` writes a temporary file first and replaces the main save only after writing succeeds. That avoids clearing the old save before the new one is ready. `read_notes()` checks the data before using it. `try/except` catches file or data errors so the app can show a useful message.

The editor and display never execute saved text as Python code.

## Test it on your Windows computer

1. Create two notes, including one with multiple lines and accented characters.
2. Edit one, then reopen it and confirm the full text is present.
3. Try all four colors, and drag a note near the edge.
4. Close and reopen the app: text, positions, and colors should remain.
5. Cancel a deletion and confirm the note remains. Confirm deletion, restart, and confirm it is gone.
6. Resize the window smaller: notes should stay reachable.

The included storage tests passed in the development environment. Windows GUI testing is still a separate check. Run the storage tests with `py -m unittest test_storage.py`.

## Explain it in an interview

Use this explanation once you can explain the corresponding functions yourself:

“I built a small Python sticky-note board using Tkinter. Each note is a dictionary with text, position, and color. Mouse events handle dragging, and buttons update the selected note. I serialize the notes to JSON so they survive restarting. I used AI assistance and reviewed and tested the code as I learned.”

Be specific about which parts you wrote, adapted, and learned with assistance. This project does not claim a database, cloud service, AI product feature, or production deployment.

## A good stopping point

This version contains only the features requested for today. Connections, search, completion tracking, GitHub publication, and Windows executable packaging are deferred. There are no due dates or reminders.

Practice task: add a fifth color to COLORS and predict why a new button appears without writing another button creation block.

## Editor layout fix

The editor now uses three grid rows: label, text, and action buttons. Only the text row expands. This keeps Save note and Cancel visible in the editor. Ctrl+Enter also saves.
