import io
import math
import re
from telethon import Button, custom, events
from userbot import CMD_LIST
from . import telealive


BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if query.startswith("**SPARKZZZ") and event.query.user_id == bot.uid:
            buttons = [
                (
                    custom.Button.inline("Stats", data="stats"),
                    Button.url("Repo", "https://github.com/vishnu175/SPARKZZZ"),
                )
            ]
            result = builder.article(
                # catpic,
                title="Alive sparkzzz",
                # force_document = False,
                text=query,
                buttons=buttons,
            )
            await event.answer([result] if result else None)
        elif event.query.user_id == bot.uid and query.startswith("Userbot"):
            rev_text = query[::-1]
            buttons = paginate_help(0, CMD_LIST, "helpme")
            result = builder.article(
                "© Userbot Help",
                text="{}\nCurrently Loaded Plugins: {}".format(query, len(CMD_LIST)),
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
        elif event.query.user_id == bot.uid and query.startswith("Inline buttons"):
            markdown_note = query[14:]
            prev = 0
            note_data = ""
            buttons = []
            for match in BTN_URL_REGEX.finditer(markdown_note):
                # Check if btnurl is escaped
                n_escapes = 0
                to_check = match.start(1) - 1
                while to_check > 0 and markdown_note[to_check] == "\\":
                    n_escapes += 1
                    to_check -= 1
                # if even, not escaped -> create button
                if n_escapes % 2 == 0:
                    # create a thruple with button label, url, and newline
                    # status
                    buttons.append(
                        (match.group(2), match.group(3), bool(match.group(4)))
                    )
                    note_data += markdown_note[prev : match.start(1)]
                    prev = match.end(1)
                # if odd, escaped -> move along
                else:
                    note_data += markdown_note[prev:to_check]
                    prev = match.start(1) - 1
            else:
                note_data += markdown_note[prev:]
            message_text = note_data.strip()
            tl_ib_buttons = ibuild_keyboard(buttons)
            result = builder.article(
                title="Inline creator",
                text=message_text,
                buttons=tl_ib_buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Aary bas kar Bhai !! Tab se dabate jaa rha h, Khudka bot bana!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = (
                "Aary bas kar Bhai !! Tab se dabate jaa rha h, Khudka bot bana!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"secret_(.+?)_(.+)")))
    async def on_plug_in_callback_query_handler(event):
        userid = event.pattern_match.group(1)
        ids = [int(userid), bot.uid]
        if event.query.user_id in ids:
            encrypted_tcxt = event.pattern_match.group(2)
            reply_pop_up_alert = encrypted_tcxt
        else:
            reply_pop_up_alert = "You little shit, why are you looking at this ? Go away and do your own work,idiot"

        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = ""
            try:
                for i in CMD_LIST[plugin_name]:
                    help_string += i
                    help_string += "\n"
            except BaseException:
                pass
            if help_string == "":
                reply_pop_up_alert = "{} is useless".format(plugin_name)
            else:
                reply_pop_up_alert = help_string
            reply_pop_up_alert += (
                "Use .unload {} to remove this plugin ©SPARKZZZ userbot".format(plugin_name)
            )
            try:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            except BaseException:
                # https://github.com/Dark-Princ3/X-tra-Telegram/commit/275fd0ec26b284d042bf56de325472e088e6f364#diff-2b2df8998ff11b6c15893b2c8d5d6af3
                with io.BytesIO(str.encode(reply_pop_up_alert)) as out_file:
                    out_file.name = "{}.txt".format(plugin_name)
                    await borg.send_file(
                        event.chat_id,
                        out_file,
                        force_document=True,
                        allow_cache=False,
                        caption=plugin_name,
                    )
        else:
            reply_pop_up_alert = (
                "Aary bas kar Bhai !! Tab se dabate jaa rha h, Khudka bot bana!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit("menu closed")
        else:
            reply_pop_up_alert = (
                "Aary bas kar Bhai !! Tab se dabate jaa rha h, Khudka bot bana!"
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats")))
    async def on_plug_in_callback_query_handler(event):
        statstext = await catalive()
        reply_pop_up_alert = statstext
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = Config.NO_OF_INLINE_ROWS
    number_of_cols = Config.NO_OF_INLINE_COLUMNS
    helpable_plugins = [p for p in loaded_plugins if not p.startswith("_")]
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{} {} {}".format(
                Config.INLINE_EMOJI, x, Config.INLINE_EMOJI
            ),
            data="us_plugin_{}".format(x),
        )
        for x in helpable_plugins
    ]
    if number_of_cols == 1:
        pairs = list(zip(modules[::number_of_cols]))
    elif number_of_cols == 2:
        pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    else:
        pairs = list(
            zip(
                modules[::number_of_cols],
                modules[1::number_of_cols],
                modules[2::number_of_cols],
            )
        )
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    elif len(modules) % number_of_cols == 2:
        pairs.append((modules[-2], modules[-1]))
    max_num_pages = math.ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "👈Previous", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline("⚡Close⚡", data="close"),
                custom.Button.inline(
                    "Next👉", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb
