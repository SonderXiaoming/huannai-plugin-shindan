import base64
import re
from typing import Optional
from hoshino import Service
import hoshino
from hoshino.typing import HoshinoBot, CQEvent
from .config import SHINDANMAKER_LIST, SHOW_MODE
from .shindanmaker import make_shindan
from nonebot import MessageSegment
sv_help = """
占卜相关功能
【占卜列表】 查看可用占卜
"""
sv = Service("占卜", help_=sv_help)
shindan_dict = {shindan.command: shindan for shindan in SHINDANMAKER_LIST}
img_pattern = r"((?:http|https)://\S+\.(?:jpg|jpeg|png|gif|bmp|webp))"


async def get_user_info(bot: HoshinoBot, event: CQEvent) -> Optional[str]:
    msg = event.message
    qq_id = None
    for msg_seg in msg:
        if msg_seg.type == "at":
            if msg_seg.data["qq"] == "all":
                break
            qq_id = msg_seg.data["qq"]
    if not qq_id:
        if name := event.message.extract_plain_text().strip():
            return name
        else:
            qq_id = event.user_id
    try:
        info = await bot.get_group_member_info(group_id=event.group_id, user_id=qq_id)
        return info["card"] or info["nickname"]
    except Exception:
        return None


@sv.on_fullmatch("占卜帮助")
async def shindan_help(bot: HoshinoBot, ev: CQEvent):
    await bot.send(ev, sv_help)


@sv.on_fullmatch("占卜列表")
async def shindan_list(bot: HoshinoBot, ev: CQEvent):
    if not SHINDANMAKER_LIST:
        await bot.finish(ev, "尚未添加任何占卜")
    msg = "\n".join(
        f"【{shindan.command} + 名字】: {shindan.title}" for shindan in SHINDANMAKER_LIST)
    msg += "\n使用【占卜】+【占卜名称】+【名字】进行占卜，例如【今天是什么少女+名字】不加名字默认聊天昵称"
    await bot.send(ev, msg)


@sv.on_prefix([shindan.command for shindan in SHINDANMAKER_LIST])
async def shindan(bot: HoshinoBot, ev: CQEvent):
    args = ev.raw_message.strip().split()
    command = args[0]
    user_name = await get_user_info(bot, ev)
    if not user_name:
        await bot.finish(ev, "无法获取名字，请加上名字再试")
        return
    shidan_config = shindan_dict[command]
    try:
        res = await make_shindan(shidan_config.id, user_name, SHOW_MODE)
    except Exception:
        hoshino.logger.error(f"占卜出错: {command} {user_name}")
        await bot.finish(ev, "出错了，请稍后再试")
        return

    msg = ""
    if isinstance(res, str):
        for text in re.split(img_pattern, res):
            if re.match(img_pattern, text):
                try:
                    msg += MessageSegment.image(text)
                except Exception:
                    hoshino.logger.warning(f"{text} 下载出错！")
            else:
                msg += text
    else:
        msg = MessageSegment.image(
            f'base64://{base64.b64encode(res).decode()}')
    await bot.send(ev, msg)
