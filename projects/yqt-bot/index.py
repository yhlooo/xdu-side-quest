"""SCF 函数的入口
"""

import base64
from io import BytesIO

from conf.settings import WORKPIECES
from log import logging
from screenshot import generate_screenshot, upload_yqt_screenshot
from submit_to_yqt import submit_to_yqt


logger = logging.getLogger('yqt_bot')


def main_handler(event, _):

    # 定时触发，填报疫情通
    if event.get('Type') == 'Timer' and event.get('TriggerName') == 'submit_to_yqt':
        # [总数, 成功数]
        count = [0, 0]

        for item in WORKPIECES:
            if 'submit_to_yqt' in item['actions']:
                try:
                    count[0] += 1
                    submit_to_yqt(item['stu_id'], item['passwd'])
                    count[1] += 1
                except ValueError as e:
                    if str(e) == '今天已经填报疫情通，不能重复填报':
                        logger.warning(f'{item["name"]} 今天已经填报疫情通，已忽略')
                        count[1] += 1
                    else:
                        raise e
                except Exception as e:
                    logger.warning(f'{item["name"]} 填报疫情通失败，已忽略，请手动填报。错误信息：{e}')

        summary_msg = f'填报疫情通完成（{count[1]}/{count[0]}）'
        logger.info(summary_msg)
        return summary_msg

    # 定时触发，上传截图
    elif event.get('Type') == 'Timer' and event.get('TriggerName') == 'upload_screenshot':
        # [总数, 成功数]
        count = [0, 0]

        for item in WORKPIECES:
            if 'upload_screenshot' in item['actions']:
                try:
                    count[0] += 1
                    upload_yqt_screenshot(name=item['name'], stu_id=item['stu_id'], dorm=item['dorm'])
                    count[1] += 1
                except Exception as e:
                    logger.warning(f'{item["name"]} 截图上传失败，已忽略，请手动上传，错误信息：{e}')

        summary_msg = f'上传截图完成（{count[1]}/{count[0]}）'
        logger.info(summary_msg)
        return summary_msg

    # API 网关触发，发送定位页
    elif 'queryString' in event and 'gps' in event['queryString']:
        with open('get_geo_api_info.html', 'rt', encoding='utf-8') as fp:
            gps_page = fp.read()
        return {
            'body': gps_page,
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'isBase64Encoded': False
        }

    # API 网关触发，生成疫情通截图
    elif 'queryString' in event:

        name = event['queryString'].get('name')
        stu_id = event['queryString'].get('stu_id')
        if not name or not stu_id:
            return {
                'body': '请求参数 `name` 和 `stu_id` 必须提供',
                'statusCode': 400,
                'headers': {'Content-Type': 'text/plain'},
                'isBase64Encoded': False
            }

        date = event['queryString'].get('date')
        shot_time = event['queryString'].get('time')
        battery = event['queryString'].get('battery')

        name = name[:6]
        stu_id = stu_id[:11]
        date = date[:10] if date else None
        shot_time = shot_time[:5] if shot_time else None
        try:
            battery = int(battery) if 10 <= int(battery) <= 99 else None
        except (TypeError, ValueError):
            battery = None

        img = generate_screenshot(name, stu_id, date, shot_time, battery)
        fp = BytesIO()
        img.save(fp, format='png')
        img.close()

        return {
            'body': base64.standard_b64encode(fp.getvalue()).decode(),
            'statusCode': 200,
            'headers': {'Content-Type': 'image/png'},
            'isBase64Encoded': True
        }

    else:
        raise RuntimeError('不能理解的触发方式')
