# CLI and Build - OPN BluePanda

[Back to README](../README.md)

Command reference for daily development and distribution.

ES (optional): Referencia de comandos para desarrollo y distribucion.

## Core commands
- Run file: `opn app.opn`
- Explicit run: `opn run app.opn`
- Compile to Python: `opn compile app.opn -o app.py`
- Setup current project env: `opn setup`
- Dependency management: `opn deps show | opn deps sync | opn deps add <pkg> | opn deps remove <pkg>`
- Run Python module in project venv: `opn -m pip install requests`
- Build portable binary: `opn build app.opn -o dist/app`

## Run and compile
```bash
opn app.opn
opn compile app.opn -o app.py
python app.py
```

## Venv module proxy (`-m`)
```bash
opn -m pip --version
opn -m pip install pygame
opn -m pip list
```

## Project setup and dependency sync
```bash
opn setup
opn deps show
opn deps sync
opn deps add requests
opn deps remove requests
```

## Portable build
`opn build` flow:
1. Ensure `.venv` exists.
2. Ensure `pip` exists in `.venv`.
3. Ensure `pyinstaller` exists in `.venv`.
4. Transpile `.opn` to temporary `.py`.
5. Generate one-file binary into `dist/`.

Examples:

```bash
opn build game.opn
opn build game.opn -o dist/game_final
```

Output:
- Windows: `dist/game.exe`
- Linux/macOS: `dist/game`

## Common errors
- `OPN4001`: source file not found
- `OPN4006`: failed to create `.venv`
- `OPN4007`: `pip` unavailable in `.venv`
- `OPN4009`: missing file for build command
- `OPN4010`: build generation failed
- `OPN4011`: failed to install PyInstaller
- `OPN4013`: dependency sync failed
- `OPN4014`: missing package in `deps add`
- `OPN4015`: missing package in `deps remove`
- `OPN4016`: unsupported `deps` subcommand

## Project metadata file
```json
{
  "name": "my-project",
  "version": "0.1.2",
  "dependencies": ["pygame", "requests"]
}
```

## Related guides
- Quickstart: `docs/quickstart.md`
- Syntax: `docs/syntax.md`
- Performance: `docs/performance.md`
- Rules: `docs/language_rules.md`
- Recommendations: `docs/recommendations.md`
- Test corpus: `docs/test/README.md`
