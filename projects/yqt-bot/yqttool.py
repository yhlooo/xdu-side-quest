"""该应用的命令行入口
"""

import argparse

from log import logging
from index import main_handler
from screenshot import generate_screenshot


logger = logging.getLogger('yqt_tool')


def main():
    parser = argparse.ArgumentParser(
        prog='python3 yqttool.py',
        description='疫情通填报、截图生成、截图上传工具'
    )

    parser.add_argument(
        'action',
        type=str, metavar='ACTION',
        choices=('submit_to_yqt', 'upload_screenshot', 'generate_screenshot'),
        help=(
            '执行的操作。 '
            'submit_to_yqt ，根据 conf/settings.py 的配置填报疫情通； '
            'upload_screenshot ，根据 conf/settings.py 的配置上传疫情通截图； '
            'generate_screenshot ，生成疫情通截图。'
        )
    )

    parser.add_argument(
        '-n', '--name',
        type=str, metavar='NAME',
        help='姓名，生成疫情通截图时必填'
    )
    parser.add_argument(
        '-i', '--stu-id',
        type=str, metavar='STU_ID',
        help='学号，生成疫情通截图时必填'
    )
    parser.add_argument(
        '-d', '--date',
        type=str, metavar='DATE',
        help='填报疫情通时的日期（格式： yyyy-MM-dd ），生成疫情通截图时选填，缺省值为今天'
    )
    parser.add_argument(
        '-t', '--time',
        type=str, metavar='TIME', dest='shot_time',
        help='填报疫情通时的时间（格式： HH:mm ），生成疫情通截图时选填，缺省值为现在'
    )
    parser.add_argument(
        '-b', '--battery',
        type=str, metavar='BATTERY',
        help='填报疫情通时手机剩余电量（两位数 10-99 ），生成疫情通截图时选填，缺省值随机'
    )
    parser.add_argument(
        '-o', '--output',
        type=str, metavar='PATH',
        help='疫情通截图保存路径，生成疫情通截图时选填，不填则直接显示不保存'
    )

    args = parser.parse_args()

    # 填报疫情通或上传截图
    if args.action in ('submit_to_yqt', 'upload_screenshot'):
        logger.info('模拟运行 SCF')
        ret = main_handler({'Type': 'Timer', 'TriggerName': args.action}, None)
        logger.info(f'运行结果：{ret}')

    # 生成疫情通截图
    elif args.action == 'generate_screenshot':
        name = args.name
        stu_id = args.stu_id
        if not name or not stu_id:
            logger.error('生成疫情通截图时，参数 --name 和 --stu-id 必填')
            return
        name = name[:6]
        stu_id = stu_id[:11]

        date = args.date[:10] if args.date else None
        shot_time = args.shot_time[:5] if args.shot_time else None

        battery = args.battery
        try:
            battery = int(battery) if 10 <= int(battery) <= 99 else None
        except (TypeError, ValueError):
            battery = None

        img = generate_screenshot(name, stu_id, date, shot_time, battery)

        if args.output:  # 保存图片
            img.save(args.output, 'png')
        else:  # 显示图片
            img.show()

        img.close()

    # 理论上不可能出现的情况
    else:
        logger.error('难以理解的要求')


if __name__ == '__main__':
    main()
