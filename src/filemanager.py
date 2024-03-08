import os

from typing import List


class FileManager:
    def __init__(self) -> None:
        self.__CODES_FILENAME = "codes.txt"
        self.__VALID_CODES_FILENAME = "valid.txt"

        if not os.path.exists(self.__CODES_FILENAME):
            open(self.__CODES_FILENAME, "a")
            raise FileNotFoundError("Отсутствующий файл с кодами был создан. Для начала работы заполните его.")

    @staticmethod
    def read_file(filepath: str) -> List[str]:
        with open(filepath, "r", encoding="utf-8") as file:
            return [code.replace("\n", "") for code in file.readlines()]

    def get_codes(self) -> List[str]:
        codes = self.read_file(self.__CODES_FILENAME)

        if not codes:
            raise ValueError("Файл с кодами пуст!")

        return codes

    def write_valid_code(self, code: str):
        with open(self.__VALID_CODES_FILENAME, "a", encoding="utf-8") as file:
            if code not in self.read_file(self.__VALID_CODES_FILENAME):
                file.write(f"{code}\n")
