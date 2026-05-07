import pytest
from cli import parse_args, process_file
from io import StringIO

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
    print("RESULT:", result)
    assert result == expected