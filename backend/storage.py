from pathlib import Path
import pickle


class Storage:
    def __init__(self, directory: str = "data/storage"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, data):
        path = self.directory / f"{name}.pkl"

        with open(path, "wb") as file:
            pickle.dump(data, file)

        return path

    def load(self, name: str):
        path = self.directory / f"{name}.pkl"

        if not path.exists():
            return None

        with open(path, "rb") as file:
            return pickle.load(file)

    def exists(self, name: str):
        path = self.directory / f"{name}.pkl"
        return path.exists()