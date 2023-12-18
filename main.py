import random
import json
import sys

# 定义字符取值范围

CHARACTERS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
LOWER_CASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
UPPER_CASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                         'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOL = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '~', '@', '^', '_', '{', '}', '[', ']', '|', '<', '>', '?', '/',
          '-', '=', ';', ':', ',', '.', '`', "'", '"', '\\']  # noqa: E501

SYMBOLS = ['!', '#', '$', '%', '&', '*', '@', ]


# 定义密码生成函数
def generator_password(length):
    lower_case_password = number_password = strong_password = normal_password = simple_password = ''
    for i in range(length):
        strong_password += random.choice(CHARACTERS + NUMBERS + SYMBOLS)
        normal_password += random.choice(CHARACTERS + NUMBERS)
        simple_password += random.choice(CHARACTERS)
        number_password += random.choice(NUMBERS)
        lower_case_password += random.choice(LOWER_CASE_CHARACTERS)
    return lower_case_password, number_password, simple_password, normal_password, strong_password


# 定义密码强度评分函数
def password_score(password):
    score = 0

    if len(password) < 6:
        return score

    score += 1
    has_sz = has_xx = has_dx = has_ts = False

    for c in password:
        if has_sz is False and c in NUMBERS:
            score += 1
            has_sz = True
        if has_xx is False and c in LOWER_CASE_CHARACTERS:
            score += 1
            has_xx = True
        if has_dx is False and c in UPPER_CASE_CHARACTERS:
            score += 1
            has_dx = True
        if has_ts is False and c in SYMBOLS:
            score += 1
            has_ts = True

    # score += len(set(password)) // 6
    # print(password, score)
    return score


def isSeries(pwd: str, seriesCount: int = 3):
    '''
    判断密码是否连续
    pwd: 密码
    seriesCount: 连续个数
    '''
    if pwd and (len(pwd) > 0):
        # 自身算起
        ascSeriesCount = 1
        descSeriesCount = 1
        # 存在顺序型的连续性的字符串
        for i in range(len(pwd)):
            currentCharCode = pwd[i]
            if i == 0:
                prevCharCode = ""
            else:
                prevCharCode = pwd[i - 1]
                if currentCharCode == chr(ord(prevCharCode) + 1):
                    ascSeriesCount += 1
                    if ascSeriesCount == seriesCount:
                        return True
                else:
                    ascSeriesCount = 1

        # 存在逆序性的连续性的字符串*/
        for i in range(len(pwd)):
            currentCharCode = pwd[i]
            if (i - 1) >= 0:
                prevCharCode = pwd[i - 1]
            else:
                prevCharCode = ""
            if chr(ord(currentCharCode) + 1) == prevCharCode:
                descSeriesCount += 1
                if descSeriesCount == seriesCount:
                    return True
            else:
                descSeriesCount = 1
    return False


def get_icon_by_score(score):
    if score >= 5:
        return {'path': 'mima-4.png'}
    elif 4 >= score > 3:
        return {'path': 'mima-7.png'}
    elif 3 >= score > 2:
        return {'path': 'mima-5.png'}
    else:
        return {'path': 'mima-6.png'}


def main(length=16):
    lower_case_password, number_password, simple_password, normal_password, strong_password = generator_password(length)

    items = [
        {
            "title": strong_password,
            "subtitle": "字母 + 数字 + 特殊符号",
            "arg": strong_password,
            'icon': eval('get_icon_by_score(password_score(strong_password))'),
            "valid": "True"
        },
        {
            "title": normal_password,
            "subtitle": "字母 + 数字",
            "arg": normal_password,
            'icon': eval('get_icon_by_score(password_score(normal_password))'),
            "valid": "True"
        },
        {
            "title": simple_password,
            "subtitle": "纯字母密码",
            "arg": simple_password,
            'icon': eval('get_icon_by_score(password_score(simple_password))'),
            "valid": "True"
        },
        {
            "title": lower_case_password,
            "subtitle": "纯小写字母密码",
            "arg": lower_case_password,
            'icon': eval('get_icon_by_score(password_score(lower_case_password))'),
            "valid": "True"
        },
        {
            "title": number_password,
            "subtitle": "纯数字密码",
            "arg": number_password,
            'icon': eval('get_icon_by_score(password_score(number_password))'),
            "valid": "True"
        },

    ]

    return json.dumps({'items': items}, ensure_ascii=False)


if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else 16
    res = main(int(query))
    print(res)
