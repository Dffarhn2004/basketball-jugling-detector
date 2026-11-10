from bounce_counter.cli import build_parser, main


def test_help_parser_contains_doctor() -> None:
    parser = build_parser()
    assert "doctor" in parser.format_help()


def test_doctor_returns_success(capsys) -> None:
    assert main(["doctor"]) == 0
    assert "python=" in capsys.readouterr().out
