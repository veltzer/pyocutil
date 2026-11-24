# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pyocutil/utils.py:50` - `do_install` unlinks an existing target symlink whenever `force` is set, before checking `doit`, so the dry-run mode (`--doit=False`, `force` defaults to `True` at `src/pyocutil/configs.py:41-44`) still deletes links; move the unlink under `if doit:`.

## Medium

- `src/pyocutil/main.py:39` - with `recurse` (default `True`) `file_gen` walks the whole tree, but every file is linked flat into `target_folder` by basename while its parent directory is also linked; nested files are double-installed and two files with the same name in different subfolders crash `os.symlink` with `FileExistsError`. Either link only the top level or mirror the relative path under the target.
- `src/pyocutil/main.py:33` - stale-link cleanup tests `link_target.startswith(cwd)` instead of the configured `source_folder`, and a plain string prefix also matches sibling dirs (`/a/b` vs `/a/bc`); compare against `os.path.realpath(source_folder)` with a path-aware check.
- `src/pyocutil/main.py:37` - `os.mkdir` fails when the target's parent does not exist; use `os.makedirs(..., exist_ok=True)`. Note `target_folder` is declared `create_existing_folder` at `src/pyocutil/configs.py:26`, which is misleading since a missing folder is supported.
- `pyproject.toml:15` - description/keywords say "utilities for openshift" (`config/project.lua:2`), but no command touches `oc` or OpenShift - they are symlink, touch and exit-code wrappers; fix the description and keywords.

## Low

- `doc/TODO.txt:1` - first item says `symlink_install` does not create the target folder, but `src/pyocutil/main.py:37` already does; remove or update the stale item.
- `src/pyocutil/main.py:70` - `no_err` has no `min_free_args=1`, so running it with no arguments crashes with a traceback from `subprocess.call([])`; add `min_free_args=1` like the sibling endpoints.
- `src/pyocutil/main.py:142` - `wrapper_css_validator` uses `check_output`, so a non-zero validator exit raises `CalledProcessError` with a traceback instead of printing the errors; use `subprocess.run(..., capture_output=True)` and inspect the output.
