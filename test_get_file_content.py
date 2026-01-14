from functions.get_file_content import get_file_content
from config import MAX_CHARS


def test():
    # 1. lorem.txt truncation test
    lorem = get_file_content("calculator", "lorem.txt")
    assert len(lorem) > MAX_CHARS
    assert lorem.endswith(
        f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    )

    # 2. Print required outputs
    result = get_file_content("calculator", "main.py")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print(result)

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)


if __name__ == "__main__":
    test()