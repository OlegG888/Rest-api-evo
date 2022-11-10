from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response, send_file
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
DOWNLOAD_FOLDER = '/'
DOWNLOAD_FILE = 'results.csv'

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
           file_path = os.path.abspath(file_path)
          # set the file path
           uploaded_file.save(file_path)
           parseCSV(file_path)
          # save the file
      return redirect(url_for('index'))


def parseCSV(filePath):
      # CVS Column Names
      col_names = ['TransactionId','RequestId','TerminalId','PartnerObjectId','AmountTotal','AmountOriginal','CommissionPS','CommissionClient','CommissionProvider','DateInput','DatePost','Status','PaymentType','PaymentNumber','ServiceId','Service','PayeeId','PayeeName','PayeeBankMfo','PayeeBankAccount','PaymentNarrative']
      # Use Pandas to parse the CSV file
      csvdata = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      for i,row in csvdata.iterrows():
            if i == 0:
              continue 
            value = (row['TransactionId'], row['RequestId'], row['TerminalId'], row['PartnerObjectId'], row['AmountTotal'], row['AmountOriginal'], row['CommissionPS'], row['CommissionClient'], row['CommissionProvider'], row['DateInput'],
                 row['DatePost'], row['Status'], row['PaymentType'], row['PaymentNumber'], row['ServiceId'], row['Service'], row['PayeeId'], row['PayeeName'], row['PayeeBankMfo'], row['PayeeBankAccount'], row['PaymentNarrative'])            
            values = ', '.join('"{0}"'.format(val) for val in value)
            sql = f"INSERT IGNORE  INTO finance (TransactionId, RequestId, TerminalId, PartnerObjectId, AmountTotal, AmountOriginal, CommissionPS, CommissionClient, CommissionProvider, DateInput, DatePost, Status, PaymentType, PaymentNumber, ServiceId, Service, PayeeId, PayeeName, PayeeBankMfo, PayeeBankAccount, PaymentNarrative) VALUES ({values})"
            mycursor.execute(sql)
            mydb.commit()
            print(i,row['TransactionId'],row['RequestId'],row['TerminalId'],row['PartnerObjectId'],row['AmountTotal'],row['AmountOriginal'],row['CommissionPS'],row['CommissionClient'],row['CommissionProvider'],row['DateInput'],row['DatePost'],row['Status'],row['PaymentType'],row['PaymentNumber'],row['ServiceId'],row['Service'],row['PayeeId'],row['PayeeName'],row['PayeeBankMfo'],row['PayeeBankAccount'],row['PaymentNarrative'])


#Filter data    
@app.route("/filter", methods=['GET'])
def api_filter():
   if request.method == 'GET':
    try:
      search_data = request.get_json()
      if 'TransactionId' in search_data:
        TransactionId = search_data['TransactionId']
        sql = f"SELECT * FROM csvdata.finance WHERE TransactionId in ('{TransactionId}')"
      elif 'TerminalId' in search_data:
        TerminalId = search_data['TerminalId']
        sql = f"SELECT * FROM csvdata.finance WHERE TerminalId in ({TerminalId})"
      elif 'Status' in search_data:
        Status = search_data['Status']
        sql = f"SELECT * FROM csvdata.finance WHERE Status in ('{Status}')"
      elif 'PaymentType'in search_data:
        PaymentType = search_data['PaymentType']
        sql = f"SELECT * FROM csvdata.finance WHERE PaymentType in ('{PaymentType}')"
      elif 'DatePostFrom'in search_data:
        DatePostFrom = search_data['DatePostFrom']
        DatePostTo = search_data['DatePostTo']
        sql = f"SELECT * FROM csvdata.finance WHERE DatePost BETWEEN ('{DatePostFrom}') AND ('{DatePostTo}') ORDER BY DatePost asc"
      elif 'PaymentNarrative'in search_data:
        PaymentNarrative = search_data['PaymentNarrative']
        sql = f"SELECT * FROM csvdata.finance WHERE PaymentNarrative LIKE ('%{PaymentNarrative}%')"
      else:
        resp = jsonify('Data not found in query string')
        return resp
      mycursor.execute(sql)
      row = mycursor.fetchall()
      labels = ['TransactionId','RequestId','TerminalId','PartnerObjectId','AmountTotal','AmountOriginal','CommissionPS','CommissionClient','CommissionProvider','DateInput','DatePost','Status','PaymentType','PaymentNumber','ServiceId','Service','PayeeId','PayeeName','PayeeBankMfo','PayeeBankAccount','PaymentNarrative']
      if 'CsvDownload' in search_data:
          df = pd.DataFrame.from_records(row,columns=labels)
          fullname = os.path.join(DOWNLOAD_FOLDER, DOWNLOAD_FILE)
          df.to_csv(fullname, index= False)
          return send_file('results.csv')
      return jsonify(row)   
    except Exception as e:
      print(e)
 
if (__name__ == "__main__"):
     app.run(host='0.0.0.0', port = 5000)
