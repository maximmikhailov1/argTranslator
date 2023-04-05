import requests
import argparse
from bs4 import BeautifulSoup


def translate(f, language_to_translate_to):
    soup = None
    try:
        r = requests.get(
            f'https://context.reverso.net/translation/{languages_enum[language_to_translate_from - 1][1].lower()}'
            '-'
            f'{languages_enum[language_to_translate_to - 1][1].lower()}/{word_to_translate}',
            headers={'User-Agent': 'Mozilla/5.0'})
        while r.status_code != 200:
            r = requests.get('https://context.reverso.net/translation/'
                             f'{languages_enum[language_to_translate_from - 1][1].lower()}'
                             '-'
                             f'{languages_enum[language_to_translate_to - 1][1].lower()}/{word_to_translate}',
                             headers={'User-Agent': 'Mozilla/5.0'})

        soup = BeautifulSoup(r.content, 'html.parser')
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
    print(type(soup))
    f.write(f'{languages_enum[language_to_translate_to - 1][1]} Translations:\n')
    print(f'{languages_enum[language_to_translate_to - 1][1]} Translations:')
    translations = list([i.text for i in soup.findAll('span', {'class': 'display-term'})])
    if not translations:
        print(f"Sorry, unable to find {args.word}")
    for translation in translations:
        f.write(translation+'\n')
        print(translation)
    f.write(f'\n{languages_enum[language_to_translate_to - 1][1]} Examples:')
    print(f'\n{languages_enum[language_to_translate_to - 1][1]} Examples:')
    if language_to_translate_to != 1 and language_to_translate_to != 6:
        examples_ltr = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'src ltr'})])
        examples_ltf = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'trg ltr'})])
    elif language_to_translate_to == 1:
        examples_ltr = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'src ltr'})])
        examples_ltf = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'trg rtl arabic'})])
    elif language_to_translate_to == 6:
        examples_ltr = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'src ltr'})])
        examples_ltf = list([i.text.rstrip('\n', ).lstrip('\n\r\n\t').strip() for i in
                             soup.findAll('div', {'class': 'trg rtl'})])
    examples = []
    for a, b in zip(examples_ltr, examples_ltf):
        print(f'{a}\n{b}\n')
        f.write(f'\n{a}\n{b}\n')
    f.write('\n')



languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
             'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian',
             'Turkish']
languages_enum = list(enumerate(languages, start=1))

print('Hello, welcome to the translator.\nTranslator supports:')
for i, language in languages_enum:
    print(i, '. ', language)

parser = argparse.ArgumentParser()
parser.add_argument('language_to_translate_from')
parser.add_argument('language_to_translate_to')
parser.add_argument('word')

args = parser.parse_args()

lttf = None # language to translate from
lttt = None #                       to

for i, language in languages_enum:
    if args.language_to_translate_from.capitalize() == language:
        lttf = i
    elif args.language_to_translate_to.capitalize() == language:
        lttt = i

if lttf is None:
    print(f"Sorry, the program doesn't support {args.language_to_translate_from}")
    exit()
if lttt is None:
    if args.language_to_translate_to != 'all':
        print(f"Sorry, the program doesn't support {args.language_to_translate_to}")
        exit()
    else:
        lttt = 0

language_to_translate_from = lttf
language_to_translate_to = lttt
word_to_translate = args.word


with open(f'{word_to_translate}.txt', 'w', encoding='utf-8') as f:
    if language_to_translate_to != 0:
        translate(f, language_to_translate_to)
    else:
        for i, language in languages_enum:
            if i != language_to_translate_from:
                translate(f, i)


