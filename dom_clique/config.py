import configparser
import dataclasses


@dataclasses.dataclass
class Config:
    token: str


def load_config(path: str) -> Config:
    parser = configparser.ConfigParser()
    parser.read(path)

    return Config(token=parser["bot"]["token"])
