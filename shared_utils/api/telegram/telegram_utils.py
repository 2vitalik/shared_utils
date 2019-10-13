import telegram


def process_keyboard(keyboard):
    return telegram.ReplyKeyboardMarkup([
        [telegram.KeyboardButton(button) for button in line]
        for line in keyboard
    ], resize_keyboard=True)


def process_buttons(buttons):
    if not buttons:
        return None
    return telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(button, callback_data=callback_data)
         for button, callback_data in line]  # todo: case without tuple
        for line in buttons
    ])


def send(bot, chat_id, text, keyboard=None, buttons=None):
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    if keyboard:
        reply_markup = process_keyboard(keyboard)
    elif buttons:
        reply_markup = process_buttons(buttons)
    else:
        reply_markup = None

    return bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True,
    )


def edit(bot, chat_id, message_id, text, buttons=None):
    reply_markup = None
    if buttons:
        reply_markup = process_buttons(buttons)

    return bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=reply_markup,
        parse_mode=telegram.ParseMode.HTML,
        disable_web_page_preview=True,
    )


def delete(bot, chat_id, msg_id):
    bot.delete_message(chat_id, msg_id)
