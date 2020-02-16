import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Donation, Donor, User

app = Flask(__name__)
app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'


@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.select().where(User.name == request.form['user']).get()
        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['user']
            return redirect(url_for('all'))
        return render_template('login.jinja2', error="Incorrect username or password.")
    else:
        return render_template('login.jinja2')


@app.route('/add/', methods=['GET', 'POST'])
def add_donation():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        donor = Donor(name=request.form['name'])
        donor.save()
        Donation(donor=donor, value=int(request.form['donation'])).save()
        return redirect(url_for('all'))
    else:
        return render_template('add_donation.jinja2')


@app.route('/view_donor')
def check_donation():
    return redirect(url_for('all'))
#     donor = request.args.get('name', None)
#
#     if donor is None:
#         return render_template('check_donations.jinja2')
#
#     donor_donations = []
#
#     try:
#         for item in Donation.select():
#             if Donation.get(Donation.donor.name) == donor:
#                 donor_donations.append(item.value)
#             else:
#                 continue
#     except:
#         return render_template('check_donations.jinja2', error='Does Not Exist')
#
#     return render_template('donor_donations.jinja2', donation=donor_donations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

