"""Storage checks: run with py -m unittest test_storage.py."""
import tempfile
import unittest
from pathlib import Path
from sticky_wall import read_notes, write_notes


class StorageTests(unittest.TestCase):
    def test_round_trip_and_delete(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'StickyWall' / 'notes.json'
            self.assertEqual(read_notes(path), {})
            data = {'note_1': {'text': 'Español\nSecond line', 'x': 52, 'y': 64, 'color': '#FBE59A'}}
            write_notes(path, data)
            self.assertEqual(read_notes(path), data)
            write_notes(path, {})
            self.assertEqual(read_notes(path), {})

    def test_reject_corrupt_data_without_modifying_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'notes.json'
            for text in ['broken json', '[]', '{"note_1": {"text": "hello"}}']:
                path.write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    read_notes(path)
                self.assertEqual(path.read_text(encoding='utf-8'), text)


if __name__ == '__main__':
    unittest.main()
