def read_file(path: str):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return "File not found"