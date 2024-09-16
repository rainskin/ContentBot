import os
import envparse


def load(file_path: str):
    envparse.env.read_envfile(file_path)


def parse(key: str, required=True) -> str | None:
    if key in os.environ:
        return os.environ[key]
    if not required:
        return None
    raise LookupError(f"Environment variable `{key}` not set")


class Env:
    def __init__(self, file_path: str):
        load(file_path)

    @staticmethod
    def parse_str(key: str, required=True) -> str | None:
        return parse(key, required)

    @staticmethod
    def parse_int(key: str, required=True) -> int | None:
        value = parse(key, required)
        if value is None:
            return value
        return int(value)


env = Env(".env")
