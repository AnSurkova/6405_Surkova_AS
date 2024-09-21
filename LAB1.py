import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math
import argparse


def read_config(config_file):
    tree = ET.parse(config_file)
    root = tree.getroot()

    config = {
        'n0': float(root.find('n0').text),
        'h': float(root.find('h').text),
        'nk': float(root.find('nk').text),
        'a': float(root.find('a').text),
        'b': float(root.find('b').text),
        'c': float(root.find('c').text)
    }

    return config


def compute_y(x, a, b, c):
    try:
        sqrt_part = math.sqrt(a - x)
        sin_part = math.sin(b * x) ** 2
        return sqrt_part * sin_part + c
    except ValueError:
        return None  # Возвращаем None, если a - x < 0, чтобы избежать ошибки при вычислении корня


def write_results(results_file, results):
    root = ET.Element("results")

    for x, y in results:
        result_elem = ET.SubElement(root, "result")
        x_elem = ET.SubElement(result_elem, "x")
        y_elem = ET.SubElement(result_elem, "y")

        x_elem.text = str(x)
        y_elem.text = str(
            y) if y is not None else "undefined"  # Обработка случая, если значение не может быть вычислено

    # Создание строки из XML-дерева
    rough_string = ET.tostring(root, 'utf-8')

    # Использование minidom для форматирования
    reparsed = minidom.parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    # Запись форматированного XML в файл
    with open(results_file, "w", encoding='utf-8') as f:
        f.write(pretty_xml_as_string)


def run(config_file="config.xml", results_file="results.xml"):

    config = read_config(config_file)
    n0 = config['n0']
    h = config['h']
    nk = config['nk']
    a = config['a']
    b = config['b']
    c = config['c']

    # Вычисление значений
    x = n0
    results = []
    while x <= nk:
        y = compute_y(x, a, b, c)
        results.append((x, y))
        x += h

    # Запись результатов в файл
    write_results(results_file, results)


def main():
    parser = argparse.ArgumentParser(description="Вычисление y(x) на заданном диапазоне.")
    parser.add_argument("config", nargs='?', default=None, help="Путь к XML файлу конфигурации")
    parser.add_argument("output", nargs='?', default=None, help="Путь к XML файлу для записи результатов")

    args = parser.parse_args()

    if args.config and args.output:
        run(args.config, args.output)
    else:
        run()


if __name__ == "__main__":
    main()
