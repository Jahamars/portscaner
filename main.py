# main.py

from portscan_v import PortScan
import telebot

bot = telebot.TeleBot('тооооокееееен')

@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите домен или IP-адрес для сканирования :')
    bot.register_next_step_handler(msg, process_input)

def process_input(message):
    user_input = message.text
    bot.send_message(message.chat.id, 'Порт сканируется, ждите...')
    bot.send_message(message.chat.id, '⌛️')

    target = user_input
    port_count = 1000
    scan = PortScan(target, port_count)
    scan.port_rotate()
    print('\r- Выполнено', end='')

    banners = scan.banners_port
    o_port = scan.open_port

    if len(banners) == 0 and len(o_port) == 0:
        bot.send_message(message.chat.id, 'Открытых портов не найдено.')
        msg = bot.send_message(message.chat.id, 'Введите домен или IP-адрес для сканирования :')
        bot.register_next_step_handler(msg, process_input)
        return
    else:
        if target.startswith("http"):
            target_print = target.split("/")[2]
            bot.send_message(message.chat.id, f'\n\nСВОДНАЯ ИНФОРМАЦИЯ ПО ДОМЕНУ (IP): {target_print}\n{"*"*50}')
        else:
            bot.send_message(message.chat.id, f'\n\nСВОДНАЯ ИНФОРМАЦИЯ ПО ДОМЕНУ (IP): {target}\n{"*"*50}')
        for bann in banners:
            bot.send_message(message.chat.id, f'  Порт: {bann:5}  Баннер: {banners[bann]}')
        for o in o_port:
            bot.send_message(message.chat.id, f'  Порт: {o:5}  Сервис: {o_port[o]}')

    msg = bot.send_message(message.chat.id, 'Введите домен или IP-адрес для сканирования :')
    bot.register_next_step_handler(msg, process_input)

bot.polling()
