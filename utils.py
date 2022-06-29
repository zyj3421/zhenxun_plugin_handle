import random
from io import BytesIO
from utils.http_utils import AsyncHttpx
from configs.path_config import TEXT_PATH, FONT_PATH
from typing import List, Tuple
from pypinyin import pinyin, Style
from PIL import ImageFont
from PIL.Image import Image as IMG
from PIL.ImageFont import FreeTypeFont
from services.log import logger

handle_txt_path = TEXT_PATH / "handle"
idiom_path = handle_txt_path / "idioms.txt"
all_idiom_path = handle_txt_path / "all_idioms.txt"
handle_txt_path.mkdir(exist_ok=True, parents=True)


def legal_idiom(idiom: str) -> bool:
    with all_idiom_path.open("r", encoding="utf-8") as f:
        while True:
            line = f.readline().strip()
            if idiom == line:
                return True
            if len(line) == 0:
                break
        return False


async def random_idiom() -> str:
    if not all_idiom_path.exists():
        # 参考以下词库，取4字成语去重合并
        # https://raw.githubusercontent.com/antfu/handle/main/src/data/idioms.txt
        # https://raw.githubusercontent.com/fighting41love/funNLP/master/data/%E6%88%90%E8%AF%AD%E8%AF%8D%E5%BA%93/ChengYu_Corpus%EF%BC%885W%EF%BC%89.txt
        # https://raw.githubusercontent.com/pwxcoo/chinese-xinhua/master/data/idiom.json
        # https://raw.githubusercontent.com/antfu/handle/main/src/data/polyphones.json
        url = "https://ghproxy.com/https://raw.githubusercontent.com/antfu/handle/main/src/data/idioms.txt"
        try:
            await AsyncHttpx.download_file(url, all_idiom_path)
        except Exception as e:
            logger.warning(f"Error downloading {url}: {e}")
    if not idiom_path.exists():
        url = "https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-handle/main/nonebot_plugin_handle/resources/data/idioms.txt"
        try:
            await AsyncHttpx.download_file(url, idiom_path)
        except Exception as e:
            logger.warning(f"Error downloading {url}: {e}")
    with idiom_path.open("r", encoding="utf-8") as f:
        return random.choice(f.readlines()).strip()


# fmt: off
# 声母
INITIALS = ["zh", "z", "y", "x", "w", "t", "sh", "s", "r", "q", "p", "n", "m", "l", "k", "j", "h", "g", "f", "d", "ch",
            "c", "b"]
# 韵母
FINALS = [
    "ün", "üe", "üan", "ü", "uo", "un", "ui", "ue", "uang", "uan", "uai", "ua", "ou", "iu", "iong", "ong", "io", "ing",
    "in", "ie", "iao", "iang", "ian", "ia", "er", "eng", "en", "ei", "ao", "ang", "an", "ai", "u", "o", "i", "e", "a"
]


# fmt: on


def get_pinyin(idiom: str) -> List[Tuple[str, str, str]]:
    pys = pinyin(idiom, style=Style.TONE3, v_to_u=True)
    results = []
    for p in pys:
        py = p[0]
        if py[-1].isdigit():
            tone = py[-1]
            py = py[:-1]
        else:
            tone = ""
        initial = ""
        for i in INITIALS:
            if py.startswith(i):
                initial = i
                break
        final = ""
        for f in FINALS:
            if py.endswith(f):
                final = f
                break
        results.append((initial, final, tone))  # 声母，韵母，声调
    return results


def save_jpg(frame: IMG) -> BytesIO:
    output = BytesIO()
    frame = frame.convert("RGB")
    frame.save(output, format="jpeg")
    return output


async def load_font(name: str, fontsize: int) -> FreeTypeFont:
    tff_path = FONT_PATH / name
    if not tff_path.exists():
        try:
            url = "https://raw.githubusercontent.com/noneplugin/nonebot-plugin-handle/main/nonebot_plugin_handle/resources/fonts/{}".format(
                name)
            await AsyncHttpx.download_file(url, tff_path)
        except:
            url = "https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-handle/main/nonebot_plugin_handle/resources/fonts/{}".format(
                name)
            await AsyncHttpx.download_file(url, tff_path)
    return ImageFont.truetype(str(tff_path), fontsize, encoding="utf-8")
