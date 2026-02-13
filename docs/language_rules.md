# OPN Language Rules (Clarity Guide)

This document defines what to write and what to avoid in OPN BluePanda (`0.1.2`).

## 1. Statement endings
- Normal statements must end with `;`.
- Examples: variable declaration, assignment, function call, import.

Correct:
```opn
var x = 10;
print(x);
```

## 2. Block endings
- Do **not** write `};` after block-based declarations in OPN.
- Preferred endings:
  - `}` for `if`, `while`, `for`, `function`, `class`

Avoid:
```opn
function bad() {
    print("x");
};
```

## 3. Comments
- Supported: `//` line comments.
- Not supported: `#` comments.

Correct:
```opn
// this is valid
var ok = true;
```

Invalid:
```opn
# this is invalid in current parser
var x = 1;
```

## 4. Supported control structures
- Supported: `if/else`, `while`, `for`
- Not supported in current parser: `do...while`, `try/catch`

## 5. Imports
- Use `import module;`
- Use `from module import name;`
- Use `as` alias where needed.

## 6. Keyword set
Supported keywords:
- `var`, `function`, `func`, `class`
- `if`, `else`, `while`, `for`, `return`
- `true`, `false`, `null`, `this`
- `import`, `from`, `as`

## 7. Quick validation references
- Valid examples: `docs/test/01_hello_world.opn` to `docs/test/20_runtime_missing_module.opn`
- Invalid examples: `docs/test/21_invalid_missing_semicolon.opn` to `docs/test/25_invalid_try_catch.opn`
