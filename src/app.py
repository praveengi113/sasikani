from flask import Flask, render_template, current_app, request
import os
import json
import datetime
from flask_mail import Mail, Message
#import requests
import smtplib
from email.mime.text import MIMEText




app = Flask(__name__)
#mail=Mail(app)

#app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_SERVER']='smtp.live.com'
app.config['DEBUG'] = True
app.config['MAIL_PORT'] = 587
#app.config['MAIL_USERNAME'] = 'newperspectiveofficials@gmail.com'
#app.config['MAIL_PASSWORD'] = 'manpradev'
app.config['MAIL_USERNAME'] = 'praveen113kumar@hotmail.com'
app.config['MAIL_PASSWORD'] = 'revathi@113'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

"""
@app.route('/')
def index():
    covid_data_log = Feed.from_mongo_all()
    covid_data = Feed.from_mongo()
    cases = covid_data[0]["cases"]
    cured = covid_data[0]["cured"]
    death = covid_data[0]["death"]
    date = covid_data[0]["time"]
    return render_template('cards_try.html', cases=cases, cured=cured, death=death, date=date, log=covid_data_log)
"""

#{% for key, value in result.items() %}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
#STATIC_ROOT = os.path.join(BASE_DIR, '/src/stactic/')
#print(STATIC_ROOT)
#os.path.join(BASE_DIR, 'documents')

with open(BASE_DIR+'/src/product_list_categ.json') as data:
    product_list_categ = json.load(data)

with open(BASE_DIR+ '/src/product_list_PID.json') as data:
    product_list_PID = json.load(data)

@app.route('/')
def index():
	new_dict={}
	for key,value in product_list_PID.items():
		new_dict[key]=value["Rate"]

	path = 'assets/product_photos/'
	return render_template('index.html',product_list_categ=product_list_categ, price=new_dict)


@app.route('/submit/order/',methods = ['POST'])
def submit_order():
	if request.method == 'POST':
		result = request.form
		with open(BASE_DIR+ '/src/product_list_PID.json') as data:
		    product_list_PID = json.load(data)
		#print(result)
		#selected_PID = [dict(tuple([key,items])) for key,items in result.items() if items != '']
		#selected_PID = dict(filter(lambda elem: elem[0] != 'email' and elem[0] != 'name'and elem[0] != 'phone' and elem[0] != 'address' , result.items()))
		#print(selected_PID)
		#print(result)
		selected_PID = dict(filter(lambda elem: elem[1] != ''and elem[1] != '0' and elem[0] != 'email' and elem[0] != 'name'and elem[0] != 'phone' and elem[0] != 'address' and elem[0] != 'payment_option' , result.items())) 
		#print(selected_PID)
		selected_PID_dict = {}
		for key,values in selected_PID.items():
			selected_PID_dict[key.split('_')[-1]] = int(values)
		#print(selected_PID_dict)

		order_dict = generate_order_sheet(selected_PID_dict,product_list_PID)

		#product_list_PID
		dat = ''
		head = '<thead><th><tr><th>S.No</th><th>PID</th><th>Product Name</th><th>Rate</th><th>Qty</th><th>Amt</th></thead>'
		total_amt = 0

		check = len(order_dict.keys())
		for key in order_dict.keys():
			if key == check:
				dat += '<tr class="last-row" ><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
			else:
				dat += '<tr><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
			total_amt += order_dict[key]["qty_amt"]

		invoice_table = '<tbody>'+dat+'</tbody>'

		dat1 = '<tr><td></td><td></td><td></td><td></td><td>Total<br>Amount</td><td>'+str(total_amt)+'</td>'
		links = '''<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>    
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"></script>'''
		body = '<tbody>'+dat+dat1+'</tbody>'

		table = "<table class='table table-responsive table-border'>"+head+body+"</table>"

		recpient_email = 'crackerssasikani@gmail.com'
		recpient_email_1 = result.get('email')
		customer_name = result.get('name')
		customer_phone = result.get('phone')
		customer_address = result.get('address')
		payment_option = result.get('payment_option')
		
		#product_list_PID
		msg = Message('Hello New Order', sender = 'praveen113kumar@hotmail.com', recipients = [recpient_email])
		msg.body = "<html><head>"+links+"</head>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Finally: "+str(selected_PID_dict)+"<br>Bye</html>"
		#msg.body = "Hi"
		#msg.html = "<html>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Order Details: <br>"+table+"<br>Bye</html>"

		ref_no = "Order0001"
		time_now = datetime.datetime.now()

		dict_new = {'name':customer_name,'address':customer_address,"phone":customer_phone,"mail":recpient_email_1,"order_time":time_now,"ref_no":ref_no,"payment_option":payment_option}

		#msg.html = render_template('invoice.html',invoice_table=invoice_table,total_amt=total_amt,invoice_details=dict_new,payment_option=payment_option)
		#requests.post("https://api.mailgun.net/v3/sandbox9ac083f02e414f50a0541191e04fe126.mailgun.org", auth = ("api","c4a2d57211829e33d0d81cfbd8f8f881-53c13666-64770e48"), data = {"from": "<app187924775@heroku.com>", "to": ["crackerssasikani@gmail.com"], "subject": "Order Placed", "html": "<html>Hello There</html>"})
		msg = MIMEText('Testing some Mailgun awesomness')
		msg['Subject'] = "Hello"
		msg['From'] = "praveen113kumar@hotmail.com"
		msg['To'] = "crackerssasikani@gmail.com"
		s = smtplib.SMTP('smtp.live.com', 587)
		s.login('praveen113kumar@hotmail.com','revathi@113')
		s.sendmail(msg['From'],msg['To'],msg.as_string())
		s.quit()

		try:
			mail.send(msg)
		except Exception as err:
			#pass
			print(err)

		"""msg = MIMEText('Testing some Mailgun awesomness')
		msg['Subject'] = "Hello"
		msg['From']    = "foo@YOUR_DOMAIN_NAME"
		msg['To']      = "bar@example.com"

		s = smtplib.SMTP('smtp.mailgun.org', 587)

		s.login('postmaster@YOUR_DOMAIN_NAME', '3kh9umujora5')
		s.sendmail(msg['From'], msg['To'], msg.as_string())
		s.quit()"""
		return render_template('invoice.html',invoice_table=invoice_table,total_amt=total_amt,invoice_details=dict_new,payment_option=payment_option)


def generate_order_sheet(dic_1,dic_2):
	selected = dic_1
	product_list = dic_2
	#print(product_list)
	total_amt = 0
	counter = 1
	new_dict = {}

	for key in selected.keys():
		qty = selected[key]
		qty_amt = qty*int(product_list[key]["Rate"])
		n_d = dict(product_list[key].items())
		n_d['qty'] = qty
		n_d['qty_amt'] = qty_amt
		new_dict[counter] = n_d
		counter += 1

	#print('new_dict')
	#print(new_dict)

	return new_dict

@app.route('/index')
def home1():
	new_dict={}
	for key,value in product_list_PID.items():
		new_dict[key]=value["Rate"]
	path = 'assets/product_photos/'
	return render_template('index.html',product_list_categ=product_list_categ, price=new_dict)

@app.route('/product')
def home2():
	new_dict={}
	for key,value in product_list_PID.items():
		new_dict[key]=value["Rate"]
	path = 'assets/product_photos/'
	return render_template('index.html',product_list_categ=product_list_categ, price=new_dict)


@app.route('/contact')
def home3():
	new_dict={}
	for key,value in product_list_PID.items():
		new_dict[key]=value["Rate"]
	path = 'assets/product_photos/'
	return render_template('index.html',product_list_categ=product_list_categ, price=new_dict)


	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',80)))



