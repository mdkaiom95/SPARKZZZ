import os
from re import match
from bitlyshortener import Shortener
from userbot.utils import admin_cmd

BIT_TOKEN = os.environ.get("BITLY_TOKEN", None)
BOTLOG = True


@borg.on(admin_cmd(outgoing=True, pattern=r"bitly(?: |$)(.*)"))
async def shortener(short):
    """
    Shorten link using bit.ly API
    """
    if BIT_TOKEN is not None:
        token = [f"{BIT_TOKEN}"]
        reply = await short.get_reply_message()
        message = short.pattern_match.group(1)
        if message:
            pass
        elif reply:
            message = reply.text
        else:
            await short.edit("`Error! No URL given!`")
            return
        link_match = match(r"\bhttps?://.*\.\S+", message)
        if not link_match:
            await short.edit(
                "`Error! Please provide valid url!`\nExample: https://google.com"
            )
            return
        urls = [f"{message}"]
        bitly = Shortener(tokens=token, max_cache_size=8192)
        raw_output = bitly.shorten_urls(urls)
        string_output = f"{raw_output}"
        output = string_output.replace("['", "").replace("']", "")
        await short.edit(
            f"`Your link shortened successfully!`\nHere is your link {output}"
        )
        if BOTLOG:
            await short.client.send_message(
                PRIVATE_GROUP_ID, f"`#SHORTLINK \nThis Your Link!`\n {output}"
            )
    else:
        await short.edit(
            "Set bit.ly API token first\nGet it from [here](https://bitly.com/a/sign_up)"
        )
