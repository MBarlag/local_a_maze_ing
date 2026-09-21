from submodules.config import Config
import pytest
from os import remove

VALID=[
    ("", {}), 
    ("\n", {}), 
    ("\n\n", {}), 
    ("OUTPUT=file#2.txt",
        {"OUTPUT": "file"}), 
    ("#comment\nOUT=3.txt #comment 2", 
        {"OUT": "3.txt"})
]

INVALID=["OUTPUT#=file2.txt", "A=3, B=4", "C==3", "D=my=file.txt"]
FILENAME="test_config.txt"

@pytest.fixture(autouse=True)
def file_handling():
    # code before the test
    with open(FILENAME, "w", encoding="utf-8") as f:
        pass
    yield
    # code after test
    remove(FILENAME)

@pytest.mark.parametrize("input,expected", VALID)
def test_valid(input: str, expected: dict[str, str]):
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(input)
    assert Config(FILENAME).parse_config() == expected

@pytest.mark.parametrize("input", INVALID)
def test_invalid(input: str):
    with open(FILENAME, "w", encoding="utf-8") as f:
        f.write(input)
    with pytest.raises(Exception):
        Config(FILENAME).parse_config()
