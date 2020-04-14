import os

from petisco import Petisco


def petisco_config():
    Petisco.from_filename(os.path.dirname(os.path.abspath(__file__)) + "/petisco.yml")


def main():
    petisco_config()
    Petisco.get_instance().start()


if __name__ == "__main__":
    main()
