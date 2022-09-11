import argparse
import os
import json
from collections import defaultdict


class Education:
    def __init__(self, path, english, encoding):
        self.directory = path
        self.text = ""
        self.to_json_prefix_one = dict()
        self.to_json_prefix_two = dict()
        self.english = english
        self.encoding = encoding
        self.read_directory()

    def read_directory(self):
        # чтение и обработка всех файлов в директории
        for file in os.listdir(self.directory):
            with open(os.path.join(self.directory, file), 'r', encoding=self.encoding) as tec_file:
                self.text = tec_file.read()
                self.to_clear()
                self.word_processing()
        self.finish()

    def word_processing(self):
        # обработка слов
        for words in self.text.split('\n'):
            words = words.split()
            new_words = []
            for word in words:
                if len(word) > 0:
                    new_words.append(word)
            for ind in range(len(new_words) - 2):  # запись слов в словарь префиксла длины 2
                first, second, next = new_words[ind], new_words[ind + 1], new_words[ind + 2]
                if (first, second) not in self.to_json_prefix_two:
                    self.to_json_prefix_two[(first, second)] = defaultdict(int)
                self.to_json_prefix_two[(first, second)][next] += 1
            for ind in range(len(new_words) - 1):  # запись слов в словарь префиксла длины 1
                first, next = new_words[ind], new_words[ind + 1]
                if first not in self.to_json_prefix_one:
                    self.to_json_prefix_one[first] = defaultdict(int)
                self.to_json_prefix_one[first][next] += 1

    def to_clear(self):
        # удаление лишних символов из строки
        new_text = ""
        for symbol in self.text.lower():
            if ord('а') <= ord(symbol) <= ord('я') or \
                    symbol == 'ё' or (self.english and ord('a') <= ord(symbol) <= ord('z')):
                new_text += symbol
            elif symbol in ['.', ',', '!', '?', ':']:
                new_text += '\n'
            else:
                new_text += ' '
        self.text = new_text

    def finish(self):
        # подсчет вероятности использования для каждого слова и запись в файлы *.json
        new_to_json_two = dict()
        for key in list(self.to_json_prefix_two.keys()):
            new_to_json_two[key[0] + ':' + key[1]] = []
            sums = 0
            for mini_key in list(self.to_json_prefix_two[key].keys()):
                sums += self.to_json_prefix_two[key][mini_key]
            for mini_key in list(self.to_json_prefix_two[key].keys()):
                new_to_json_two[key[0] + ':' + key[1]].append((mini_key,
                                                               round(self.to_json_prefix_two[key][mini_key] / sums, 8)))
        with open('dictionary_prefix_two.json', 'w') as file:
            json.dump(new_to_json_two, file, sort_keys=True, indent=2, ensure_ascii=False)
        new_to_json_one = dict()
        for key in list(self.to_json_prefix_one.keys()):
            new_to_json_one[key] = []
            sums = 0
            for mini_key in list(self.to_json_prefix_one[key].keys()):
                sums += self.to_json_prefix_one[key][mini_key]
            for mini_key in list(self.to_json_prefix_one[key].keys()):
                new_to_json_one[key].append((mini_key,
                                             round(self.to_json_prefix_one[key][mini_key] / sums, 8)))
        with open('dictionary_prefix_one.json', 'w') as file:
            json.dump(new_to_json_one, file, sort_keys=True, indent=2, ensure_ascii=False)


def createParser():
    # создание парсера
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir",
                        help="path to the directory containing the collection of documents", default="data")
    parser.add_argument("-u", "--use_english",
                        help="flag to count english words", action="store_true")
    parser.add_argument("-e", "--encoding",
                        help="encoding for reading and writing files", default="ANSI")
    return parser


def main():
    parser = createParser()
    args = parser.parse_args()
    education = Education(args.input_dir, args.use_english, args.encoding)


if __name__ == '__main__':
    main()
