import logging

from typing import Tuple, Optional
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram.ext import Updater, CommandHandler, CallbackContext, ChatMemberHandler
from multicolorcaptcha import CaptchaGenerator

CaptchaGen = CaptchaGenerator(2)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

"""COMENZILE BOTULUI"""


def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        "Finnaly there's a BSC token with the same total supply with WebDollar - $WWEBD, and it is available on PanCake swap.\n"
        "\n"
        "The contract address is : 0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc\n"
        "\n"
        "You can check our BSCSCAN here:  https://bscscan.com/token/0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc#tokenAnalytics\n"
        "\n"
        "Also, you can find the actual price of $WWEBD on this site: https://dex.guru/token/0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc-bsc\n"
        "\n"
        "Total supply  of 42BILLION tokens.\n"
        "\n"
        "50% will be burned, starting every 6 months, the rate of doubling would be x2 every time starting from 200 MIL\n"
        "\n"
        "8.1% alocated to developer funds which shall be locked for 2-3 years.\n"
        "\n"
        "2.3% of the funds will be used for various marketing/ growth purposes.\n"
        "\n"
        "Liquidity pool blocked will be blocked at 20 BNB through a trusted service.\n"
        "\n"
        "To get a list of all the commands use /help\n"
        "\n"
        "Everything presented above will be written on a lite/whitepaper in a short time. A website and roadmap will follow soon as well.\n"
        "\n"
        "You can find us on Twitter - https://twitter.com/WWebdollar\n"
        "\n"
        "Also, on telegram - https://t.me/joinchat/Ga8tx6vvHJw4NmM0\n"
        "\n"
        "Discord - https://discord.gg/Y4bhjJsS \n"
    )

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("⚙️ You can run the following commands: \n"
                              "\n"
                              "/buy - How you can buy $WWEBD"
                              "\n"
                              "/price - The price and volume for $WWEBD"
                              "\n"
                              "/staff"
                              "\n"
                              "/tokenomics - Shows the tokenomics  of $WWEBD")

def tokenomics_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Total supply of 42 billion tokens.\n \n 50% of the total supply will be burned, starting every 6 months, the rate of burning would be x2 every time starting from 200 mil. tokens\n \n 8.1% alocated to developer funds which shall be locked for 2-3 years.\n \n 2.3% of the funds will be used for various marketing/ growth purposes.\n \n Liquidity pool blocked will be blocked at 20 BNB through a trusted service.")

def buy_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Buy $WWEBD using Pancake Swap (https://pancakeswap.finance/).\n"
                              " The contract address: 0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc")

def contract_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("The contract address: 0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc")

def staff_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("The full staff is the following :\n"
                              "Founder:\n"
                              "@beliall23\n"
                              "Co-Founder:\n"
                              "@dudor04\n"
                              "Trading-Consult:\n"
                              "@catalinbunea\n"
                              "Community Managers:\n"
                              "@RoyalKend\n"                        
                              "@AretiHil\n"
                              "Coder:\n"
                              "@Leo71299")

def price_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("The price, liquidity and volume can be seen at: https://dex.guru/token/0x0a02b47484d55a0556ba092f1ac56165cf9f1fbc-bsc")

def extract_status_change(
        chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change.
    """
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
            old_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
            new_status
            in [
                ChatMember.MEMBER,
                ChatMember.CREATOR,
                ChatMember.ADMINISTRATOR,
            ]
            or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member

def track_chats(update: Update, context: CallbackContext) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s started the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s", cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    else:
        if not was_member and is_member:
            logger.info("%s added the bot to the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the channel %s", cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


def show_chats(update: Update, context: CallbackContext) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid) for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid) for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    update.effective_message.reply_text(text)


def greet_chat_members(update: Update, context: CallbackContext) -> None:
    """Greets new users in chats and announces when someone leaves"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        update.effective_chat.send_message(
            fr"Welcome {member_name}! Use the following link to get in touch with our bot http://t.me/WrappedWebdollar_bot",
            parse_mode=ParseMode.HTML,
        )



import os
def main() -> None:
    """TOKEN"""
    token = os.environ.get('API_KEY')
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("buy", buy_command))
    dispatcher.add_handler(CommandHandler("price", price_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("contract", contract_command))
    dispatcher.add_handler(CommandHandler("tokenomics", tokenomics_command))
    dispatcher.add_handler(CommandHandler("staff", staff_command))
    dispatcher.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the Bot
    updater.start_polling(allowed_updates=Update.ALL_TYPES)

    updater.idle()


if __name__ == '__main__':
    main()
