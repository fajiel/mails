# coding=utf-8

from unsubscribe.unsub_msg import UnsubMSG
from flask import Flask, render_template, request


app = Flask(__name__)
app.config.from_object('config')

@app.route('/unsubscribe')
def unsubscribe_mail():
    """
    根据uid退订邮件
    """

    if request.method == 'POST':
        uid = request.form['uid']
    else:
        uid = request.args.get('uid')
    sm = UnsubMSG(uid)
    sm.unsub_mail()
    mail = sm.mail

    template = 'unsubscribe.html'
    if uid == mail:
        template = 'unsubscribed.html'
    return render_template(template, date=mail)

if __name__ == "__main__":
    app.run(host='0.0.0.0')