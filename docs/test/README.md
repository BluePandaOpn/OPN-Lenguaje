# OPN Test Corpus (30 `.opn` Files)

This folder contains curated examples for learning, testing, and AI context ingestion.

## Goal
- Provide runnable examples for core language features.
- Provide intentional invalid examples to teach parser limits.
- Give AI assistants realistic snippets for code generation and debugging.

## File groups
- `01` to `20`: valid examples (should run if dependencies exist).
- `21` to `25`: invalid examples (should fail by design).
- `26` to `30`: advanced but valid composition examples.

## How to use
- Run a single test:

```bash
opn docs/test/01_hello_world.opn
```

- Compile and inspect generated Python:

```bash
opn compile docs/test/12_class_init_method.opn -o out.py
```

## Invalid test policy
Invalid files are marked with comments like `INVALID TEST` and are intentionally included for teaching.

## Recommended learning order
1. `01` to `08` (syntax and flow)
2. `09` to `15` (data + imports + classes)
3. `16` to `20` (logic + runtime behavior)
4. `21` to `25` (what not to write)
5. `26` to `30` (composition patterns)

## Related docs
- Main rules: `docs/language_rules.md`
- Best practices: `docs/recommendations.md`
- Syntax reference: `docs/syntax.md`
