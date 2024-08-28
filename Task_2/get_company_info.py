import json
from typing import List, Tuple, Dict


def recurse_func(data: Dict, result_list: List) -> List[Tuple[str, int]]:
    """
    Рекурсивно обходит data и извлекает пары (title, id)

    :param data: Словарь с данными о компаниях
    :param result_list: Пустой список для заполнения

    :return: Список, заполненный кортежами (title, id)
    """

    if isinstance(data, dict):
        if 'title' in data and 'id' in data:
            result_list.append((data['title'], data['id']))

        for key, value in data.items():
            recurse_func(value, result_list)

    elif isinstance(data, list):
        for item in data:
            recurse_func(item, result_list)

    return result_list


def extract_company_data(company_data: Dict) -> Tuple[Tuple[str, int], ...]:
    """

    :param company_data: Словарь с данными о компаниях
    :return: Кортеж заполненный парами (title, id)
    """
    result_list = []
    company_pairs_list = recurse_func(company_data, result_list)

    return tuple(company_pairs_list)


def get_json_data(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        load_data = json.load(file)

    return load_data

if __name__ == '__main__':
    data_from_json = get_json_data(filename='new_test_hw.json')
    result = extract_company_data(data_from_json)
    print(result)
