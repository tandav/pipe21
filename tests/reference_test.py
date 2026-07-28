import ast
import doctest
import re
import tomllib
from pathlib import Path

import pipe21 as P

ROOT = Path(__file__).parent.parent
REFERENCE = ROOT / 'docs' / 'reference.md'
STUB = ROOT / 'pipe21.pyi'
PYPROJECT = ROOT / 'pyproject.toml'


def all_ops():
    out = []
    for k, v in vars(P).items():
        if not isinstance(v, type):
            continue
        if not issubclass(v, P.B):
            continue
        if v is P.B:
            continue
        out.append(k)
    return out


def stub_classes():
    tree = ast.parse(STUB.read_text())
    return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]


def test_all_operators_have_reference_docs():
    """Every operator is documented, and the reference is sorted alphabetically."""
    reference = REFERENCE.read_text()
    assert re.findall(r'## (\w+)', reference) == sorted(all_ops())


def test_reference_doctests_pass():
    result = doctest.testfile(str(REFERENCE), module_relative=False)
    assert result.failed == 0


def test_stub_matches_public_operators():
    """Every operator is typed in pipe21.pyi, and the stub declares nothing extra."""
    stub = {c for c in stub_classes() if not c.startswith('_')}
    assert stub == {*all_ops(), 'B'}


def test_version_matches_pyproject():
    pyproject = tomllib.loads(PYPROJECT.read_text())
    assert P.__version__ == pyproject['project']['version']
