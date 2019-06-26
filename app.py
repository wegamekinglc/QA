from typing import Tuple
import requests
from flask import (
    Flask, render_template, request, redirect
)
import pandas as pd

app = Flask(__name__)

pd.set_option('display.max_colwidth', -1)


def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


def handle_response_hr(resp: dict) -> Tuple[str, str]:
    code = resp['code']

    if code == 1:
        is_matched = '是'
        answer = resp['data']['target_answer'].replace('\n', '')
        answer = '<br>'.join(chunkstring(answer, 50))

    else:
        is_matched = '否'
        answer = "您好，这个问题您是商米第一位提到的呢，<br>" \
                 "暂时无法查询到对应答案哦。请您尝试调整搜索关键词或直接联系人力资源部张小桐(Tel:15651621590)来寻求帮助，<br>" \
                 "后续我们也会将您提出的问题完善到我的“大脑”中，谢谢您"
    return is_matched, answer


def handle_response_cs(resp: dict) -> Tuple[str, str]:
    code = resp['code']

    if code == 1:
        is_matched = '是'
        answer = resp['data']['target_answer'].replace('\n', '')
        answer = '<br>'.join(chunkstring(answer, 50))
    else:
        is_matched = '否'
        answer = "您好，已经帮您转人工服务!"
    return is_matched, answer


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit_button'] == '商米HR问答Demo':
            return redirect('/hr')
        elif request.form['submit_button'] == '客户服务问答Demo':
            return redirect('/cs')
    elif request.method == 'GET':
        return render_template('index.html', head='商米问答机器人测试')


@app.route('/hr', methods=['GET'])
def hr_form():
    return render_template('hr_search.html', hint="请输入测试问题", head="商米HR问答Demo", result="")


@app.route('/hr', methods=['POST'])
def hr_query():
    query = request.form['query']
    resp = requests.post('http://172.16.0.170:8126/faq', data={"question": query}).json()
    parsed_resp = handle_response_hr(resp)

    df = pd.DataFrame(columns=['是否匹配', '答案'])
    df.loc[0, '是否匹配'] = parsed_resp[0]
    df.loc[0, '答案'] = parsed_resp[1]
    return render_template('hr_search.html',
                           hint="请输入测试问题",
                           head="商米HR问答Demo",
                           result=df.to_html(index=False, justify='center', classes='center', escape=False))


@app.route('/cs', methods=['GET'])
def cs_form():
    return render_template('cs_search.html', hint="请输入测试问题", head="客户服务问答Demo", result="")


@app.route('/cs', methods=['POST'])
def cs_query():
    query = request.form['query']
    resp = requests.post('http://172.16.0.170:8000/faq', data={"question": query}).json()
    parsed_resp = handle_response_cs(resp)

    df = pd.DataFrame(columns=['是否匹配', '答案'])
    df.loc[0, '是否匹配'] = parsed_resp[0]
    df.loc[0, '答案'] = parsed_resp[1]
    return render_template('cs_search.html',
                           hint="请输入测试问题",
                           head="客户服务问答Demo",
                           result=df.to_html(index=False, justify='center', classes='center', escape=False))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
