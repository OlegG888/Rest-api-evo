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
  host="db",
  user="root",
  password="root",
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
      
@app.route("/filter", methods=["GET"])
def message():
    json = request.get_json()
    transaction_id = json['transaction_id']
    mycursor.execute("SELECT * FROM csvdata.finance WHERE TransactionId in (*transactionId)")
    terminal_id = json['terminal_id']
    status = json['status']
    payment_type = json['payment_type']
    date_post = json['date_post']
    payment_narrative = json['payment_narrative']


    return jsonify(" Hope you are having a good time " +  name + "!!!")

def parseCSV(filePath):
      # CVS Column Names
      col_names = ['TransactionId','RequestId','TerminalId','PartnerObjectId','AmountTotal','AmountOriginal','CommissionPS','CommissionClient','CommissionProvider','DateInput','DatePost','Status','PaymentType','PaymentNumber','ServiceId','Service','PayeeId','PayeeName','PayeeBankMfo','PayeeBankAccount','PaymentNarrative']
      # Use Pandas to parse the CSV file
      csvdata = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvdata.iterrows():
            if i == 0:
              continue 
            sql = "INSERT INTO finance (TransactionId, RequestId, TerminalId, PartnerObjectId, AmountTotal, AmountOriginal, CommissionPS, CommissionClient, CommissionProvider, DateInput, DatePost, Status, PaymentType, PaymentNumber, ServiceId, Service, PayeeId, PayeeName, PayeeBankMfo, PayeeBankAccount, PaymentNarrative) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            value = (row['TransactionId'],row['RequestId'],row['TerminalId'],row['PartnerObjectId'],row['AmountTotal'],row['AmountOriginal'],row['CommissionPS'],row['CommissionClient'],row['CommissionProvider'],row['DateInput'],row['DatePost'],row['Status'],row['PaymentType'],row['PaymentNumber'],row['ServiceId'],row['Service'],row['PayeeId'],row['PayeeName'],row['PayeeBankMfo'],row['PayeeBankAccount'],row['PaymentNarrative'])
            mycursor.execute(sql, value)
            mydb.commit()
            print(i,row['TransactionId'],row['RequestId'],row['TerminalId'],row['PartnerObjectId'],row['AmountTotal'],row['AmountOriginal'],row['CommissionPS'],row['CommissionClient'],row['CommissionProvider'],row['DateInput'],row['DatePost'],row['Status'],row['PaymentType'],row['PaymentNumber'],row['ServiceId'],row['Service'],row['PayeeId'],row['PayeeName'],row['PayeeBankMfo'],row['PayeeBankAccount'],row['PaymentNarrative'])

if (__name__ == "__main__"):
     app.run(host='0.0.0.0', port = 5000)