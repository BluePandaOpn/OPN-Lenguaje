import argparse
import ast
import hashlib
import os
import re
import sys
import traceback
import warnings
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Optional

# Suppress pygame and setuptools warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")
warnings.filterwarnings("ignore", message=".*setuptools.*")


class OPNError(Exception):
    def __init__(
        self,
        message: str,
        token: Optional["Token"] = None,
        *,
        code: str = "OPN0000",
        phase: str = "General",
        source_name: Optional[str] = None,
        source_code: Optional[str] = None,
        line: Optional[int] = None,
        col: Optional[int] = None,
        details: Optional[str] = None,
        hint: Optional[str] = None,
    ):
        self.message = message
        self.code = code
        self.phase = phase
        self.source_name = source_name
        self.source_code = source_code
        self.details = details
        self.hint = hint
        self.line = line if line is not None else (token.line if token else None)
        self.col = col if col is not None else (token.col if token else None)
        super().__init__(self.__str__())

    def __str__(self) -> str:
        if self.line is not None and self.col is not None:
            return f"[Linea {self.line}, Col {self.col}] {self.message}"
        return self.message


class _Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"


def _supports_color(stream: Any) -> bool:
    if os.getenv("NO_COLOR"):
        return False
    return bool(hasattr(stream, "isatty") and stream.isatty())


def _apply_color(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{color}{text}{_Ansi.RESET}"


def _line_excerpt(source_code: str, line: int, col: int) -> list[str]:
    lines = source_code.splitlines()
    if line < 1 or line > len(lines):
        return []
    source_line = lines[line - 1]
    pointer_col = max(1, min(col, len(source_line) + 1))
    pointer = " " * (pointer_col - 1) + "^"
    return [source_line, pointer]


def format_opn_error(exc: OPNError, *, color: bool = True) -> str:
    header = f"{exc.phase}Error [{exc.code}]"
    lines = [
        _apply_color(header, _Ansi.RED + _Ansi.BOLD, color),
        _apply_color(exc.message, _Ansi.YELLOW, color),
    ]

    if exc.source_name:
        loc = exc.source_name
        if exc.line is not None and exc.col is not None:
            loc += f":{exc.line}:{exc.col}"
        lines.append(_apply_color(f"  Archivo: {loc}", _Ansi.CYAN, color))

    if exc.source_code and exc.line is not None and exc.col is not None:
        excerpt = _line_excerpt(exc.source_code, exc.line, exc.col)
        if excerpt:
            lines.append(_apply_color(f"  {exc.line:>4} | {excerpt[0]}", _Ansi.GRAY, color))
            lines.append(_apply_color(f"       | {excerpt[1]}", _Ansi.RED, color))

    if exc.details:
        lines.append(_apply_color(f"  Detalle: {exc.details}", _Ansi.GRAY, color))
    if exc.hint:
        lines.append(_apply_color(f"  Sugerencia: {exc.hint}", _Ansi.CYAN, color))
    return "\n".join(lines)


def print_opn_error(exc: OPNError, *, stream: Any = sys.stderr) -> None:
    color = _supports_color(stream)
    stream.write(format_opn_error(exc, color=color) + "\n")


TOKEN_SPEC = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP", r"==|!=|<=|>=|\|\||&&|\+|-|\*|/|%|<|>|=|!"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("DOT", r"\."),
    ("COMMA", r","),
    ("COLON", r":"),
    ("SEMICOL", r";"),
    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t\r]+"),
    ("MISMATCH", r"."),
]

KEYWORDS = {
    "var",
    "function",
    "func",
    "class",
    "if",
    "else",
    "while",
    "for",
    "return",
    "true",
    "false",
    "null",
    "this",
    "import",
    "from",
    "as",
}

TOKEN_REGEX = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))
LINE_COMMENT_REGEX = re.compile(r"//.*")
# El transpiler inserta 5 lineas de preambulo y una linea en blanco antes del cuerpo.
GENERATED_BODY_LINE_OFFSET = 6
DEFAULT_CACHE_SIZE = 128


class LRUCache:
    def __init__(self, maxsize: int = DEFAULT_CACHE_SIZE):
        self.maxsize = maxsize
        self._data: OrderedDict[tuple[str, str], Any] = OrderedDict()

    def get(self, key: tuple[str, str]) -> Any:
        if key not in self._data:
            return None
        value = self._data.pop(key)
        self._data[key] = value
        return value

    def set(self, key: tuple[str, str], value: Any) -> None:
        if key in self._data:
            self._data.pop(key)
        self._data[key] = value
        if len(self._data) > self.maxsize:
            self._data.popitem(last=False)


_TRANSPILE_CACHE = LRUCache()
_COMPILED_CACHE = LRUCache()


@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int


class Lexer:
    def __init__(self, code: str, source_name: Optional[str] = None):
        self.source_name = source_name
        self.source_code = code
        self.code = LINE_COMMENT_REGEX.sub("", code)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        line = 1
        col = 1
        append_token = tokens.append
        token_regex = TOKEN_REGEX

        for mo in token_regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == "NEWLINE":
                line += 1
                col = 1
                continue
            if kind == "SKIP":
                col += len(value)
                continue
            if kind == "MISMATCH":
                bad = Token("MISMATCH", value, line, col)
                raise OPNError(
                    f"Caracter inesperado: {value}",
                    bad,
                    code="OPN1001",
                    phase="Lexico",
                    source_name=self.source_name,
                    source_code=self.source_code,
                    hint="Revisa simbolos no validos o comillas sin cerrar.",
                )
            if kind == "ID" and value in KEYWORDS:
                kind = value.upper()

            append_token(Token(kind, value, line, col))
            col += len(value)

        append_token(Token("EOF", "", line, col))
        return tokens


class Node:
    pass


@dataclass
class Program(Node):
    body: list[Node]


@dataclass
class Block(Node):
    body: list[Node]


@dataclass
class VarDecl(Node):
    name: str
    expr: Node


@dataclass
class FunctionDecl(Node):
    name: str
    params: list[str]
    body: Block


@dataclass
class ClassDecl(Node):
    name: str
    body: Block


@dataclass
class IfStmt(Node):
    test: Node
    cons: Block
    alt: Optional[Block]


@dataclass
class WhileStmt(Node):
    test: Node
    body: Block


@dataclass
class ForStmt(Node):
    init: Optional[Node]
    test: Optional[Node]
    update: Optional[Node]
    body: Block


@dataclass
class ReturnStmt(Node):
    expr: Optional[Node]


@dataclass
class ExprStmt(Node):
    expr: Node


@dataclass
class ImportStmt(Node):
    module: str
    alias: Optional[str]


@dataclass
class FromImportStmt(Node):
    module: str
    names: list[tuple[str, Optional[str]]]


@dataclass
class AssignExpr(Node):
    target: Node
    value: Node


@dataclass
class BinaryExpr(Node):
    left: Node
    op: str
    right: Node


@dataclass
class UnaryExpr(Node):
    op: str
    value: Node


@dataclass
class Literal(Node):
    value: Any


@dataclass
class Identifier(Node):
    name: str


@dataclass
class CallExpr(Node):
    callee: Node
    args: list[Node]


@dataclass
class MemberExpr(Node):
    obj: Node
    prop: str


@dataclass
class IndexExpr(Node):
    obj: Node
    index: Node


@dataclass
class ArrayLiteral(Node):
    elements: list[Node]


@dataclass
class DictLiteral(Node):
    pairs: list[tuple[Node, Node]]


class Parser:
    def __init__(
        self,
        tokens: list[Token],
        source_name: Optional[str] = None,
        source_code: Optional[str] = None,
    ):
        self.tokens = tokens
        self.pos = 0
        self.source_name = source_name
        self.source_code = source_code

    def current(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.current()
        self.pos += 1
        return tok

    def eat(self, t: str) -> Token:
        tok = self.current()
        if tok.type != t:
            raise OPNError(
                f"Se esperaba {t}, pero se encontro {tok.type or 'EOF'}",
                tok,
                code="OPN2001",
                phase="Sintaxis",
                source_name=self.source_name,
                source_code=self.source_code,
            )
        return self.advance()

    def match(self, t: str) -> bool:
        if self.current().type == t:
            self.pos += 1
            return True
        return False

    def match_op(self, op: str) -> bool:
        tok = self.current()
        if tok.type == "OP" and tok.value == op:
            self.pos += 1
            return True
        return False

    def eat_semicol(self) -> None:
        self.eat("SEMICOL")

    def parse(self) -> Program:
        body = []
        while self.current().type != "EOF":
            body.append(self.statement())
        return Program(body)

    def statement(self) -> Node:
        tok = self.current()
        if tok.type == "VAR":
            return self.var_decl(require_semicol=True)
        if tok.type in ("FUNCTION", "FUNC"):
            return self.func_decl()
        if tok.type == "CLASS":
            return self.class_decl()
        if tok.type == "IF":
            return self.if_stmt()
        if tok.type == "WHILE":
            return self.while_stmt()
        if tok.type == "FOR":
            return self.for_stmt()
        if tok.type == "RETURN":
            return self.return_stmt()
        if tok.type == "IMPORT":
            return self.import_stmt()
        if tok.type == "FROM":
            return self.from_import_stmt()
        if tok.type == "LBRACE":
            return self.block()
        expr = self.expression()
        self.eat_semicol()
        return ExprStmt(expr)

    def block(self) -> Block:
        self.eat("LBRACE")
        body = []
        while self.current().type != "RBRACE":
            if self.current().type == "EOF":
                raise OPNError(
                    "Falta '}' para cerrar bloque",
                    self.current(),
                    code="OPN2002",
                    phase="Sintaxis",
                    source_name=self.source_name,
                    source_code=self.source_code,
                )
            body.append(self.statement())
        self.eat("RBRACE")
        return Block(body)

    def var_decl(self, require_semicol: bool) -> VarDecl:
        self.eat("VAR")
        name = self.eat("ID").value
        self.eat("OP")
        expr = self.expression()
        if require_semicol:
            self.eat_semicol()
        return VarDecl(name, expr)

    def func_decl(self) -> FunctionDecl:
        if self.current().type in ("FUNCTION", "FUNC"):
            self.advance()
        else:
            self.eat("FUNCTION")
        name = self.eat("ID").value
        self.eat("LPAREN")
        params = []
        if self.current().type != "RPAREN":
            params.append(self.eat("ID").value)
            while self.match("COMMA"):
                params.append(self.eat("ID").value)
        self.eat("RPAREN")
        body = self.block()
        return FunctionDecl(name, params, body)

    def class_decl(self) -> ClassDecl:
        self.eat("CLASS")
        name = self.eat("ID").value
        body = self.block()
        return ClassDecl(name, body)

    def if_stmt(self) -> IfStmt:
        self.eat("IF")
        self.eat("LPAREN")
        test = self.expression()
        self.eat("RPAREN")
        cons = self.block()
        alt = None
        if self.match("ELSE"):
            alt = self.block()
        return IfStmt(test, cons, alt)

    def while_stmt(self) -> WhileStmt:
        self.eat("WHILE")
        self.eat("LPAREN")
        test = self.expression()
        self.eat("RPAREN")
        body = self.block()
        return WhileStmt(test, body)

    def for_stmt(self) -> ForStmt:
        self.eat("FOR")
        self.eat("LPAREN")

        init: Optional[Node] = None
        if self.current().type != "SEMICOL":
            if self.current().type == "VAR":
                init = self.var_decl(require_semicol=False)
            else:
                init = ExprStmt(self.expression())
        self.eat("SEMICOL")

        test: Optional[Node] = None
        if self.current().type != "SEMICOL":
            test = self.expression()
        self.eat("SEMICOL")

        update: Optional[Node] = None
        if self.current().type != "RPAREN":
            update = self.expression()
        self.eat("RPAREN")

        body = self.block()
        return ForStmt(init, test, update, body)

    def return_stmt(self) -> ReturnStmt:
        self.eat("RETURN")
        expr = None
        if self.current().type != "SEMICOL":
            expr = self.expression()
        self.eat_semicol()
        return ReturnStmt(expr)

    def import_stmt(self) -> ImportStmt:
        self.eat("IMPORT")
        module = self.eat("ID").value
        while self.match("DOT"):
            module += "." + self.eat("ID").value
        alias = None
        if self.match("AS"):
            alias = self.eat("ID").value
        self.eat_semicol()
        return ImportStmt(module, alias)

    def from_import_stmt(self) -> FromImportStmt:
        self.eat("FROM")
        module = self.eat("ID").value
        while self.match("DOT"):
            module += "." + self.eat("ID").value
        self.eat("IMPORT")

        names: list[tuple[str, Optional[str]]] = []
        names.append(self.import_name())
        while self.match("COMMA"):
            names.append(self.import_name())
        self.eat_semicol()
        return FromImportStmt(module, names)

    def import_name(self) -> tuple[str, Optional[str]]:
        name = self.eat("ID").value
        alias = None
        if self.match("AS"):
            alias = self.eat("ID").value
        return name, alias

    def expression(self) -> Node:
        return self.assignment()

    def assignment(self) -> Node:
        expr = self.logic_or()
        if self.match_op("="):
            value = self.assignment()
            if not isinstance(expr, (Identifier, MemberExpr, IndexExpr)):
                raise OPNError(
                    "Asignacion invalida",
                    self.current(),
                    code="OPN2003",
                    phase="Sintaxis",
                    source_name=self.source_name,
                    source_code=self.source_code,
                    hint="El lado izquierdo debe ser variable, propiedad o indice.",
                )
            return AssignExpr(expr, value)
        return expr

    def logic_or(self) -> Node:
        expr = self.logic_and()
        while self.match_op("||"):
            expr = BinaryExpr(expr, "||", self.logic_and())
        return expr

    def logic_and(self) -> Node:
        expr = self.equality()
        while self.match_op("&&"):
            expr = BinaryExpr(expr, "&&", self.equality())
        return expr

    def equality(self) -> Node:
        expr = self.comparison()
        while self.current().type == "OP" and self.current().value in ("==", "!="):
            op = self.advance().value
            expr = BinaryExpr(expr, op, self.comparison())
        return expr

    def comparison(self) -> Node:
        expr = self.addition()
        while self.current().type == "OP" and self.current().value in ("<", "<=", ">", ">="):
            op = self.advance().value
            expr = BinaryExpr(expr, op, self.addition())
        return expr

    def addition(self) -> Node:
        expr = self.multiplication()
        while self.current().type == "OP" and self.current().value in ("+", "-"):
            op = self.advance().value
            expr = BinaryExpr(expr, op, self.multiplication())
        return expr

    def multiplication(self) -> Node:
        expr = self.unary()
        while self.current().type == "OP" and self.current().value in ("*", "/", "%"):
            op = self.advance().value
            expr = BinaryExpr(expr, op, self.unary())
        return expr

    def unary(self) -> Node:
        if self.current().type == "OP" and self.current().value in ("!", "-"):
            op = self.advance().value
            return UnaryExpr(op, self.unary())
        return self.call()

    def call(self) -> Node:
        expr = self.primary()
        while True:
            if self.match("LPAREN"):
                args = []
                if self.current().type != "RPAREN":
                    args.append(self.expression())
                    while self.match("COMMA"):
                        args.append(self.expression())
                self.eat("RPAREN")
                expr = CallExpr(expr, args)
                continue
            if self.match("DOT"):
                prop = self.eat("ID").value
                expr = MemberExpr(expr, prop)
                continue
            if self.match("LBRACKET"):
                idx = self.expression()
                self.eat("RBRACKET")
                expr = IndexExpr(expr, idx)
                continue
            break
        return expr

    def primary(self) -> Node:
        tok = self.current()
        if tok.type == "NUMBER":
            self.advance()
            if "." in tok.value:
                return Literal(float(tok.value))
            return Literal(int(tok.value))
        if tok.type == "STRING":
            self.advance()
            return Literal(ast.literal_eval(tok.value))
        if tok.type == "TRUE":
            self.advance()
            return Literal(True)
        if tok.type == "FALSE":
            self.advance()
            return Literal(False)
        if tok.type == "NULL":
            self.advance()
            return Literal(None)
        if tok.type == "THIS":
            self.advance()
            return Identifier("this")
        if tok.type == "ID":
            self.advance()
            return Identifier(tok.value)
        if tok.type == "LPAREN":
            self.advance()
            expr = self.expression()
            self.eat("RPAREN")
            return expr
        if tok.type == "LBRACKET":
            return self.array_literal()
        if tok.type == "LBRACE":
            return self.dict_literal()
        raise OPNError(
            "Expresion invalida",
            tok,
            code="OPN2004",
            phase="Sintaxis",
            source_name=self.source_name,
            source_code=self.source_code,
        )

    def array_literal(self) -> ArrayLiteral:
        self.eat("LBRACKET")
        elements = []
        if self.current().type != "RBRACKET":
            elements.append(self.expression())
            while self.match("COMMA"):
                elements.append(self.expression())
        self.eat("RBRACKET")
        return ArrayLiteral(elements)

    def dict_literal(self) -> DictLiteral:
        self.eat("LBRACE")
        pairs: list[tuple[Node, Node]] = []
        if self.current().type != "RBRACE":
            pairs.append(self.dict_pair())
            while self.match("COMMA"):
                pairs.append(self.dict_pair())
        self.eat("RBRACE")
        return DictLiteral(pairs)

    def dict_pair(self) -> tuple[Node, Node]:
        key = self.expression()
        self.eat("COLON")
        value = self.expression()
        return key, value


class Transpiler:
    def __init__(self):
        self.indent = 0

    def emit(self, line: str) -> str:
        return ("    " * self.indent) + line

    def transpile(self, node: Node, in_class: bool = False) -> str:
        if isinstance(node, Program):
            chunks = [self.transpile(stmt) for stmt in node.body]
            body = "\n".join(c for c in chunks if c.strip())
            prelude = "\n".join(
                [
                    "import sys as _opn_sys",
                    "if hasattr(_opn_sys.stdout, 'reconfigure'):",
                    "    _opn_sys.stdout.reconfigure(encoding='utf-8')",
                    "if hasattr(_opn_sys.stderr, 'reconfigure'):",
                    "    _opn_sys.stderr.reconfigure(encoding='utf-8')",
                ]
            )
            if body:
                return prelude + "\n\n" + body
            return prelude

        if isinstance(node, Block):
            chunks = [self.transpile(stmt, in_class=in_class) for stmt in node.body]
            lines = [c for c in chunks if c.strip()]
            return "\n".join(lines) if lines else self.emit("pass")

        if isinstance(node, ImportStmt):
            if node.alias:
                return self.emit(f"import {node.module} as {node.alias}")
            return self.emit(f"import {node.module}")

        if isinstance(node, FromImportStmt):
            names = []
            for name, alias in node.names:
                if alias:
                    names.append(f"{name} as {alias}")
                else:
                    names.append(name)
            return self.emit(f"from {node.module} import {', '.join(names)}")

        if isinstance(node, VarDecl):
            return self.emit(f"{node.name} = {self.expr(node.expr)}")

        if isinstance(node, FunctionDecl):
            py_name = "__init__" if in_class and node.name == "init" else node.name
            params = list(node.params)
            if in_class and (not params or params[0] != "self"):
                params.insert(0, "self")
            header = self.emit(f"def {py_name}({', '.join(params)}):")
            self.indent += 1
            body = self.transpile(node.body, in_class=in_class)
            self.indent -= 1
            return header + "\n" + body

        if isinstance(node, ClassDecl):
            header = self.emit(f"class {node.name}:")
            self.indent += 1
            body = self.transpile(node.body, in_class=True)
            self.indent -= 1
            return header + "\n" + body

        if isinstance(node, IfStmt):
            head = self.emit(f"if {self.expr(node.test)}:")
            self.indent += 1
            cons = self.transpile(node.cons, in_class=in_class)
            self.indent -= 1
            if not node.alt:
                return head + "\n" + cons
            else_head = self.emit("else:")
            self.indent += 1
            alt = self.transpile(node.alt, in_class=in_class)
            self.indent -= 1
            return head + "\n" + cons + "\n" + else_head + "\n" + alt

        if isinstance(node, WhileStmt):
            head = self.emit(f"while {self.expr(node.test)}:")
            self.indent += 1
            body = self.transpile(node.body, in_class=in_class)
            self.indent -= 1
            return head + "\n" + body

        if isinstance(node, ForStmt):
            range_info = self._for_to_range(node)
            if range_info is not None:
                var_name, range_args = range_info
                reduced = self._reduce_sum_loop(node, var_name, range_args, in_class)
                if reduced is not None:
                    return reduced
                header = self.emit(f"for {var_name} in range({range_args}):")
                self.indent += 1
                body_code = self.transpile(node.body, in_class=in_class)
                self.indent -= 1
                return header + "\n" + body_code

            lines = []
            if node.init:
                lines.append(self.transpile(node.init, in_class=in_class))
            cond = self.expr(node.test) if node.test else "True"
            lines.append(self.emit(f"while {cond}:"))
            self.indent += 1
            body_code = self.transpile(node.body, in_class=in_class)
            lines.append(body_code)
            if node.update:
                lines.append(self.emit(self.expr(node.update)))
            self.indent -= 1
            return "\n".join(lines)

        if isinstance(node, ReturnStmt):
            if node.expr is None:
                return self.emit("return")
            return self.emit(f"return {self.expr(node.expr)}")

        if isinstance(node, ExprStmt):
            return self.emit(self.expr(node.expr))

        return ""

    def expr(self, node: Node) -> str:
        if isinstance(node, Literal):
            return repr(node.value)
        if isinstance(node, Identifier):
            return "self" if node.name == "this" else node.name
        if isinstance(node, AssignExpr):
            return f"{self.expr(node.target)} = {self.expr(node.value)}"
        if isinstance(node, BinaryExpr):
            if isinstance(node.left, Literal) and isinstance(node.right, Literal):
                folded = self._eval_const_binary(node.op, node.left.value, node.right.value)
                if folded is not None:
                    return repr(folded)
            op = node.op.replace("&&", "and").replace("||", "or")
            return f"({self.expr(node.left)} {op} {self.expr(node.right)})"
        if isinstance(node, UnaryExpr):
            if node.op == "!":
                return f"(not {self.expr(node.value)})"
            if isinstance(node.value, Literal) and node.op == "-":
                if isinstance(node.value.value, (int, float)):
                    return repr(-node.value.value)
            return f"(-{self.expr(node.value)})"
        if isinstance(node, CallExpr):
            args = ", ".join(self.expr(arg) for arg in node.args)
            return f"{self.expr(node.callee)}({args})"
        if isinstance(node, MemberExpr):
            return f"{self.expr(node.obj)}.{node.prop}"
        if isinstance(node, IndexExpr):
            return f"{self.expr(node.obj)}[{self.expr(node.index)}]"
        if isinstance(node, ArrayLiteral):
            return "[" + ", ".join(self.expr(e) for e in node.elements) + "]"
        if isinstance(node, DictLiteral):
            pairs = [f"{self.expr(k)}: {self.expr(v)}" for k, v in node.pairs]
            return "{" + ", ".join(pairs) + "}"
        return "None"

    def _eval_const_binary(self, op: str, left: Any, right: Any) -> Optional[Any]:
        if op in ("&&", "||"):
            return None
        if op == "+":
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            return None
        if op in ("-", "*", "/", "%"):
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                return None
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                return left / right
            if op == "%":
                return left % right
        return None

    def _for_to_range(self, node: ForStmt) -> Optional[tuple[str, str]]:
        if node.init is None or node.test is None or node.update is None:
            return None

        var_name = None
        start_expr = None

        if isinstance(node.init, VarDecl):
            var_name = node.init.name
            start_expr = self.expr(node.init.expr)
        elif isinstance(node.init, ExprStmt) and isinstance(node.init.expr, AssignExpr):
            assign = node.init.expr
            if isinstance(assign.target, Identifier):
                var_name = assign.target.name
                start_expr = self.expr(assign.value)
        if not var_name or start_expr is None:
            return None

        if not isinstance(node.test, BinaryExpr):
            return None
        if not isinstance(node.test.left, Identifier):
            return None
        if node.test.left.name != var_name:
            return None
        if node.test.op not in ("<", "<=", ">", ">="):
            return None
        end_expr = self.expr(node.test.right)

        if not isinstance(node.update, AssignExpr):
            return None
        if not isinstance(node.update.target, Identifier):
            return None
        if node.update.target.name != var_name:
            return None
        if not isinstance(node.update.value, BinaryExpr):
            return None
        if not isinstance(node.update.value.left, Identifier):
            return None
        if node.update.value.left.name != var_name:
            return None
        if node.update.value.op not in ("+", "-"):
            return None
        if not isinstance(node.update.value.right, Literal):
            return None
        step_value = node.update.value.right.value
        if not isinstance(step_value, int) or step_value != 1:
            return None

        step = 1 if node.update.value.op == "+" else -1

        if node.test.op in ("<", "<=") and step < 0:
            return None
        if node.test.op in (">", ">=") and step > 0:
            return None

        if node.test.op == "<":
            stop_expr = end_expr
        elif node.test.op == "<=":
            stop_expr = f"({end_expr} + 1)"
        elif node.test.op == ">":
            stop_expr = end_expr
        else:
            stop_expr = f"({end_expr} - 1)"

        if step == 1:
            range_args = f"{start_expr}, {stop_expr}"
        else:
            range_args = f"{start_expr}, {stop_expr}, -1"
        return var_name, range_args

    def _reduce_sum_loop(
        self, node: ForStmt, var_name: str, range_args: str, in_class: bool
    ) -> Optional[str]:
        if not isinstance(node.body, Block):
            return None
        if len(node.body.body) != 1:
            return None
        stmt = node.body.body[0]
        if not isinstance(stmt, ExprStmt):
            return None
        if not isinstance(stmt.expr, AssignExpr):
            return None
        assign = stmt.expr
        if not isinstance(assign.target, Identifier):
            return None
        acc = assign.target.name
        if not isinstance(assign.value, BinaryExpr):
            return None
        if assign.value.op != "+":
            return None

        left = assign.value.left
        right = assign.value.right
        if isinstance(left, Identifier) and isinstance(right, Identifier):
            if left.name == acc and right.name == var_name:
                return self.emit(f"{acc} += sum(range({range_args}))")
            if left.name == var_name and right.name == acc:
                return self.emit(f"{acc} += sum(range({range_args}))")
        return None


def _cache_key(source: str, source_name: Optional[str] = None) -> tuple[str, str]:
    digest = hashlib.blake2b(source.encode("utf-8"), digest_size=16).hexdigest()
    return digest, source_name or "<opn>"


def parse_opn(code: str, source_name: Optional[str] = None) -> Program:
    lexer = Lexer(code, source_name=source_name)
    tokens = lexer.tokenize()
    parser = Parser(tokens, source_name=source_name, source_code=code)
    return parser.parse()


def transpile_opn(code: str, source_name: Optional[str] = None) -> str:
    key = _cache_key(code, source_name)
    cached = _TRANSPILE_CACHE.get(key)
    if cached is not None:
        return cached
    ast_root = parse_opn(code, source_name=source_name)
    transpiler = Transpiler()
    py_code = transpiler.transpile(ast_root)
    _TRANSPILE_CACHE.set(key, py_code)
    return py_code


def compile_opn(code: str, source_name: Optional[str] = None) -> Any:
    key = _cache_key(code, source_name)
    compiled = _COMPILED_CACHE.get(key)
    if compiled is not None:
        return compiled
    py_code = transpile_opn(code, source_name=source_name)
    filename = f"<opn:{source_name or '<memory>'}>"
    compiled = compile(py_code, filename, "exec")
    _COMPILED_CACHE.set(key, compiled)
    return compiled


def compile_opn_file(source_path: str, output_path: str) -> str:
    with open(source_path, "r", encoding="utf-8") as f:
        code = f.read()
    py_code = transpile_opn(code, source_name=source_path)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(py_code + ("\n" if py_code and not py_code.endswith("\n") else ""))
    return output_path


class OPNInterpreter:
    def __init__(self):
        self.globals = {"__builtins__": __builtins__}

    def run(self, code: str, source_name: str = "<opn>") -> None:
        compiled = compile_opn(code, source_name=source_name)
        try:
            exec(compiled, self.globals)
        except OPNError:
            raise
        except Exception as err:
            tb = traceback.extract_tb(err.__traceback__)
            opn_frame = None
            for frame in reversed(tb):
                if frame.filename.startswith("<opn:"):
                    opn_frame = frame
                    break
            generated_line = opn_frame.lineno if opn_frame else None
            line = (
                max(1, generated_line - GENERATED_BODY_LINE_OFFSET)
                if generated_line is not None
                else None
            )
            col = 1 if opn_frame else None
            detail = "".join(traceback.format_exception_only(type(err), err)).strip()
            raise OPNError(
                "Error durante la ejecucion del programa OPN",
                code="OPN3001",
                phase="Runtime",
                source_name=source_name,
                source_code=code,
                line=line,
                col=col,
                details=f"{detail} (linea Python generada: {generated_line})"
                if generated_line is not None
                else detail,
            ) from err


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="opn2.py",
        description="Interprete y compilador de OPN (.opn -> .py).",
    )
    parser.add_argument(
        "args",
        nargs="+",
        help="Uso rapido: opn2.py archivo.opn | opn2.py run archivo.opn | opn2.py compile in.opn -o out.py",
    )
    parser.add_argument("-o", "--output", help="Ruta de salida para compile")
    ns = parser.parse_args(argv)

    if len(ns.args) == 1 and ns.args[0].endswith(".opn"):
        path = ns.args[0]
        try:
            with open(path, "r", encoding="utf-8") as f:
                OPNInterpreter().run(f.read(), source_name=path)
        except FileNotFoundError as err:
            raise OPNError(
                "No se encontro el archivo .opn",
                code="OPN4001",
                phase="CLI",
                source_name=path,
                hint="Verifica la ruta o el nombre del archivo.",
                details=str(err),
            ) from err
        return 0

    cmd = ns.args[0]
    if cmd == "run":
        if len(ns.args) < 2:
            raise OPNError(
                "Falta archivo .opn para run",
                code="OPN4002",
                phase="CLI",
                hint="Uso: opn2.py run archivo.opn",
            )
        path = ns.args[1]
        try:
            with open(path, "r", encoding="utf-8") as f:
                OPNInterpreter().run(f.read(), source_name=path)
        except FileNotFoundError as err:
            raise OPNError(
                "No se encontro el archivo .opn",
                code="OPN4001",
                phase="CLI",
                source_name=path,
                hint="Verifica la ruta o el nombre del archivo.",
                details=str(err),
            ) from err
        return 0

    if cmd == "compile":
        if len(ns.args) < 2:
            raise OPNError(
                "Falta archivo .opn para compile",
                code="OPN4003",
                phase="CLI",
                hint="Uso: opn2.py compile in.opn -o out.py",
            )
        src = ns.args[1]
        out = ns.output or re.sub(r"\.opn$", ".py", src)
        if out == src:
            out = src + ".py"
        try:
            compile_opn_file(src, out)
        except FileNotFoundError as err:
            raise OPNError(
                "No se encontro el archivo fuente para compilar",
                code="OPN4001",
                phase="CLI",
                source_name=src,
                hint="Verifica la ruta de entrada.",
                details=str(err),
            ) from err
        print(f"Compilado: {src} -> {out}")
        return 0

    raise OPNError(
        f"Comando no soportado: {cmd}",
        code="OPN4004",
        phase="CLI",
        hint="Comandos validos: run, compile",
    )


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(main(sys.argv[1:]))
    except OPNError as exc:
        print_opn_error(exc)
        raise SystemExit(1)
    except Exception as exc:
        err = OPNError(
            "Fallo interno no controlado",
            code="OPN9000",
            phase="Interno",
            details="".join(traceback.format_exception_only(type(exc), exc)).strip(),
        )
        print_opn_error(err)
        raise SystemExit(1)
