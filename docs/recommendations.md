# OPN Recommendations (Best Practices)

Practical recommendations for readable and stable OPN projects.

## 1. Naming
- Use descriptive names for variables and functions.
- Prefer `snake_case` or `camelCase` consistently in one project.

## 2. File organization
- Keep one main program per `.opn` file.
- Split large projects by domain.
- Keep docs examples under `docs/test` or similar folders.

## 3. Functions
- Keep functions small and single-purpose.
- Return explicit values.
- Avoid hidden mutations when possible.

## 4. Classes
- Use `init` to define initial state.
- Keep methods cohesive.
- Prefer explicit state transitions (example: `complete()` method).

## 5. Imports and dependencies
- Import only what is needed.
- Let OPN auto-install missing dependencies when useful.
- Keep `opn.json` clean and reviewed.

## 6. Runtime workflow
Recommended flow:
1. `opn app.opn`
2. `opn deps show`
3. `opn deps sync`
4. `opn compile app.opn -o app.py`
5. `opn build app.opn -o dist/app`

## 7. Error handling mindset
- Reproduce with the smallest input.
- Isolate parser errors vs runtime errors.
- Use invalid test corpus (`docs/test/21`-`25`) to learn fast.

## 8. For AI-assisted development
When prompting an AI:
- Paste exact error message.
- Paste minimal failing `.opn` snippet.
- Mention target platform (Windows/Linux/macOS).
- Ask for code that matches current parser support only.
