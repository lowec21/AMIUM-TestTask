from typing import List

from playwright.sync_api import sync_playwright
import openpyxl


def parse_python_releases() -> List[List[str]]:
    """
    Парсит таблицу релизов Python по номерам версий

    :return: Список списков, где каждый вложенный список содержит информацию о релизе:
             [release_version, release_date, download_link, release_notes_link]
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        page = browser.new_page()
        page.goto("https://www.python.org/downloads/")

        # получаем все элементы списка релизов из нужного блока
        releases_section = page.query_selector("div.row.download-list-widget")
        list_items = releases_section.query_selector_all("ol.list-row-container.menu > li")

        data = []

        for item in list_items: # получаем данные из каждого элемента списка
            release_version = item.query_selector("span.release-number").inner_text()
            release_date = item.query_selector("span.release-date").inner_text()
            download_link = item.query_selector("span.release-download a").get_attribute("href")
            release_notes_link = item.query_selector("span.release-enhancements a").get_attribute("href")

            data.append([release_version, release_date, download_link, release_notes_link]) # добавляем информацию в data

        browser.close()

        return data


# функция для сохранения данных в Excel
def save_to_excel(data: List[List[str]], filename: str) -> None:
    """
    Сохраняет данные из (data) в файл формата xlsx для просмотра в Excel

    :param data: Данные для записи
    :param filename: Имя файла в который будут сохранены данные
    """

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Python Releases"

    headers = ["Release version", "Release date", "Download", "Release Notes"]
    sheet.append(headers)

    for row in data:
        sheet.append(row) # добавляем данные в таблицу

    workbook.save(filename)


# Основная функция
def main():
    data = parse_python_releases() # парсим таблицу с сайта

    save_to_excel(data, filename="python_releases.xlsx") # сохраняем данные в формате xlsx в текущую директорию


if __name__ == "__main__":
    main()