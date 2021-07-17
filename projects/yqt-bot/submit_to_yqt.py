"""与填报疫情通相关的方法
"""

import datetime
import json
import logging
import pytz
import re
import time
from typing import Dict

import requests

from conf.settings import YQT_URLS, TIMEZONE


logger = logging.getLogger('submit_to_yqt')


def handle_http_err(ret: requests.Response, event: str) -> None:
    """处理 HTTP 异常

    按照一个通用流程检查一个响应是否正确
    如果不正确，会抛出异常

    :param ret: 响应
    :param event: 事件，这个请求做了什么事情（比如： '登录' ）
    :return: None
    """

    if ret.status_code != 200:
        err_msg = f'{event}时服务端返回异常状态码：[{ret.status_code}] {ret.text}'
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    try:
        ret_data = json.loads(ret.text)
    except json.JSONDecodeError:
        err_msg = f'{event}时服务端返回结构异常：{ret.text}'
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    if ret_data.get('e') != 0:
        err_msg = f'{event}时服务端返回异常：[200] {ret_data.get("e")} - {ret_data.get("m")} - {ret_data.get("d")}'
        logger.error(err_msg)
        raise RuntimeError(err_msg)


def login(session: requests.Session, username: str, password: str) -> None:
    """登录疫情通

    :param session: 请求会话
    :param username: 用户名（学号）
    :param password: 密码
    :return: None
    """

    ret = session.post(
        f'{YQT_URLS["base"]}{YQT_URLS["login"]}',
        data={
            'username': username,
            'password': password
        }
    )
    handle_http_err(ret, '登录疫情通')


def generate_data(session: requests.Session, username: str) -> Dict[str, str]:
    """生成疫情通填报数据

    生成全部都是正常的数据

    :param session: 请求会话
    :param username: 用户名（学号）
    :return: 生成的数据
    """

    # 访问疫情通页面
    ret = session.get(f'{YQT_URLS["base"]}{YQT_URLS["yqt"]}')

    if ret.status_code != 200:
        err_msg = f'访问疫情通页面错误，状态码 {ret.status_code}'
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    # 正则查找 hasFlag
    has_flag = re.search(r"hasFlag: '1',", ret.text)
    if has_flag:
        err_msg = '今天已经填报疫情通，不能重复填报'
        logger.warning(err_msg)
        raise ValueError(err_msg)

    # 正则查找 uid 和 id 字段的值
    init_data = re.search(r'var def = (.+?)"uid":"([^"]+?)"(.+?)"id":([^"]+?),(.+?);\n', ret.text)
    if not init_data:
        err_msg = '疫情通页面结构不符合预期'
        logger.error(err_msg)
        raise RuntimeError(err_msg)
    uid = init_data.group(2)
    its_id = init_data.group(4)

    # 读取定位信息
    with open(f'conf/geo_api_info/{username}.json', 'rt', encoding='utf-8') as fp:
        geo_api_info_json = fp.read()
    geo_api_info_obj = json.loads(geo_api_info_json)

    # 生成填报数据
    data = {
        'szgjcs': '',
        'szcs': '',
        'zgfxdq': '0',
        'mjry': '0',
        'csmjry': '0',
        # 'uid': uid,
        # 'date': datetime.datetime.now(tz=pytz.timezone(TIMEZONE)).strftime('%Y%m%d'),
        'tw': '2',
        'sfcxtz': '0',
        'sfyyjc': '0',
        'jcjgqr': '0',
        # 'jcjg': '',
        'sfjcbh': '0',
        'sfcxzysx': '0',
        'qksm': '',
        'remark': '',
        'address': geo_api_info_obj["formattedAddress"],
        'area': (
            f'{geo_api_info_obj["addressComponent"]["province"]} '
            f'{geo_api_info_obj["addressComponent"]["city"]} '
            f'{geo_api_info_obj["addressComponent"]["district"]}'
        ),
        'province': geo_api_info_obj['addressComponent']['province'],
        'city': geo_api_info_obj['addressComponent']['city'],
        'geo_api_info': geo_api_info_json,
        # 'created': str(int(time.time())),
        'sfzx': '0',
        'sfjcwhry': '0',
        'sfcyglq': '0',
        'gllx': '',
        'glksrq': '',
        'jcbhlx': '',
        'jcbhrq': '',
        'sftjwh': '0',
        'sftjhb': '0',
        # 'fxyy': '',
        'bztcyy': '',
        # 'fjsj': '0',
        'sfjchbry': '0',
        'sfjcqz': '',
        # 'jcqzrq': '',
        # 'jcwhryfs': '',
        # 'jchbryfs': '',
        # 'xjzd': '',
        'szgj': '',
        # 'sfsfbh': '0',
        # 'szsqsfybl': '0',
        # 'sfsqhzjkk': '',
        # 'sqhzjkkys': '',
        # 'sfygtjzzfj': '0',
        # 'gtjzzfjsj': '',
        'sfjcjwry': '0',
        # 'created_uid': '0',
        # 'id': its_id,
        'gwszdd': '',
        # 'sfyqjzgc': '',
        # 'jrsfqzys': '',
        # 'jrsfqzfy': '',
        'ismoved': '0',
    }

    return data


def submit(session: requests.Session, data: Dict[str, str]) -> None:
    """提交疫情通

    :param session: 请求会话
    :param data: 填报的数据
    :return: None
    """

    ret = session.post(f'{YQT_URLS["base"]}{YQT_URLS["submit"]}', data=data)
    handle_http_err(ret, '提交疫情通时')


def submit_to_yqt(username: str, password: str) -> None:
    """提交疫情通

    :param username: 用户名（学号）
    :param password: 密码
    :return: None
    """

    logger.info(f'正在填报 {username} 的疫情通...')

    s = requests.Session()             # 创建会话
    login(s, username, password)       # 登录
    data = generate_data(s, username)  # 生成提交表单
    submit(s, data)                    # 提交
    s.close()                          # 关闭会话

    logger.info(f'{username} 疫情通已提交')
