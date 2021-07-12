from flask import Flask, render_template, request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'
db = SQLAlchemy(app)


class Customer(db.Model):
   sno = db.Column(db.Integer(), primary_key=True)
   name = db.Column(db.String(length=30), nullable=False, unique=True)
   email = db.Column(db.String(length=25),nullable=False, unique=True)
   transaction_id = db.Column(db.Integer(), nullable=False)
   currentbalance = db.Column(db.String(length=12), nullable=False, unique=True)


class History(db.Model):
    sno = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer(), nullable=False)
    receiver = db.Column(db.Integer(), nullable=False)
    cash = db.Column(db.Integer(), nullable=False)


def __repr__(self):
     return f'Customer {self.name}'


@app.route('/')
def cover_page():
    return render_template('coverpage.html')


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/customers')
def customer_page():
    customers = Customer.query.all()
    return render_template('db.html', customers=customers)


@app.route('/transfer')
def transfer_page():
    return render_template('Transfer.html')


@app.route('/success')
def success_page():
    return render_template('success.html')


@app.route('/views/<string:viewer_id>', methods=['GET'])
def view_page(viewer_id):
    s_no = int(viewer_id)
    cust = Customer.query.get(s_no)
    customer = [cust]
    return render_template('view.html', customer=customer)


@app.route('/transferamount/<string:sender_id>/<string:receipt_id>/<string:amount>', methods=['GET', 'POST'])
def transfer_amount(sender_id, receipt_id, amount):
    senderid = int(sender_id)
    receiptid = int(receipt_id)
    debitamt = int(amount)
    print(senderid, receiptid, debitamt)
    record = History(sender=senderid, receiver=receiptid, cash=debitamt)
    db.session.add(record)
    db.session.commit()
    return render_template('success.html')


@app.route('/transactionhistory')
def transaction_history():
    history = History.query.all()
    return render_template('history.html', history=history)


if __name__ == "__main__":
    app.run(debug=True)