"""与疫情通截图相关的方法
"""

import datetime
import json
import logging
import pytz
import random
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

from conf import settings


logger = logging.getLogger('screenshot')


def generate_screenshot(
        name: str,
        stu_id: str,
        date: str = None,
        shot_time: str = None,
        battery: int = None
) -> Image:
    """生成疫情通截图

    :param name: 姓名
    :param stu_id: 学号
    :param date: 日期（%Y-%m-%d），缺省值是今天
    :param shot_time: 截图时间（%H:%M），缺省值是现在
    :param battery: 电量，两位数， 10-99 ，缺省值随机
    :return: 生成的图片
    """

    now_datetime = datetime.datetime.now(tz=pytz.timezone(settings.TIMEZONE))

    # 日期缺省值
    if date is None:
        date = now_datetime.strftime('%Y-%m-%d')

    # 时间缺省值
    if shot_time is None:
        shot_time = now_datetime.strftime('%H:%M')

    # 电量缺省值是 10-99 的随机整数
    if battery is None:
        battery = random.randint(10, 99)

    logger.info(f'正在生成疫情通截图：{name}， {stu_id} ， {date} ，电量 {battery} ，时间 {shot_time}')

    # 打开模板图片
    template_img = Image.open('./assets/template.png')
    dw = ImageDraw.Draw(template_img)

    # 添加日期、姓名、学号
    form_font = ImageFont.truetype('./assets/msyh.ttc', 43)
    dw.text((92, 1279), date, fill=(20, 20, 20), font=form_font)
    dw.text((92, 1604), name, fill=(20, 20, 20), font=form_font)
    dw.text((92, 1939), stu_id, fill=(20, 20, 20), font=form_font)

    # 添加电池电量、时间
    dw.text((1187, 29), str(battery), fill=(102, 102, 102), font=ImageFont.truetype('./assets/msyh.ttc', 31))
    dw.text((1259, 23), shot_time, fill=(102, 102, 102), font=ImageFont.truetype('./assets/msyh.ttc', 42))

    # 添加提交成功弹窗
    alert_img = Image.open('./assets/alert.png')
    template_img.paste(alert_img, (260, 1460))
    alert_img.close()

    logger.info('截图生成完成.')

    return template_img


def upload_yqt_screenshot(
        name: str,
        stu_id: str,
        dorm: str,
        shot_time: datetime.datetime = None
) -> None:
    """生成并上传疫情通截图

    :param name: 姓名
    :param stu_id: 学号
    :param dorm: 寝室号
    :param shot_time: 截图时间，缺省值是今天 06:00:00 - 08:59:59 的一个随机数
    :return: None
    """

    logger.info(f'准备上传 {name} 的截图')

    # 截图时间缺省值是今天 06:00:00 - 08:59:59 中的一个随机数
    if shot_time is None:
        shot_time = datetime.datetime.now(tz=pytz.timezone(settings.TIMEZONE))
        shot_time = shot_time.replace(
            hour=random.randint(6, 8),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

    # 生成截图
    screenshot_name = shot_time.strftime('Screenshot_%Y%m%d_%H%M%S_com.tencent.mm.png')
    screenshot = generate_screenshot(
        name,
        stu_id,
        date=shot_time.strftime('%Y-%m-%d'),
        shot_time=shot_time.strftime('%H:%M')
    )
    screenshot_fp = BytesIO()
    screenshot.save(screenshot_fp, format='png')
    screenshot.close()

    ret = requests.post(
        settings.YQT_SCREENSHOT_UPLOAD_URL,
        data={
            'name': name,
            'dorm': dorm
        },
        files={
            'photo': (screenshot_name, screenshot_fp.getvalue(), 'image/png')
        }
    )

    try:
        ret_data = json.loads(ret.text)
        if not isinstance(ret_data, dict):
            ret_data = {}
    except json.JSONDecodeError:
        ret_data = {}

    if ret.status_code == 200 and ret_data.get('code') == 0:
        logger.info(f'{name} 的截图上传成功')
    else:
        err_msg = f'{name} 的截图上传失败'
        logger.error(err_msg)
        raise RuntimeError(err_msg)
