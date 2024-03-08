from filemanager import FileManager
from driver import MSDriver


def main():
    print("MS Code-checker запущен!")

    try:
        filemanager = FileManager()
    except (ValueError, FileNotFoundError) as error:
        print(error)
    else:
        ms_driver = MSDriver(filemanager)
        result = ms_driver.start()

        print(
            "Програма успешно завершила работу!"
            if result
            else "Программа звершила работу с ошибкой авторизации! Скорее всего, "
                 "превышено время ожидания. Попробуйте запустить проверку заново."
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
