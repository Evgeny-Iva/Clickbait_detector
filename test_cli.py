from io import StringIO

from cli import parse_args, print_table, process_file


def test_parse_args_default():
    args = parse_args(["--files", "video.csv"])
    assert args.files == ["video.csv"]
    assert args.report == "clickbait"


def test_parser_args_custom_report():
    args = parse_args(["--files", "data.csv", "--report", "summary"])
    assert args.report == "summary"


def test_process_file(monkeypatch):
    fake_csv = "title,ctr,retention\nВидео 1,20,30\nВидео 2,10,50\nВидео 3,25,35\n"

    def mock_open(*args, **kwargs):
        return StringIO(fake_csv)

    monkeypatch.setattr("builtins.open", mock_open)

    result = process_file("fake_path.csv")

    expected = [["Видео 1", 20.0, 30.0], ["Видео 3", 25.0, 35.0]]
    assert result == expected


def test_print_table(capsys):
    data = [
        ["Видео 1", 20.0, 30.0],
        ["Видео 3", 25.0, 35.0],
    ]

    print_table(data)
    captured = capsys.readouterr()
    output = captured.out

    assert "title" in output
    assert "ctr" in output
    assert "retention" in output

    assert "Видео 1" in output
    assert "Видео 3" in output
    assert "20.0" in output
    assert "25.0" in output
