from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
import mysql.connector

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  port= "3306",
  database="csvdata"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
  print(x)


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
      return redirect(url_for('index'))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
      
@app.route("/filter", methods=['GET'])
def api_filter():
    query_parameters = request.args
    
    transaction_id = query_parameters.get('transaction_id')
    terminal_id = query_parameters.get('terminal_id')
    status = query_parameters.get('status')
    payment_type = query_parameters.get('payment_type')
    date_post = query_parameters.get('date_post')
    payment_narrative = query_parameters.get('payment_narrative')

    to_filter = []
    query = build_query(transaction_id, terminal_id, status, payment_type, date_post, payment_narrative)
    conn = mydb
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    results = cur.execute(query, to_filter).fetchall()
    
    return jsonify(results)

def build_query(transaction_id, terminal_id, status, payment_type, date_post, payment_narrative):
    
    if transaction_id:
        query = ' transaction_id=? AND'
        to_filter.append(transaction_id)
    if terminal_id:
        query += ' terminal_id=? AND'
        to_filter.append(terminal_id)
    if status:
        query += ' status=? AND'
        to_filter.append(status)
    if payment_type:
        payment_type += 'payment_type=? AND'
    if date_post:
        date_post += 'date_post=? AND'
    if payment_narrative:
        payment_narrative += 'payment_narrative=? AND'    
    if not (transaction_id or terminal_id or status or payment_type or date_post or payment_narrative):
        return render_template('404.html'), 404
    query = query[:-4] + ';'
    return query

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['TransactionId','RequestId','TerminalId','PartnerObjectId','AmountTotal','AmountOriginal','CommissionPS','CommissionClient','CommissionProvider','DateInput','DatePost','Status','PaymentType','PaymentNumber','ServiceId','Service','PayeeId','PayeeName','PayeeBankMfo','PayeeBankAccount','PaymentNarrative']
      # Use Pandas to parse the CSV file
      csvdata = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvdata.iterrows():
            if i == 0:
              continue 
            sql = "INSERT INTO finance (TransactionId, RequestId, TerminalId, PartnerObjectId, AmountTotal, AmountOriginal, CommissionPS, CommissionClient, CommissionProvider, DateInput, DatePost, Status, PaymentType, PaymentNumber, ServiceId, Service, PayeeId, PayeeName, PayeeBankMfo, PayeeBankAccount, PaymentNarrative) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE"
            value = (row['TransactionId'],row['RequestId'],row['TerminalId'],row['PartnerObjectId'],row['AmountTotal'],row['AmountOriginal'],row['CommissionPS'],row['CommissionClient'],row['CommissionProvider'],row['DateInput'],row['DatePost'],row['Status'],row['PaymentType'],row['PaymentNumber'],row['ServiceId'],row['Service'],row['PayeeId'],row['PayeeName'],row['PayeeBankMfo'],row['PayeeBankAccount'],row['PaymentNarrative'])
            mycursor.execute(sql, value)
            mydb.commit()
            print(i,row['TransactionId'],row['RequestId'],row['TerminalId'],row['PartnerObjectId'],row['AmountTotal'],row['AmountOriginal'],row['CommissionPS'],row['CommissionClient'],row['CommissionProvider'],row['DateInput'],row['DatePost'],row['Status'],row['PaymentType'],row['PaymentNumber'],row['ServiceId'],row['Service'],row['PayeeId'],row['PayeeName'],row['PayeeBankMfo'],row['PayeeBankAccount'],row['PaymentNarrative'])

if (__name__ == "__main__"):
     app.run(host='0.0.0.0', port = 5000)