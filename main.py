from flask import Flask, render_template, request
import requests
import smtplib
from email.message import EmailMessage

posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()
app = Flask(__name__)

SEND_EMAIL = 'email'
EMAIL_PASSWORD = 'password'
TO_EMAIL = 'email'

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data['username'], data['email'], data['phone'], data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template("contact.html")

def send_email(username, email, phone, message):
    msg = EmailMessage()
    msg.set_content(f'Name: {username}\n Email: {email}\n Phone: {phone}\n Message: {message}')
    msg['from'] = 'Your Website'
    msg['to'] = TO_EMAIL
    msg['subject'] = 'New message!'
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SEND_EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    app.run(debug=True)
