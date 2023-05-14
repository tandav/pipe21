import re
from pathlib import Path

import pipe21 as P


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


def test_all_operators_have_reference_docs():
    reference = Path('docs/reference.md').read_text()
    assert re.findall(r'## (\w+)', reference) == all_ops()
