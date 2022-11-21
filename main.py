import pickle
import telebot
from telebot import types
from excel import Starting
from PSD import text

driver = []
info_save = []
number = 0
quick_list_of_addresses = []
registr = []
attempts = {1234: 3}
token = text[1]
password = text[2]


def main():
    bot = telebot.TeleBot(token)
    print("\033[40m       \033[1m\033[37mThe bot is being launched")
    try:
        with open("data_number", "rb") as fp:
            number = pickle.load(fp)
            print("\033[40m\033[1m\033[32mthe data_number file has been successfully shipped")
    except FileNotFoundError:
        print("\033[40m\033[1m\033[31mUnable to open the file data_number")

    try:
        with open("data_info", "rb") as fp:
            info_save = pickle.load(fp)
            x = Starting(lin=info_save, num=number)
            x.update()
            print("\033[40m\033[1m\033[32mthe data_info file has been successfully shipped")
    except FileNotFoundError:
        print("\033[40m\033[1m\033[31mUnable to open the file data_info")

    def registr_save(message):
        if message.from_user.id in attempts:
            if attempts[message.from_user.id] == 3:
                bot.send_message(message.chat.id, f'Вы заблокированы превышено кол-во ввода пароля')
            elif password == message.text:
                registr.append(message.from_user.id)
                bot.send_message(message.chat.id, f'Пароль введен верно')
            else:
                if message.from_user.id in attempts:
                    attempts[message.from_user.id] += 1
                    bot.send_message(message.chat.id, f'Неверный пароль\nОсталось попыток {attempts[message.from_user.id]}/3')
                else:
                    attempts[message.from_user.id] = 1
                    bot.send_message(message.chat.id, f'Неверный пароль\nОсталось попыток {attempts[message.from_user.id]}/3')
        elif message.from_user.id not in attempts:
            attempts[message.from_user.id] = 0
            if password == message.text:
                registr.append(message.from_user.id)
                bot.send_message(message.chat.id, f'Пароль введен верно')
            else:
                if message.from_user.id in attempts:
                    attempts[message.from_user.id] += 1
                    bot.send_message(message.chat.id, f'Неверный пароль\nОсталось попыток {attempts[message.from_user.id]}/3')
                else:
                    attempts[message.from_user.id] = 1
                    bot.send_message(message.chat.id, f'Неверный пароль\nОсталось попыток {attempts[message.from_user.id]}/3')

    def start_menu(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить заказ")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

    # старт бота добавление кнопок
    @bot.message_handler(commands=['start'])
    def button_message(message):
        start_menu(message=message)
        bot.send_message(message.chat.id, text[0])

    # вывод команд
    @bot.message_handler(commands=['help'])
    def button_message(message):
        if message.from_user.id in registr:
            bot.send_message(message.chat.id, text[3])
        else:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)

    @bot.message_handler(commands=['change_password'])
    def button_message(message):
        if message.from_user.id not in registr:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)
        else:
            mesg = bot.send_message(message.chat.id, f'Введите новый пароль')
            bot.register_next_step_handler(mesg, change_password)

    def change_password(message):
        global trywoiu
        trywoiu = message.text
        bot.send_message(message.chat.id, f'пароль изменен')

    @bot.message_handler(commands=['account_recovery'])
    def button_message(message):
        if message.from_user.id in registr:
            mesg = bot.send_message(message.chat.id, f'Введите ID из следуйщего списка кого хотите восстановить')
            for i in attempts:
                if attempts[i] == 3:
                    bot.send_message(message.chat.id, i)
            bot.register_next_step_handler(mesg, account_recovery)
        else:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)

    def account_recovery(message):
        if message.text.isdigit():
            if int(message.text) not in attempts:
                bot.send_message(message.chat.id, f'Такого ID нету')
            elif int(message.text) in attempts:
                attempts[int(message.text)] = 0
                bot.send_message(message.chat.id, f'У пользователя обнулялись попытки')
        else:
            bot.send_message(message.chat.id, f'Некорректный  ввод ID')

    # удаление всех добавленных элементов
    @bot.message_handler(commands=['delet_all'])
    def button_message(message):
        if message.from_user.id in registr:
            global number, info_save
            with open("data_info", "wb") as f:
                pickle.dump([], f)
            with open("data_number", "wb") as f:
                pickle.dump(0, f)
            info_save.clear()
            number = 0
            x = Starting(lin=info_save, num=number)
            x.update()
            bot.send_message(message.chat.id, f'Таблица удалена')
        else:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)

    # bot.send_document(message.chat.id,f)
    @bot.message_handler(commands=['unloading_melons_excel'])
    def unloading_melons_excel(message):
        if message.from_user.id in registr:
            x = Starting(lin=info_save, num=number)
            x.update()
            f = open("taxi.xlsx", "rb")
            bot.send_document(message.chat.id, f)
        else:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)

    # удаление элемента по номеру
    @bot.message_handler(commands=['delet_number'])
    def delet_number(message):
        if message.from_user.id in registr:
            mesg = bot.send_message(message.chat.id, f'Введите номер ряда для удаления')
            bot.register_next_step_handler(mesg, del_nuber)
        else:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)

    def del_nuber(message):
        global number, info_save
        a = 0
        a1 = int(message.text)
        a2 = []
        if a1 <= number:
            for i in range((a1-1)):
                a += 5
            for i in range(5):
                if i == 0:
                    a2.append(i+a+1)
                if i == 4:
                    a2.append(i+a+1)
            del info_save[a2[0]-1:a2[1]]
            number -= 1
        else:
            bot.send_message(message.chat.id, f'Такого ряда нету')
        with open("data_info", "wb") as f:
            pickle.dump(info_save, f)
        with open("data_number", "wb") as f:
            pickle.dump(number, f)
        x = Starting(lin=info_save, num=number)
        x.update()

    def info(message, num):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        a = 0
        save = []
        for i in range(number):
            for i in range(5+a):
                if i == num+a:
                    save.append(info_save[i])
            a += 5
        btn1 = types.KeyboardButton("information is missing")
        btn2 = types.KeyboardButton(f"information is missing")
        btn3 = types.KeyboardButton(f"information is missing")
        btn4 = types.KeyboardButton(f"information is missing")
        if 0 < len(list(reversed(save))):
            btn1 = types.KeyboardButton(f"{list(reversed(save))[0]}")
        if 1 < len(list(reversed(save))):
            btn2 = types.KeyboardButton(f"{list(reversed(save))[1]}")
        if 2 < len(list(reversed(save))):
            btn3 = types.KeyboardButton(f"{list(reversed(save))[2]}")
        if 3 < len(list(reversed(save))):
            btn4 = types.KeyboardButton(f"{list(reversed(save))[3]}")

        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, text="info", reply_markup=markup)

    # добавление времени
    def time_save(message):
        info_save.append(text)
        mesg = bot.send_message(message.chat.id, f'Введите водителя')
        bot.register_next_step_handler(mesg, driver_save)

    # добавление водителя
    def driver_save(message):
        info_save.append(f"{message.text}".replace("/", ''))
        mesg = bot.send_message(message.chat.id, f'Введите имя пассажира')
        bot.register_next_step_handler(mesg, passenger_name_save)

    # добавление пассажира
    def passenger_name_save(message):
        info_save.append(message.text)
        mesg = bot.send_message(message.chat.id, f'Введите пункт отправления')
        info(message=message, num=3)
        bot.register_next_step_handler(mesg, where_to_go_save)

    # добавление адрес куда ехать
    def where_to_go_save(message):
        info_save.append(message.text)
        mesg = bot.send_message(message.chat.id, f'Введите пункт назначения')
        info(message=message, num=4)
        bot.register_next_step_handler(mesg, save)

    # добавление пункта назначения
    def save(message):
        global number, info_save
        number += 1
        info_save.append(message.text)
        # save info and number
        with open("data_info", "wb") as f:
            pickle.dump(info_save, f)
        with open("data_number", "wb") as f:
            pickle.dump(number, f)
        bot.send_message(message.chat.id, f'Заказ сохранён')
        x = Starting(lin=info_save, num=number)
        x.update()
        start_menu(message=message)

    @bot.message_handler(content_types='text')
    def message_reply(message):
        if message.from_user.id not in registr:
            mesg = bot.send_message(message.chat.id, f'Введите пароль')
            bot.register_next_step_handler(mesg, registr_save)
        else:
            if message.text == "Добавить заказ":
                mesg = bot.send_message(message.chat.id, 'Введите время')
                bot.register_next_step_handler(mesg, time_save)

    print("\033[40m\033[1m\033[37mThe bot has been successfully launched.")
    print("     \033[40m\033[1m\033[32mThe bot is ready to work")
    bot.polling()


if __name__ == '__main__':
    main()
