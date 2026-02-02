#使用Python写一个正则表达式，把类似“xgshi@139.com, johnshi@139.com, rona1@vip.sina.com， 13456， Nihaoa, skter1@vip.sina.com"
#这样的字符串中的所有邮箱地址提取出来，放到一个列表中。
import re
def extract_emails(input_string):
    # 定义正则表达式模式来匹配邮箱地址
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # 使用 re.findall() 方法提取所有匹配的邮箱地址
    emails = re.findall(email_pattern, input_string)

    return emails
# 测试字符串
test_string = "xgshi@139.com, johnshi@139.com, rona1@vip.sina.com， 13456， Nihaoa, skter1@vip.sina.com"
print(extract_emails(test_string))
