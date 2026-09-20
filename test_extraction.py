from pathlib import Path
from backend.extraction import extract_file

TEST_DIR = Path("data/test_documents")


def test_file(filename):
    print()
    print("=" * 70)
    print(f"TESTING: {filename}")
    print("=" * 70)

    path = TEST_DIR / filename

    if not path.exists():
        print(f"FILE NOT FOUND: {path}")
        return

    try:
        documents = extract_file(path)

        print(f"Extracted units: {len(documents)}")

        total_chars = 0

        for i, document in enumerate(documents, 1):
            text = getattr(document, "text", str(document))
            total_chars += len(text)

            print()
            print(f"--- Unit {i} ---")
            print(f"Text: {text}")

        print()
        print(f"Total characters: {total_chars}")

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")


def main():
    test_file("test_schemes.csv")
    test_file("test_scheme.docx")
    test_file("test_scheme.pdf")
    test_file("test_notes.txt")
    test_file("test_schemes.xlsx")


if __name__ == "__main__":
    main()