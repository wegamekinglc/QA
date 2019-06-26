from flask import (
    Flask, render_template, request, redirect
)
import pandas as pd

app = Flask(__name__)


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
    df = pd.DataFrame(columns=['是否匹配', '答案'])
    df.loc[0, '是否匹配'] = '是'
    df.loc[0, '答案'] = query
    return render_template('hr_search.html', hint="请输入测试问题", head="商米HR问答Demo", result=df.to_html(index=False, classes='center'))


@app.route('/cs', methods=['GET'])
def cs_form():
    return render_template('cs_search.html', hint="请输入测试问题", head="客户服务问答Demo", result="")


@app.route('/cs', methods=['POST'])
def cs_query():
    query = request.form['query']
    df = pd.DataFrame(columns=['是否匹配', '答案'])
    df.loc[0, '是否匹配'] = '是'
    df.loc[0, '答案'] = query
    return render_template('cs_search.html', hint="请输入测试问题", head="客户服务问答Demo", result=df.to_html(index=False, classes='center'))


if __name__ == '__main__':
    app.run()#debug=True)