import argparse
import re
import sys
import traceback

from opn2 import OPNError, compile_opn_file, print_opn_error


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="opn_compiler.py", description="Compila .opn a .py")
    parser.add_argument("input", help="Archivo fuente .opn")
    parser.add_argument("-o", "--output", help="Archivo destino .py")
    args = parser.parse_args(argv)

    output = args.output or re.sub(r"\.opn$", ".py", args.input)
    if output == args.input:
        output = args.input + ".py"

    try:
        compile_opn_file(args.input, output)
    except FileNotFoundError as err:
        raise OPNError(
            "No se encontro el archivo fuente para compilar",
            code="OPN4001",
            phase="CLI",
            source_name=args.input,
            hint="Verifica la ruta de entrada.",
            details=str(err),
        ) from err
    print(f"Compilado: {args.input} -> {output}")
    return 0


if __name__ == "__main__":
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
