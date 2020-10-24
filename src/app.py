from flask import Flask, render_template, current_app, request, redirect, url_for, jsonify,session, flash
from functools import wraps
import os
import json
import datetime
from pytz import timezone
from json import JSONEncoder
import pymongo
#from flask_mail import Mail, Message


SECRET_KEY = 'sho123prav456mana911234'

app = Flask(__name__)
app.secret_key = SECRET_KEY
#mail=Mail(app)
URI = "mongodb+srv://praveen123:praveen321@skt.u5rw5.mongodb.net/skt_sc?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client['skt_sc']

#app.config['MAIL_SERVER']='smtp.gmail.com'
'''app.config['MAIL_SERVER']='smtp.live.com'
app.config['MAIL_PORT'] = 587
#app.config['MAIL_USERNAME'] = 'newperspectiveofficials@gmail.com'
#app.config['MAIL_PASSWORD'] = 'manpradev'
app.config['MAIL_USERNAME'] = 'praveen113kumar@hotmail.com'
app.config['MAIL_PASSWORD'] = 'revathi@113'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)'''

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
   
# database  
#print(product_list_PID)

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)
#STATIC_ROOT = os.path.join(BASE_DIR, '/src/stactic/')
#print(STATIC_ROOT)
#os.path.join(BASE_DIR, 'documents')
'''
with open(BASE_DIR+'/src/product_list_categ.json') as data:
    product_list_categ = json.load(data)

with open(BASE_DIR+ '/src/product_list_PID.json') as data:
    product_list_PID = json.load(data)
'''
login_username = "sasikani@2020crackers@skt"
login_password = "Sasikani@2020"

# custom Encoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()


@app.route('/')
def index():
	try:

		Collection_pro = db["product"] 

		json_c = {}
		for x in Collection_pro.find():
			#print(x)
			product_list_PID = x.copy()
			#print(type(product_list_PID))
			#print('\n')
			#print(product_list_PID)
			#print('\n')
			product_list_PID.update(json_c)
			#print('***********')

		product_list_PID = dict(filter(lambda elem: elem[0] != '_id' , product_list_PID.items())) 


		new_dict={}
		for key,value in product_list_PID.items():
			new_dict[key]=value["Rate"]

		Categ_dict = {}
		te = []
		for key,values in product_list_PID.items():
			te.append(values)

		for each in te:
			Key = each['Category']
			if Key in Categ_dict.keys():
				Categ_dict[Key].append(each)
			else:
				Categ_dict[Key]=[each]

		path = 'assets/product_photos/'
		return render_template('index.html',product_list_categ=Categ_dict, price=new_dict)
	except Exception as err:
		print(str(err))
		return 'Error ahhm'


@app.route('/submit/order/',methods = ['POST'])
def submit_order():

	if request.method == 'POST':
		result = request.form
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


		Collection_pro = db["product"] 

		json_c = {}
		for x in Collection_pro.find():
			#print(x)
			product_list_PID = x.copy()
			#print(type(product_list_PID))
			#print('\n')
			#print(product_list_PID)
			#print('\n')
			product_list_PID.update(json_c)
			#print('***********')

		product_list_PID = dict(filter(lambda elem: elem[0] != '_id' , product_list_PID.items())) 



		order_dict = generate_order_sheet(selected_PID_dict,product_list_PID)

		#print(order_dict)

		#product_list_PID
		dat = ''
		#head = '<thead><th><tr><th>S.No</th><th>PID</th><th>Product Name</th><th>Rate</th><th>Qty</th><th>Amt</th></thead>'
		total_amt = 0

		check = len(order_dict.keys())
		for key in order_dict.keys():
			if key == check:
				dat += '<tr class="last-row" ><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
			else:
				dat += '<tr><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
			total_amt += order_dict[key]["qty_amt"]


		if total_amt < 3000:
			return '<h1 style="color:red;">Please order above Rs.3000</h1> <button><a href="https://covaicrackers.com">Home</a></button>'

		invoice_table = '<tbody>'+dat+'</tbody>'


		Col_order = db["orders"]
		json_d = {}
		order_list_dict = {}
		for y in Col_order.find():
			#print(x)
			order_list_dict = y.copy()
			#print(type(product_list_PID))
			#print('\n')
			#print(product_list_PID)
			#print('\n')
			order_list_dict.update(json_d)
			#print('***********')

		order_list_dict = dict(filter(lambda elem: elem[0] != '_id' , order_list_dict.items())) 
		#print("\n From Database")
		#print(order_list_dict)

		'''try:
			with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
				order_list_dict1 = json.load(jsonFile) #, object_hook=DecodeDateTime
		except IOError as err:
			print('err')'''


		#datetime.datetime.fromisoformat(empDict["joindate"])


		recpient_email = 'crackerssasikani@gmail.com'
		customer_email = result.get('email','')
		customer_name = result.get('name')
		customer_phone = result.get('phone')
		customer_address = result.get('address')
		payment_option = result.get('payment_option')
		#print("Process ends here")
		order_time  = datetime.datetime.now()
		#order_time =  datetime.now(timezone('Asia/Kolkata'))
		#print(order_time)
		#with open(BASE_DIR+'/src/latest_ref_no.txt') as data:
		    #shiprocket_token = data.read().strip()

		#print(order_list_dict)
		#print('selected_PID_dict')
		#print(selected_PID_dict)
		ref_no = generate_order_no(order_list_dict)
		order_list_dict1={}
		order_list_dict1[ref_no] = {}
		order_details = order_list_dict1[ref_no]

		order_details['order_no'] = ref_no
		order_details['order_processed'] = False
		order_details['order_time'] = order_time
		order_details['payment_option'] = payment_option
		order_details['order_amt'] = total_amt
		order_details['customer_details'] = {"name":customer_name,"phone":customer_phone,"email":customer_email,"address":customer_address}
		order_details['product_details'] = selected_PID_dict


		Col_order.insert_one(order_list_dict1)
		'''
		try:
			with open(BASE_DIR+ '/src/order_list.json', "w") as jsonFile:
				json.dump(order_list_dict, jsonFile, cls=DateTimeEncoder)

		except Exception as err:
			#pass
			print(err)

		'''

		#product_list_PID
		#msg = Message('Hello New Order', sender = 'praveen113kumar@hotmail.com', recipients = [recpient_email])
		#msg.body = "<html><head>"+links+"</head>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Finally: "+str(selected_PID_dict)+"<br>Bye</html>"
		#msg.body = "Hi"
		#msg.html = "<html>Hello "+customer_name+" has ordered.<br> His Phone Number: "+customer_phone+"<br>His Address: "+customer_address+"<br>Order Details: <br>"+table+"<br>Bye</html>"



		dict_new = {'name':customer_name,'address':customer_address,"phone":customer_phone,"mail":customer_email,"order_time":order_time,"ref_no":ref_no,"payment_option":payment_option}

		#msg.html = render_template('invoice.html',invoice_table=invoice_table,total_amt=total_amt,invoice_details=dict_new,payment_option=payment_option)

		'''try:
			mail.send(msg)
		except Exception as err:
			#pass
			print(err)'''


		return render_template('invoice.html',invoice_table=invoice_table,total_amt=total_amt,invoice_details=dict_new,payment_option=payment_option)



def generate_order_no(order_list_dict):
	keys = list(order_list_dict.keys())
	print(keys)
	if len(keys) > 0:
		keys.sort()
		o_n = keys[-1].split('-')
		no = int(o_n[1]) + 1
		o_n = o_n[0]+'-'+str(no).zfill(5)
		return o_n
	else:
		return 'SKT-00001'

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

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'token' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('admin_login'))

    return wrap


@app.route('/admin/login',methods = ['POST','GET'])
#@login_required
def admin_login():
	if request.method == 'POST':
		result = request.form
		username = result.get('username')
		password = result.get('password')
		#print(username)
		#print(password)
		if (username == login_username and password == login_password):
			session['token'] = True
			return redirect(url_for('admin'))
		else:
			#print('Wrong Password')
			flash("Wrong Username or Password")
			return render_template('login.html')
	if request.method == 'GET':
		return render_template('login.html')

@app.route('/admin/logout')
@login_required
def logout():
	session.pop('token',None)
	return render_template('login.html')
	#redirect(url_for('admin_login'))


@app.route('/admin')
@login_required
def admin():

	Col_order = db["orders"]
	json_d = {}
	order_list_dict = {}
	for y in Col_order.find():
		#print(x)
		order_list_dict2 = y.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		order_list_dict.update(order_list_dict2)
		#print('***********')

	order_list_dict = dict(filter(lambda elem: elem[0] != '_id' , order_list_dict.items())) 
	#print("\n From Database")
	#print(order_list_dict)

	'''

	try:
		with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
			order_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')'''

	#print(order_list_dict)
	#check = len(order_list_dict.keys())
	#print(order_list_dict.keys())
	#print(len(list(order_list_dict.keys())))
	if len(list(order_list_dict.keys())) != 0:
		last_order = list(order_list_dict.keys())
		last_order.sort()
		last_order = last_order[-1]
		dat = ''
		counter = 1
		for key in order_list_dict.keys():
			if order_list_dict[key]['order_processed']:
				status = "Closed"
				action = 'Nil'
			else:
				status = "Open"
				action = '<a class="btn btn-success" role="button" href="close-order/'+str(key)+'">Close Order</a>'
			#status = str(order_list_dict[key]['order_processed'])
			if key == last_order:
				dat += '<tr class="last-row" ><td class="text-center">'+str(counter)+'</td><td class="text-center"><a href="order-detail/'+str(key)+'">'+str(key)+'</a></td><td class="text-center">'+str(order_list_dict[key]['customer_details']['name'])+'</td><td class="text-center">'+str(order_list_dict[key]['customer_details']['phone'])+'</td><td class="text-center">'+str(order_list_dict[key]['order_amt'])+'</td><td class="text-center">'+status+'</td><td class="text-center">'+action+'</td></tr>'
			else:
				dat += '<tr><td class="text-center">'+str(counter)+'</td><td class="text-center"><a href="order-detail/'+str(key)+'">'+str(key)+'</a></td><td class="text-center">'+str(order_list_dict[key]['customer_details']['name'])+'</td><td class="text-center">'+str(order_list_dict[key]['customer_details']['phone'])+'</td><td class="text-center">'+str(order_list_dict[key]['order_amt'])+'</td><td class="text-center">'+status+'</td><td class="text-center">'+action+'</td></tr>'
			counter += 1
			#total_amt += order_list_dict[key]["qty_amt"]

		orders_table = '<tbody>'+dat+'</tbody>'
	else:
		orders_table = '<tbody>No Data</tbody>'

	return render_template('admin_page.html',orders_table=orders_table)


@app.route('/order-detail/<order_id>')
@login_required
def order_detail(order_id):



	Collection_pro = db["product"] 

	json_c = {}
	for x in Collection_pro.find():
		#print(x)
		product_list_PID = x.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		product_list_PID.update(json_c)
		#print('***********')

	product_list_PID = dict(filter(lambda elem: elem[0] != '_id' , product_list_PID.items())) 


	Col_order = db["orders"]
	json_d = {}
	order_list_dict = {}
	for y in Col_order.find():
		#print(x)
		order_list_dict2 = y.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		order_list_dict.update(order_list_dict2)
		#print('***********')

	order_list_dict = dict(filter(lambda elem: elem[0] != '_id' , order_list_dict.items())) 

	'''try:
		with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
			order_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')
	'''
	taotal_order_ids = list(order_list_dict.keys())
	


	try:
		if order_id in taotal_order_ids:

			selected_PID_dict = order_list_dict[order_id]['product_details'] 

			order_dict = generate_order_sheet(selected_PID_dict,product_list_PID)
			#print(order_dict)
			#product_list_PID
			dat = ''
			#head = '<thead><th><tr><th>S.No</th><th>PID</th><th>Product Name</th><th>Rate</th><th>Qty</th><th>Amt</th></thead>'
			total_amt = 0

			check = len(order_dict.keys())
			for key in order_dict.keys():
				if key == check:
					dat += '<tr class="last-row" ><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
				else:
					dat += '<tr><td class="text-center">'+str(key)+'</td><td class="text-center">'+str(order_dict[key]["PID"])+'</td><td class="text-center">'+str(order_dict[key]["Product_Name"])+'</td><td class="text-right">'+str(order_dict[key]["Rate"])+'</td><td class="text-right">'+str(order_dict[key]["qty"])+'</td><td class="text-right">'+str(order_dict[key]["qty_amt"])+'</td></tr>'
				total_amt += order_dict[key]["qty_amt"]

			invoice_table = '<tbody>'+dat+'</tbody>'

			customer_name = order_list_dict[order_id]["customer_details"]["name"]
			customer_address = order_list_dict[order_id]["customer_details"]["address"]
			customer_phone = order_list_dict[order_id]["customer_details"]["phone"]
			customer_email = order_list_dict[order_id]["customer_details"]["email"]
			#order_list_dict[order_id]["order_time"] = datetime.datetime.fromisoformat(order_list_dict[order_id]["order_time"])
			order_time = order_list_dict[order_id]["order_time"]
			ref_no = order_id
			payment_option = order_list_dict[order_id]["payment_option"]
			total_amt = order_list_dict[order_id]["order_amt"]


			dict_new = {'name':customer_name,'address':customer_address,"phone":customer_phone,"mail":customer_email,"order_time":order_time,"ref_no":ref_no,"payment_option":payment_option}

			return render_template('invoice.html',invoice_table=invoice_table,total_amt=total_amt,invoice_details=dict_new,payment_option=payment_option)

		else:
			return render_template('error.html')
	except Exception as err:
		print(err)
		return "Error"

@app.route('/close-order/<order_id>')
@login_required
def close_order(order_id):
	Col_order = db["orders"]
	order_list_dict = {}
	for y in Col_order.find():
		#print(x)
		order_list_dict2 = y.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		order_list_dict.update(order_list_dict2)
		#print('***********')

	order_list_dict = dict(filter(lambda elem: elem[0] != '_id' , order_list_dict.items())) 
	print(order_list_dict.keys())

	'''
	try:
		with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
			order_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')
	'''
	'''
	taotal_order_ids = list(order_list_dict.keys())
	if order_id in taotal_order_ids:
		order_list_dict[order_id]['order_processed'] = True
	'''
	
	query =Col_order.find_one({order_id+".order_processed":False})
	print(query)
	replace_data = {"$set" :{order_id+".order_processed":True}}
	result = Col_order.update_one( query, replace_data )
	print(result)

	'''
		with open(BASE_DIR+ '/src/order_list.json', "w") as jsonFile:
		    json.dump(order_list_dict, jsonFile, cls=DateTimeEncoder)

	'''
	return redirect(url_for('admin'))



@app.route('/product_update')
@login_required
def product_update():
	Collection_pro = db["product"] 
	json_c = {}
	for x in Collection_pro.find():
		#print(x)
		product_list_dict = x.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		product_list_dict.update(json_c)
		#print('***********')

	product_list_dict = dict(filter(lambda elem: elem[0] != '_id' , product_list_dict.items())) 
	#print(product_list_PID)
	'''
	try:
		with open(BASE_DIR+ '/src/product_list_PID.json', "r") as jsonFile:
			product_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')
	'''
	#print(order_list_dict)
	#check = len(order_list_dict.keys())
	#print(order_list_dict.keys())
	#print(len(list(order_list_dict.keys())))
	if len(list(product_list_dict.keys())) != 0:
		last_product = list(product_list_dict.keys())
		last_product.sort()
		last_product = last_product[-1]
		dat = ''
		counter = 1
		for key in product_list_dict.keys():
			if product_list_dict[key]['show']:
				status = "Active"
				action = '<a class="btn btn-danger" role="button" href="close-product/'+str(key)+'">Hide Product</a>'
			else:
				status = "Inactive"
				action = '<a class="btn btn-success" role="button" href="open-product/'+str(key)+'">Show Product</a>'
			#status = str(order_list_dict[key]['order_processed'])
			if key == last_product:
				dat += '<tr class="last-row" ><td class="text-center">'+str(counter)+'</td><td class="text-center">'+str(product_list_dict[key]['PID'])+'</td><td class="text-center">'+str(product_list_dict[key]['Product_Name'])+'</td><td class="text-center">'+status+'</td><td class="text-center">'+action+'</td></tr>'
			else:
				dat += '<tr><td class="text-center">'+str(counter)+'</td><td class="text-center">'+str(product_list_dict[key]['PID'])+'</td><td class="text-center">'+str(product_list_dict[key]['Product_Name'])+'</td><td class="text-center">'+status+'</td><td class="text-center">'+action+'</td></tr>'
			counter += 1
			#total_amt += order_list_dict[key]["qty_amt"]

		product_table = '<tbody>'+dat+'</tbody>'
	else:
		product_table = '<tbody>No Data</tbody>'

	return render_template('product_update.html',product_table=product_table)


@app.route('/close-product/<PID>')
@login_required
def close_product(PID):
	#product_list_categ
	Col_pro = db["product"]
	'''
	order_list_dict = {}
	for y in Col_order.find():
		#print(x)
		order_list_dict2 = y.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		order_list_dict.update(order_list_dict2)
		#print('***********')

	order_list_dict = dict(filter(lambda elem: elem[0] != '_id' , order_list_dict.items())) 
	print(order_list_dict.keys())
	'''

	'''
	try:
		with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
			order_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')
	'''
	'''
	taotal_order_ids = list(order_list_dict.keys())
	if order_id in taotal_order_ids:
		order_list_dict[order_id]['order_processed'] = True
	'''
	
	query =Col_pro.find_one({PID+".show":True})
	print(query)
	replace_data = {"$set" :{PID+".show":False}}
	result = Col_pro.update_one( query, replace_data )
	print(result)

	'''
		with open(BASE_DIR+ '/src/order_list.json', "w") as jsonFile:
		    json.dump(order_list_dict, jsonFile, cls=DateTimeEncoder)

	'''
	'''

	pids = list(product_list_PID.keys())
	if PID in pids:
		product_list_PID[PID]['show'] = False
		for key,values in product_list_categ.items():
			for e in values:
				if str(e['PID']) == PID:
					e['show'] = False

		
		Categ_dict = {}
		temp_dic_list = []
		for key,values in PID_dict.items():
			temp_dic_list.append(PID_dict[key])
		#print(temp_dic_list)
		for each in temp_dic_list:
		    Key = each['Category']
		    if Key in PID_dict.keys():
		        Categ_dict[Key].append(each)
		    else:
		        Categ_dict[Key]=[each]'''

		#print(PID_dict)
		#print(Categ_dict.keys())
	'''
		with open('product_list_PID.json', "w") as jsonFile:
		    json.dump(product_list_PID, jsonFile)
		with open('product_list_categ.json', "w") as jsonFile:
		    json.dump(product_list_categ, jsonFile)

		return redirect(url_for('product_update'))

	else:
		'''

	return redirect(url_for('product_update'))

@app.route('/open-product/<PID>')
@login_required
def open_product(PID):
	#product_list_categ
	Col_pro = db["product"]
	query =Col_pro.find_one({PID+".show":False})
	print(query)
	replace_data = {"$set" :{PID+".show":True}}
	result = Col_pro.update_one( query, replace_data )
	print(result)

	return redirect(url_for('product_update'))
'''
@app.route('/downlaodFile/edith', methods=['POST','GET'])
def downlaodFile():
	try:
		with open(BASE_DIR+ '/src/order_list.json', "r") as jsonFile:
			order_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')

	response = app.response_class(
		response=json.dumps(order_list_dict),
		status=200,
		mimetype='application/json'
		)
	return response
	'''
'''content = json.dumps(order_list_dict)
	return Response(content, 
		mimetype='application/json',
		headers={'Content-Disposition':'attachment;filename=zones.geojson'})'''
	#return json.dumps(order_list_dict)


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




@app.route('/product_change')
@login_required
def product_change():
	Collection_pro = db["product"] 
	json_c = {}
	for x in Collection_pro.find():
		#print(x)
		product_list_dict = x.copy()
		#print(type(product_list_PID))
		#print('\n')
		#print(product_list_PID)
		#print('\n')
		product_list_dict.update(json_c)
		#print('***********')

	product_list_dict = dict(filter(lambda elem: elem[0] != '_id' , product_list_dict.items())) 
	#print(product_list_PID)

	'''
	try:
		with open(BASE_DIR+ '/src/product_list_PID.json', "r") as jsonFile:
			product_list_dict = json.load(jsonFile) #, object_hook=DecodeDateTime
	except IOError as err:
		print('err')'''

	#print(order_list_dict)
	#check = len(order_list_dict.keys())
	#print(order_list_dict.keys())
	#print(len(list(order_list_dict.keys())))
	if len(list(product_list_dict.keys())) != 0:
		last_product = list(product_list_dict.keys())
		last_product.sort()
		last_product = last_product[-1]
		dat = ''
		counter = 1
		for key in product_list_dict.keys():
			#status = str(order_list_dict[key]['order_processed'])
			s_pid = str(product_list_dict[key]['PID'])
			action = '<button class="btn btn-warning updateBut" id="'+s_pid+'">Update</button>'
			if key == last_product:
				dat += '<tr class="last-row" ><td class="text-center">'+str(counter)+'</td><td class="text-center">'+str(product_list_dict[key]['PID'])+'</td><td class="text-center"><input type="text" class="form-control" id="pname'+s_pid+'" placeholder="Name" required value="'+str(product_list_dict[key]['Product_Name'])+'"></td><td class="text-center"><input type="number" class="form-control" id="mrp'+s_pid+'" placeholder="MRP" required value="'+str(product_list_dict[key]['MRP'])+'"></td><td class="text-center"><input type="text" class="form-control" id="dicount'+s_pid+'" placeholder="Discount" required value="'+str(product_list_dict[key]['Discount'])+'"></td><td class="text-center"><input type="number" class="form-control" id="rate'+s_pid+'" placeholder="Rate" required value="'+str(product_list_dict[key]['Rate'])+'"></td><td class="text-center">'+action+'</td></tr>'
			else:
				dat += '<tr><td class="text-center">'+str(counter)+'</td><td class="text-center">'+str(product_list_dict[key]['PID'])+'</td><td class="text-center"><input type="text" class="form-control" id="pname'+s_pid+'" placeholder="Name" required value="'+str(product_list_dict[key]['Product_Name'])+'"></td><td class="text-center"><input type="number" class="form-control" id="mrp'+s_pid+'" placeholder="MRP" required value="'+str(product_list_dict[key]['MRP'])+'"></td><td class="text-center"><input type="text" class="form-control" id="dicount'+s_pid+'" placeholder="Discount" required value="'+str(product_list_dict[key]['Discount'])+'"></td><td class="text-center"><input type="number" class="form-control" id="rate'+s_pid+'" placeholder="Rate" required value="'+str(product_list_dict[key]['Rate'])+'"></td><td class="text-center">'+action+'</td></tr>'
			counter += 1
			#total_amt += order_list_dict[key]["qty_amt"]

		product_table = '<tbody>'+dat+'</tbody>'
	else:
		product_table = '<tbody>No Data</tbody>'

	return render_template('chng_price.html',product_table=product_table)



@app.route('/cng_price',methods = ['POST','GET'])
@login_required
def cng_price():
	if request.method == 'POST':
		#print(dir(request))
		result = request.form
		#print(request.values)
		#print(result)
		PID =  result['PID']
		name = result['name']
		mrp = result['mrp']
		rate = result['rate']
		disc = result['disc']

		#print(PID,name,mrp,disc)
		#print(type(PID))
	Col_pro = db["product"]
	query1 =Col_pro.find_one({PID+".PID":int(PID)})
	replace_data1 = {"$set" :{PID+".Product_Name":name}}
	result1 = Col_pro.update_one( query1, replace_data1 )

	query2 =Col_pro.find_one({PID+".PID":int(PID)})
	replace_data2 = {"$set" :{PID+".MRP":int(mrp)}}
	result2 = Col_pro.update_one( query2, replace_data2 )

	query3 =Col_pro.find_one({PID+".PID":int(PID)})
	replace_data3 = {"$set" :{PID+".Rate":int(rate)}}
	result3 = Col_pro.update_one( query3, replace_data3 )

	query4 =Col_pro.find_one({PID+".PID":int(PID)})
	replace_data4 = {"$set" :{PID+".Discount":disc}}
	result4 = Col_pro.update_one( query4, replace_data4 )


	'''if request.method == 'GET':
		print(dir(request))
		result = request.form
		print(result)'''


	return "success"



if __name__ == '__main__':
	app.run(debug=True, port=int(os.environ.get('PORT',80)))



