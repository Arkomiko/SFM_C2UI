"""
Test runner.

Zero dependencies on purpose: the engine is pure standard library at this stage,
so the tests must run anywhere Python does.

    python Testing/run.py                 everything
    python Testing/run.py core            one folder
    python Testing/run.py core/test_vfs   one module

A test is any top-level `test_*` function in a `test_*.py` file. Failures are
reported with the assertion message and the runner exits non-zero.
"""
from __future__ import annotations

import importlib.util
import sys
import time
import traceback
from pathlib import Path
from typing import Callable, List, Tuple

TESTING_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTING_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

FOLDERS = ("core", "app", "tools")


def _load(path: Path):
    name = "c2ui_tests." + path.relative_to(TESTING_DIR).as_posix().replace("/", ".")[:-3]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _collect(selector: str = "") -> List[Tuple[str, Callable[[], None]]]:
    files: List[Path] = []
    if selector:
        target = TESTING_DIR / selector
        if target.is_dir():
            files = sorted(target.rglob("test_*.py"))
        elif target.with_suffix(".py").is_file():
            files = [target.with_suffix(".py")]
        elif target.is_file():
            files = [target]
    else:
        for folder in FOLDERS:
            d = TESTING_DIR / folder
            if d.is_dir():
                files.extend(sorted(d.rglob("test_*.py")))

    tests: List[Tuple[str, Callable[[], None]]] = []
    for file in files:
        try:
            module = _load(file)
        except Exception:
            label = file.relative_to(TESTING_DIR).as_posix()
            def _fail(_tb=traceback.format_exc()):
                raise AssertionError("import failed:\n" + _tb)
            tests.append((f"{label}::<import>", _fail))
            continue
        label = file.relative_to(TESTING_DIR).as_posix()
        for attr in sorted(vars(module)):
            if attr.startswith("test_") and callable(getattr(module, attr)):
                tests.append((f"{label}::{attr}", getattr(module, attr)))
    return tests


def main(argv: List[str]) -> int:
    selector = argv[0] if argv else ""
    tests = _collect(selector)
    if not tests:
        print("no tests found" + (f" for {selector!r}" if selector else ""))
        return 1

    passed, failures = 0, []
    started = time.time()
    for name, fn in tests:
        try:
            fn()
            passed += 1
            print(f"  ok    {name}")
        except Exception as exc:
            failures.append((name, exc, traceback.format_exc()))
            print(f"  FAIL  {name}")

    print()
    print("=" * 72)
    for name, exc, tb in failures:
        print(f"FAIL {name}")
        message = str(exc).strip()
        if message:
            for line in message.splitlines():
                print("      " + line)
        else:
            print("      " + tb.strip().splitlines()[-1])
        print()
    elapsed = time.time() - started
    print(f"{passed}/{len(tests)} passed in {elapsed:.2f}s")
    print("=" * 72)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
