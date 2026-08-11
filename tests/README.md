# Contract tests

These tests validate repository structure, behavioral contracts, and the dependency-free local tracker without calling a model.

Each `.prompt.md` fixture describes an invocation and its repository evidence. Its paired `.expected.md` preserves expected behavior for forward-test scenarios. `test_contracts.py` checks the published Feature-centered skill contract, while `test_local_work_tracker.py` exercises identity, revision checks, dependency-aware assignment, transitions, validation, and generated views in a temporary Git repository.

Run:

```bash
python3 -m unittest discover -s tests -v
```
