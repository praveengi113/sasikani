from flask import Flask, render_template, current_app, request
import os
import json
from flask_mail import Mail, Message


app = Flask(__name__)
#mail=Mail(app)

#app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_SERVER']='smtp.live.com'
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

with open('product_list_categ.json') as data:
    product_list_categ = json.load(data)

with open('product_list_PID.json') as data:
    product_list_PID = json.load(data)


@app.route('/')
def index():
	path = 'assets/product_photos/'
	return render_template('index.html',product_list_categ=product_list_categ)


@app.route('/submit/order/',methods = ['POST'])
def submit_order():
	if request.method == 'POST':
		result = request.form
		#print(result)
		#selected_PID = [dict(tuple([key,items])) for key,items in result.items() if items != '']
		#selected_PID = dict(filter(lambda elem: elem[0] != 'email' and elem[0] != 'name'and elem[0] != 'phone' and elem[0] != 'address' , result.items()))
		#print(selected_PID)
		selected_PID = dict(filter(lambda elem: elem[1] != ''and elem[0] != 'email' and elem[0] != 'name'and elem[0] != 'phone' and elem[0] != 'address' , result.items())) 
		#print(selected_PID)
		selected_PID_dict = {}
		for key,values in selected_PID.items():
			selected_PID_dict[key.split('_')[-1]] = int(values)
		#print(selected_PID_dict)

		order_dict = generate_order_sheet(selected_PID_dict)

		#product_list_PID
		dat = ''
		head = '<thead><th><tr><th>S.No</th><th>PID</th><th>Product Name</th><th>Rate</th><th>Qty</th><th>Amt</th></thead>'
		total_amt = 0

		for key in order_dict.keys():
			dat += '<tr><td>'+str(key)+'</td><td>'+str(order_dict[key]["PID"])+'</td><td>'+str(order_dict[key]["Product_Name"])+'</td><td>'+str(order_dict[key]["Rate"])+'</td><td>'+str(order_dict[key]["qty"])+'</td><td>'+str(order_dict[key]["qty_amt"])+'</td></tr>'
			total_amt += order_dict[key]["qty_amt"]

		dat1 = '<tr><td></td><td></td><td></td><td></td><td>Total<br>Amount</td><td>'+str(total_amt)+'</td>'
		body = '<tbody>'+dat+dat1+'</tbody>'

		table = "<table class='table table-border'>"+head+body+"</table>"

		recpient_email = 'contact@sasikanicrackers.com'
		#recpient_email = result.get('email')
		customer_name = result.get('name')
		customer_phone = result.get('phone')
		customer_address = result.get('address')
		#product_list_PID
		msg = Message('Hello New Order', sender = 'praveen113kumar@hotmail.com', recipients = [recpient_email])
		msg.body = "<html>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Finally: "+str(selected_PID_dict)+"<br>Bye</html>"
		#msg.body = "Hi"
		msg.html = "<html>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Order Details: <br>"+table+"<br>Bye</html>"
		mail.send(msg)



		return render_template('index.html',product_list_categ=product_list_categ)


def generate_order_sheet(dic_1,dic_2=product_list_PID):
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

"""
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',80)))

"""

