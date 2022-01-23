import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

SMTP_USER = os.environ['SMTP_USER']  # Googleアカウントのユーザ名
SMTP_PASSWORD = os.environ['SMTP_PASSWORD']  # Googleアカウントで生成したアプリパスワード
MAIL_FROM = os.environ['MAIL_FROM']  # 送信元のメールアドレス


def main():
    send_email('<送信先のメールアドレス>', 'メールの件名', 'メールの本文')


def send_email(to: str, subject: str, body: str):
    """
    メールを送信する。
    """
    msg = MIMEText(body)  # MIMETextオブジェクトでメッセージを組み立てる。
    msg['Subject'] = Header(subject, 'utf-8')  # 件名に日本語を含める場合はHeaderオブジェクトを使う。
    msg['From'] = MAIL_FROM
    msg['To'] = to

    with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
        smtp.login(SMTP_USER, SMTP_PASSWORD)  # 環境変数のユーザー名とパスワードでログインする。
        smtp.send_message(msg)  # send_message()メソッドでメールを送信する。

if __name__ == '__main__':
    main()
