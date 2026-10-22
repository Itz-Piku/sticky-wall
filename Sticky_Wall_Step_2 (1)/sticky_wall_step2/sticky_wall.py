"""Sticky Wall: a small Tkinter app using dictionaries and JSON.
Run: py sticky_wall.py
Click to select, drag to move, double-click to edit.
"""
import json
import math
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

NOTE_WIDTH, NOTE_HEIGHT = 220, 170
COLORS = {'Yellow': '#FBE59A', 'Green': '#CBE8D1',
          'Blue': '#CCDDF8', 'Pink': '#F4CCD6'}
# AppData is writable even when the app is later installed in Program Files.
SAVE_FILE = Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'StickyWall' / 'notes.json'
notes = {}
selected = None
next_note_id = 1
saving_enabled = True
drag = {'tag': None, 'x': 0, 'y': 0}


def read_notes(path):
    """Read and check saved data before using it in the interface."""
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Expected a dictionary of notes.')
    for tag, note in data.items():
        if not tag.startswith('note_') or not tag[5:].isdigit():
            raise ValueError('Invalid note ID.')
        if not isinstance(note, dict) or not isinstance(note.get('text'), str):
            raise ValueError('Invalid note text.')
        if note.get('color') not in COLORS.values():
            raise ValueError('Invalid note color.')
        for axis in ('x', 'y'):
            value = note.get(axis)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError('Invalid note position.')
    return data


def write_notes(path, data):
    """Write a temporary file, then replace the old save after writing succeeds."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    temporary.replace(path)


def save_notes():
    if not saving_enabled:
        status.set('Saving disabled: your existing save could not be read.')
        return False
    try:
        write_notes(SAVE_FILE, notes)
    except OSError as error:
        status.set('Not saved — check the save location or disk space.')
        messagebox.showerror('Could not save notes', str(error), parent=root)
        return False
    status.set(f'{len(notes)} notes  •  Saved automatically')
    return True


def draw_note(tag):
    """Redraw one note from its dictionary; all shapes share the same tag."""
    wall.delete(tag)
    note = notes[tag]
    x, y = note['x'], note['y']
    wall.create_rectangle(x + 5, y + 5, x + NOTE_WIDTH + 5, y + NOTE_HEIGHT + 5,
                          fill='#D6D2C9', outline='', tags=(tag,))
    wall.create_rectangle(x, y, x + NOTE_WIDTH, y + NOTE_HEIGHT,
                          fill=note['color'], outline='', tags=(tag, 'paper'))
    # The board shows a preview. The editor always opens the complete text.
    text = ' '.join(note['text'].split())
    preview = text[:110] + ('…' if len(text) > 110 else '')
    wall.create_text(x + 16, y + 16, text=preview, width=NOTE_WIDTH - 32,
                     anchor='nw', font=('Segoe UI', 12), fill='#25312E', tags=(tag,))


def select_note(tag):
    global selected
    selected = tag
    wall.itemconfigure('paper', outline='', width=1)
    if tag:
        for item in wall.find_withtag(tag):
            if 'paper' in wall.gettags(item):
                wall.itemconfigure(item, outline='#253E35', width=2)
        wall.tag_raise(tag)
    state = 'normal' if tag else 'disabled'
    for button in note_buttons:
        button.configure(state=state)


def open_editor(tag=None):
    """One small editor handles both new notes and edits."""
    editor = tk.Toplevel(root)
    editor.title('Edit note' if tag else 'New note')
    editor.geometry('440x340')
    editor.minsize(360, 260)
    editor.transient(root)
    # Only the text row expands; the action row always keeps its own space.
    editor.columnconfigure(0, weight=1)
    editor.rowconfigure(1, weight=1)
    tk.Label(editor, text='Write your note:', padx=12, pady=8).grid(row=0, column=0, sticky='w')
    text_box = tk.Text(editor, height=8, width=30, font=('Segoe UI', 12), wrap='word', undo=True)
    text_box.grid(row=1, column=0, sticky='nsew', padx=12)
    if tag:
        text_box.insert('1.0', notes[tag]['text'])

    def apply_changes():
        global next_note_id
        text = text_box.get('1.0', 'end-1c').strip()
        if not text:
            messagebox.showinfo('Empty note', 'Enter some text, or choose Cancel.', parent=editor)
            return
        note_tag = tag
        if note_tag is None:
            note_tag = f'note_{next_note_id}'
            offset = (next_note_id - 1) % 6
            notes[note_tag] = {'text': text, 'x': 40 + offset * 35,
                               'y': 40 + offset * 25, 'color': COLORS['Yellow']}
            next_note_id += 1
        else:
            notes[note_tag]['text'] = text
        draw_note(note_tag)
        select_note(note_tag)
        editor.destroy()
        save_notes()

    actions = tk.Frame(editor, padx=12, pady=10)
    actions.grid(row=2, column=0, sticky='ew')
    tk.Button(actions, text='Save note', command=apply_changes).pack(side='right')
    tk.Button(actions, text='Cancel', command=editor.destroy).pack(side='right', padx=8)
    editor.bind('<Control-Return>', lambda event: apply_changes())
    editor.bind('<Escape>', lambda event: editor.destroy())
    editor.grab_set()
    text_box.focus_set()


def edit_selected():
    if selected:
        open_editor(selected)


def delete_selected():
    if selected and messagebox.askyesno('Delete note?', 'Permanently delete this note?', parent=root):
        tag = selected
        wall.delete(tag)
        del notes[tag]
        select_note(None)
        save_notes()


def change_color(color):
    if selected:
        notes[selected]['color'] = color
        draw_note(selected)
        select_note(selected)
        save_notes()


def start_drag(event):
    items = wall.find_withtag('current')
    tag = wall.gettags(items[0])[0] if items else None
    select_note(tag if tag in notes else None)
    drag.update(tag=selected, x=event.x, y=event.y)
    if selected:
        wall.configure(cursor='fleur')


def move_note(event):
    tag = drag['tag']
    if tag is None:
        return
    note = notes[tag]
    x = max(8, min(note['x'] + event.x - drag['x'], wall.winfo_width() - NOTE_WIDTH - 8))
    y = max(8, min(note['y'] + event.y - drag['y'], wall.winfo_height() - NOTE_HEIGHT - 8))
    wall.move(tag, x - note['x'], y - note['y'])
    note.update(x=x, y=y)
    drag.update(x=event.x, y=event.y)


def stop_drag(event):
    was_dragging = drag['tag'] is not None
    drag['tag'] = None
    wall.configure(cursor='')
    if was_dragging:
        save_notes()


def resize_wall(event):
    """Keep notes reachable if the window becomes smaller."""
    for tag, note in notes.items():
        x = max(8, min(note['x'], event.width - NOTE_WIDTH - 8))
        y = max(8, min(note['y'], event.height - NOTE_HEIGHT - 8))
        wall.move(tag, x - note['x'], y - note['y'])
        note.update(x=x, y=y)


def close_app():
    if not save_notes():
        if not messagebox.askyesno('Unsaved changes', 'Close anyway? Changes may be lost.', parent=root):
            return
    root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Sticky Wall')
    root.geometry('1000x700')
    root.minsize(800, 480)
    root.configure(bg='#F7F5EF')
    toolbar = tk.Frame(root, bg='#F7F5EF', padx=18, pady=12)
    toolbar.pack(fill='x')
    tk.Label(toolbar, text='Sticky Wall', font=('Segoe UI', 20, 'bold'),
             bg='#F7F5EF', fg='#25312E').pack(side='left', padx=(0, 16))
    tk.Button(toolbar, text='+ New note', command=open_editor).pack(side='left', padx=3)
    note_buttons = []
    for label, command in [('Edit', edit_selected), ('Delete', delete_selected)]:
        button = tk.Button(toolbar, text=label, command=command, state='disabled')
        button.pack(side='left', padx=3)
        note_buttons.append(button)
    for name, color in COLORS.items():
        button = tk.Button(toolbar, text=name, bg=color, state='disabled',
                           command=lambda chosen=color: change_color(chosen))
        button.pack(side='left', padx=3)
        note_buttons.append(button)
    status = tk.StringVar(value='Click to select  •  Drag to move  •  Double-click to edit')
    tk.Label(root, textvariable=status, bg='#F7F5EF', fg='#59635E',
             font=('Segoe UI', 10), padx=18, pady=12).pack(side='bottom', anchor='w')
    wall = tk.Canvas(root, bg='#EBE8DF', highlightthickness=0)
    wall.pack(fill='both', expand=True, padx=18)
    wall.bind('<Button-1>', start_drag)
    wall.bind('<B1-Motion>', move_note)
    wall.bind('<ButtonRelease-1>', stop_drag)
    wall.bind('<Double-Button-1>', lambda event: edit_selected())
    wall.bind('<Configure>', resize_wall)
    root.protocol('WM_DELETE_WINDOW', close_app)
    try:
        notes = read_notes(SAVE_FILE)
    except (OSError, ValueError) as error:
        saving_enabled = False  # Never overwrite an unreadable existing save.
        messagebox.showerror('Could not load notes', f'{error}\n\nFile: {SAVE_FILE}\n'
                             'Saving is disabled to protect this file. Back it up and repair or rename it, then restart.', parent=root)
        status.set('Saving disabled: existing save could not be read.')
    next_note_id = max((int(tag[5:]) for tag in notes), default=0) + 1
    for tag in notes:
        draw_note(tag)
    root.mainloop()
