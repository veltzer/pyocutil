"""Behavioural tests for pyocutil's file helpers."""

import os
import tempfile
import unittest

from pyocutil import utils


class EnsureDirTests(unittest.TestCase):
    def test_creates_missing_parent(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "a", "b", "file.txt")
            utils.ensure_dir(target)
            self.assertTrue(os.path.isdir(os.path.join(d, "a", "b")))


class TouchTests(unittest.TestCase):
    def test_creates_new_file(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "new.txt")
            utils.touch(target)
            self.assertTrue(os.path.isfile(target))

    def test_touch_mkdir_creates_dirs_and_file(self):
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "x", "y", "z.txt")
            utils.touch_mkdir(target)
            self.assertTrue(os.path.isfile(target))

    def test_touch_mkdir_many(self):
        with tempfile.TemporaryDirectory() as d:
            names = [os.path.join(d, f"s{i}", f"f{i}.txt") for i in range(3)]
            utils.touch_mkdir_many(names)
            self.assertTrue(all(os.path.isfile(n) for n in names))


class DoInstallTests(unittest.TestCase):
    def test_creates_symlink_when_doit(self):
        with tempfile.TemporaryDirectory() as d:
            source = os.path.join(d, "source.txt")
            target = os.path.join(d, "link.txt")
            with open(source, "w", encoding="utf-8") as fh:
                fh.write("data")
            utils.do_install(source, target, force=False, doit=True)
            self.assertTrue(os.path.islink(target))
            self.assertEqual(os.readlink(target), source)

    def test_no_symlink_when_not_doit(self):
        with tempfile.TemporaryDirectory() as d:
            source = os.path.join(d, "source.txt")
            target = os.path.join(d, "link.txt")
            utils.do_install(source, target, force=False, doit=False)
            self.assertFalse(os.path.lexists(target))

    def test_force_replaces_existing_link(self):
        with tempfile.TemporaryDirectory() as d:
            first = os.path.join(d, "first.txt")
            second = os.path.join(d, "second.txt")
            target = os.path.join(d, "link.txt")
            os.symlink(first, target)
            utils.do_install(second, target, force=True, doit=True)
            self.assertEqual(os.readlink(target), second)


class FileGenTests(unittest.TestCase):
    def test_non_recursive_lists_only_top_level(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "top.txt"), "w", encoding="utf-8"):
                pass
            os.mkdir(os.path.join(d, "subdir"))
            with open(os.path.join(d, "subdir", "deep.txt"), "w", encoding="utf-8"):
                pass
            results = list(utils.file_gen(d, recurse=False))
            self.assertEqual(len(results), 1)
            root, directories, files = results[0]
            self.assertEqual(root, d)
            self.assertEqual(directories, ["subdir"])
            self.assertEqual(files, ["top.txt"])

    def test_recursive_walks_subdirectories(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, "subdir"))
            with open(os.path.join(d, "subdir", "deep.txt"), "w", encoding="utf-8"):
                pass
            all_files = []
            for _root, _dirs, files in utils.file_gen(d, recurse=True):
                all_files.extend(files)
            self.assertIn("deep.txt", all_files)


if __name__ == "__main__":
    unittest.main()
