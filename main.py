import string
from collections import Counter
import re


Alfavit = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

#удаление дубликатов букв из алфавита
def remove_dup_alfa(str, alfavit):
    for i in alfavit:
        for j in str:
            if i == j:
                alfavit = alfavit.replace(i, '')
    return alfavit

#проверка на русские слова
def cont_rus_let(str_check):
    flag = False

    for i in str_check:
        if ord('а') <= ord(i) <= ord('я'):
            flag = True
        else:
            flag = False
            break

    if flag:
        return True
    else:
        return False


def uniq(s):
    return len(s) == len(set(s))


def caesar(key, index, text):
    new_alfavit = remove_dup_alfa(key, Alfavit)
    new_alfavit = new_alfavit[-int(index):] + key + new_alfavit[:-int(index)]

    message = []

    for character in text:
        try:
            index = Alfavit.index(character)
            character = new_alfavit[index]
            message.append(character)
        except ValueError:
            message.append(character)

    return ''.join(message)


#main_main_main_main_main_main_main_main_main_main_main_main_main_
def enter_key():
    print("ENTER THE KEY:")
    f_key = input().lower()

    while (not (uniq(f_key))) or (len(f_key) < 0 or len(f_key) > 32) or not cont_rus_let(f_key):
        print("WRONG KEY, TRY AGAIN")
        f_key = input().lower()

    return f_key


def enter_index():
    print("ENTER THE SHIFT INDEX:")
    f_index = input()

    while not f_index.isdigit() or (int(f_index) < 0 or int(f_index) > 32):
        print("WRONG INDEX, TRY AGAIN")
        f_index = input()

    return f_index

#удаление спец символов
def symbols_remove(text, chars):
    return "".join([ch for ch in text if ch not in chars])


symbols_spec = string.punctuation + '\n\xa0«»\t—… '
symbols_spec_2 = "!\"#$%&'()*+-./:;<=>?@[\]^_`{|}~" + "\xa0,\xa0"

letters_freq = 'оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё'

while 1:
    print("\n / CHOOSE ONE OPTION BELOW / \n\n 1) ROMAN CHAPTER ENCRYPTION AND DECRYPTION \n 2) CLOSE PROGRAM \n \n ENTER A NUMBER:")
    number = input()

    if number.isdigit():
        number = int(number)

    # Шифрация и дешифрация части романа
    if number == 1:
            print("/ ROMAN CHAPTER ENCRYPTION AND DECRYPTION /")
            # ввод ключа
            key = enter_key()
            # ввод идекса сдвига
            index = enter_index()
            # открытие файла для чтения
            with open('texts/roman_full.txt', 'rt') as roman_original:
            #with open('texts/roman_part.txt', 'rt', encoding="utf-8") as roman_original:
                roman = roman_original.read()
                # удаление нерусских символов
                roman = (re.sub('[a-z|A-Z]', '', roman)).lower()

                # удаление специальных символов
                roman_2 = symbols_remove(roman, symbols_spec)
                # удаление чисел
                roman_2 = symbols_remove(roman, string.digits)
                # подсчёт 10 самых популярных биграм в оригинальном тексте
                bigrams = Counter(re.findall(r'(?=([а-я]{2}))', roman_2)).most_common(10)
                bigrams_list = str(bigrams)
                bigrams_list = symbols_remove(bigrams_list, string.digits)
                bigrams_list = symbols_remove(bigrams_list, symbols_spec_2).split()
                print("BIGRAMS IN THE ORIGINAL TEXT:\n ", bigrams, "\n ", bigrams_list)


            with open('texts/roman_encrypt.txt', 'w') as roman_encrypted:
                # запись в файл зашифрованного цезарем текста
                roman_encrypted.write(caesar(key, index, roman)) #roman_2

            new_text = caesar(key, index, roman) #roman_2
            # подсчёт букв по популярности
            letters_decr = Counter("".join([ch for ch in new_text if ch in Alfavit]))

            message_1 = []

            letters_list = str(letters_decr)
            letters_list = symbols_remove(letters_list, symbols_spec)
            letters_list = symbols_remove(letters_list, string.digits)
            letters_list = letters_list[7:]

            with open('texts/roman_decrypt.txt', 'wt') as roman_decrypted:
            #запись в файл расшифрованного цезарем текста
                for char_new in new_text:
                    try:
                        index_new = letters_list.index(char_new)
                        new_char = letters_freq[index_new]
                        message_1.append(new_char)
                    except ValueError:
                        message_1.append(char_new)
                roman_decrypted.write(''.join(message_1))

            letters_freq_update = letters_freq
            letters_freq_update = list(letters_freq_update)

            with open('texts/roman_decrypt.txt', 'rt') as roman_decrypted_2:
                bigrams_new = roman_decrypted_2.read()
                # подсчёт 10 популярных биграм в расщиврованном тексте
                bigrams_new = Counter(re.findall(r'(?=([а-я]{2}))', bigrams_new)).most_common(10)
                #print("BIGRAMS IN THE DECRYPTED TEXT: ")
                letters_list_2 = str(bigrams_new)
                letters_list_2 = symbols_remove(letters_list_2, string.digits)
                letters_list_2 = symbols_remove(letters_list_2, symbols_spec_2).split()
                print("BIGRAMS IN THE DECRYPTED TEXT:\n ", letters_list_2)


            for a in range(len(letters_list_2)):
                if letters_list_2[a] != bigrams_list[a]:
                    x = letters_list_2[a]
                    y = bigrams_list[a]
                    # нахождение и изменение неправильного символа
                    if x[0] != y[0]:
                        index_1_1 = letters_freq.index(x[0])
                        letters_freq_update[index_1_1] = y[0]
                        index_1_2 = letters_freq.index(y[0])
                        letters_freq_update[index_1_2] = x[0]

                    if x[1] != y[1]:
                        index_2_1 = letters_freq.index(x[1])
                        letters_freq_update[index_2_1] = y[1]
                        index_2_2 = letters_freq.index(x[1])
                        letters_freq_update[index_2_2] = y[1]

            print("\nALPHABET BEFORE BIGRAM ANALYSIS:\n ", (list(letters_freq)))
            print("ALPHABET AFTER BIGRAM ANALYSIS:\n ", (letters_freq_update))

            open_decrypt = open('texts/roman_decrypt.txt', 'r')
            o_p_d = open_decrypt.read()
            message_2 = []
            # расшифровка текста с использованием биграм
            with open('texts/roman_decrypt_upgrade.txt', 'wt') as roman_decrypted_3:
                for char in o_p_d:
                    try:
                        index_1_1 = letters_freq.index(char)
                        index_2_1 = letters_freq_update.index(char)

                        if index_1_1 != index_2_1:
                            character2 = letters_freq_update[index_1_1]
                            message_2.append(character2)

                        else:
                            message_2.append(char)

                    except ValueError:
                        message_2.append(char)

                roman_decrypted_3.write(''.join(message_2))

            roman_original.close()
            roman_encrypted.close()
            roman_decrypted.close()
            roman_decrypted_2.close()
            roman_decrypted_3.close()

    # завершение программы
    elif number == 2:
        print("PROGRAM IS FINISHED")
        break