# Contract tests

These tests validate repository structure and behavioral contracts without calling a model.

Each `.prompt.md` fixture describes an independent invocation and its repository evidence. Its paired `.expected.md` lists observable requirements for a compliant response or artifact. `test_contracts.py` checks fixture pairing and the high-risk invariants encoded by the skills.

Run:

```bash
python3 -m unittest discover -s tests -v
```
