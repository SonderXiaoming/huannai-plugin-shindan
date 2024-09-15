from typing import List

from pydantic import BaseModel


SHINDANMAKER_COOKIE: str = ""  # shindanmaker 的 cookie
SHOW_MODE = "image"  # 显示模式，image 或 text


class ShindanConfig(BaseModel):
    id: int
    command: str
    title: str


SHINDANMAKER_LIST: List[ShindanConfig] = [
    ShindanConfig(id=162207, command="今天是什么少女",
                  title="你的二次元少女化形象"),
    ShindanConfig(id=917962, command="人设生成", title="人设生成器"),
    ShindanConfig(id=790697, command="中二称号", title="奇妙的中二称号生成器"),
    ShindanConfig(id=587874, command="异世界转生", title="異世界轉生—∩開始的種族∩——"),
    ShindanConfig(id=940824, command="魔法人生", title="魔法人生：我在霍格沃兹读书时发生的两三事"),
    ShindanConfig(id=1075116, command="二次元老婆", title="あなたの二次元での嫁ヒロイン"),
    ShindanConfig(id=400813, command="抽舰娘", title="【艦これ】あ なたの嫁になる艦娘は？"),
    ShindanConfig(id=361845, command="抽高达", title="マイ・ガンダム診断"),
    ShindanConfig(id=595068, command="英灵召唤", title="Fate 英霊召喚"),
    ShindanConfig(id=360578, command="卖萌", title="顔文字作るよ(  ﾟдﾟ )"),
]
