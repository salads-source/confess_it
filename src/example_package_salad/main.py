#!/usr/bin/env python
from dotenv import load_dotenv
import logging
import os
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHANNEL_ID = '@confessit_test'  # test channel

QUESTION, OPTION = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hello there! Start by sending /poll to create a custom poll and send it to the main channel:D"
    )


async def create_poll_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your poll question.")
    return QUESTION


async def create_poll_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for the poll options."""
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Enter the first option.")
    return OPTION


async def create_poll_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Processes each option and asks for the next one until all options are provided."""
    options = context.user_data.setdefault('options', [])
    text = update.message.text

    if text == "/done":
        return await create_poll_done(update, context)

    options.append(text)

    if len(options) < 10:
        await update.message.reply_text("Enter the next option, or type /done if you're finished.")
        return OPTION
    else:
        await update.message.reply_text("Maximum number of options reached (10). Type /done to finish.")
        return OPTION


async def create_poll_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Creates the poll and sends it to the channel."""
    options = context.user_data.setdefault('options', [])
    if len(options) < 2:
        await update.message.reply_text("At least two options are required to create a poll.")
        return OPTION

    question = context.user_data['question']
    options = context.user_data['options']

    try:
        await context.bot.send_poll(
            chat_id=CHANNEL_ID,
            question=question,
            options=options,
            is_anonymous=True,
            allows_multiple_answers=False
        )
        await update.message.reply_text('Poll created and forwarded to the channel.')
    except Exception as e:
        logger.error(f"Error in create_poll: {e}")
        await update.message.reply_text('Failed to create poll.')

    context.user_data.clear()
    return ConversationHandler.END


async def create_poll_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the poll creation."""
    await update.message.reply_text('Poll creation cancelled.')
    context.user_data.clear()
    return ConversationHandler.END


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Start by sending /poll to create a poll!")


async def done_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle /done outside of a conversation
    if 'question' not in context.user_data:
        await update.message.reply_text("Please start by creating a poll using the /poll command.")
        return


async def set_commands(application: Application) -> None:
    """Set the bot commands for the menu"""
    commands = [
        BotCommand("start", "Welcome message"),
        BotCommand("poll", "Create a custom poll"),
        BotCommand("help", "Display help message"),
        BotCommand("done", "Finish creating the poll")
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())


def main() -> None:
    load_dotenv('../../.env')
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_handler))

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('poll', create_poll_start)],
        states={
            QUESTION: [MessageHandler(None, create_poll_question)],
            OPTION: [
                MessageHandler(None, create_poll_options),
                CommandHandler('done', create_poll_done),
            ],
        },
        fallbacks=[CommandHandler('done', create_poll_done)],
    )

    application.add_handler(conversation_handler)
    application.add_handler(CommandHandler(
        'done', done_handler))  # Global done handler

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
