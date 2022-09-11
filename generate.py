import argparse
import os
import json
import random
import numpy as np
from collections import defaultdict
from train import Education

with open('dictionary_prefix_one.json') as file:
    prefix_one = json.load(file)


def createParser():
    # создание парсера
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--first",
                        help="the first word in the generated sequence")
    parser.add_argument("-s", "--second",
                        help="the second word in the generated sequence")
    parser.add_argument("-l", "--length", type=int,
                        help="length of generated sequence", default=5)
    parser.add_argument("-d", "--directory",
                        help="directory for changing the data dictionary")
    parser.add_argument("-u", "--use_english",
                        help="flag to count english words", action="store_true")
    parser.add_argument("-e", "--encoding",
                        help="encoding for reading and writing files", default="ANSI")
    return parser


def genetare_random_word():
    # нахождение случайного слова
    global prefix_one
    return random.choice(list(prefix_one.keys()))


def generate_sequence(first, second, length):
    # генерация самой последовательности
    print(first, second, end=' ')
    first = first.lower()
    with open('dictionary_prefix_one.json') as file_one:
        prefix_one = json.load(file_one)
        with open('dictionary_prefix_two.json') as fire_two:
            prefix_two = json.load(fire_two)
    for ind in range(length - 2):
        word = []
        ver = []
        preff_two = False
        if first + ':' + second in prefix_two:  # пытаемся продолжить префикс длины 2 (вероятность 60%)
            word.extend([i[0] for i in prefix_two[first + ':' + second]])
            ver.extend([i[1] * 0.6 for i in prefix_two[first + ':' + second]])
            preff_two = True
        if second in prefix_one:  # пытаемся продолжить префикс длины 1 (вероятность 35%)
            koeff = 0.35 if preff_two else 0.95
            word.extend([i[0] for i in prefix_one[second]])
            ver.extend([i[1] * koeff for i in prefix_one[second]])
        word.append(genetare_random_word())  # пытаемся продолжить с помощью случайного слова (вероятность 5%)
        ver.append(1 - sum(ver))
        next_word = np.random.choice(word, 1, p=ver)[0]
        if ind != length - 3:
            print(next_word, end=' ')
        else:
            while len(next_word) < 3:  # чтобы последнее слово состояло из трех и более букв
                next_word = genetare_random_word()
            print(next_word + '.')
        first, second = second, next_word


def main():
    parser = createParser()
    args = parser.parse_args()
    if args.directory is not None:
        # изменение словаря с данными
        education = Education(args.directory, args.use_english, args.encoding)
    first, second = args.first, args.second
    if first is None:
        first = genetare_random_word()
    if second is None:
        second = genetare_random_word()
    first = first.capitalize()
    second = second.lower()
    generate_sequence(first, second, args.length)


if __name__ == '__main__':
    main()
