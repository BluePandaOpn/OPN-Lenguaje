import sys
import traceback

from opn2 import OPNError, main as runtime_main, print_opn_error


def main(argv: list[str]) -> int:
    # Keep opn.py as a thin wrapper so all CLI behavior lives in opn2.py.
    return runtime_main(argv)


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
