//console.info(price)
//$("body").block(options);  
//$.blockUI(options);
$.blockUI({ message: '<h1><img src="https://hackernoon.com/images/0*4Gzjgh9Y7Gu8KEtZ.gif" /> Just a moment...</h1>' });

/*$("body").on('change','.qty',function() {

var qty = parseInt($(this).val());
if(qty == " "){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
if(qty == ""){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
if(qty == "0"){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
})*/




/*$('.qty').blur(function() {

var qty = parseInt($(this).val());
if(qty == " "){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
if(qty == ""){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }	
})

$('.qty').focusout(function() {

var qty = parseInt($(this).val());
if(qty == " "){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
if(qty == ""){
	alert('f');
    	$(this).val("0");//focus
    	$(this).parent().next().find('.total_price').html('₹ 0');
    	$(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }	
})*/


$("body").on('input','.qty',function() {
//$(".qty").bind('input',function() {
    //alert('hi')
    console.info($(this));
    var PID = $(this).attr('name');
    PID = parseInt(PID.split("_")[1]);
    var qty = parseInt($(this).val());
    //alert(qty);
    //console.info(qty)
    //console.info(qty)
    //console.info(typeof(qty))
    if(Number.isNaN(qty)){
        $(this).val("0");//focus
        $(this).parent().next().find('.total_price').html('₹ 0');
        $(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');
    }else{
        //alert('Not NaN')
    }
    if (qty >= 0){
        var rate = parseInt(price[PID-1])
        tot_amt = rate*qty
        console.info(tot_amt)
        $(this).parent().next().find('.total_price').html('₹ '+tot_amt);
        if(qty == 0){
            $(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');
            
        }else{
            $(this).parent().next().find('.total_price_cmt').html('(Item Added for checkout)');
        }
    }else if(qty == ""){
        $(this).val("0");//focus
        $(this).parent().next().find('.total_price').html('₹ 0');
        $(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
    if(qty == " "){
            $(this).val("0");//focus
            $(this).parent().next().find('.total_price').html('₹ 0');
            $(this).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

        }
    var tot_pri = $('.total_price');
    //var s_no = $("#extra_expense_div .s-no")
    var amount = 0;
    for (var i = 0; i < tot_pri.length; i++){
      //j = i+2
      var html = $(tot_pri[i]).html();
      console.info(html)
      amount += parseInt(html.split(" ")[1]);
      
    }
    $('#grand_total').html('<b>₹ '+amount+'</b>');
    $('#grand_total_po').html('<b>₹ '+amount+'</b>');
    $('#grand_total_fab').html('<b>₹ '+amount+'</b>');
    $('#grand_total_modal').html('<b>₹ '+amount+'</b>');



    if(amount >= 3000){
        $("#order_submit").attr("disabled", false);
    }else{
        $("#order_submit").attr("disabled", true);
    }

});
/*const input_ele = document.getElementsByClassName('qty')

input_ele.addEventListener("input",updateAmt);

function updateAmt(e){



	console.info($(e));
	var PID = $(e).attr('name');
	PID = parseInt(PID.split("_")[1]);
    var qty = parseInt($(e).val());
    console.info(typeof(qty))
    if (qty >= 0){
    	var rate = parseInt(price[PID-1])
    	tot_amt = rate*qty
    	console.info(tot_amt)
    	$(e).parent().next().find('.total_price').html('₹ '+tot_amt);
    	if(qty == 0){
    		$(e).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');
    		
    	}else{
    		$(e).parent().next().find('.total_price_cmt').html('(Item Added for checkout)');
    	}
    }else if(qty == ""){
    	$(e).val("0");//focus
    	$(e).parent().next().find('.total_price').html('₹ 0');
    	$(e).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

    }
	if(qty == " "){
		alert('f');
	    	$(e).val("0");//focus
	    	$(e).parent().next().find('.total_price').html('₹ 0');
	    	$(e).parent().next().find('.total_price_cmt').html('(Add Quantity for checkout)');

	    }
    var tot_pri = $('.total_price');
    //var s_no = $("#extra_expense_div .s-no")
    var amount = 0;
    for (var i = 0; i < tot_pri.length; i++){
      //j = i+2
      var html = $(tot_pri[i]).html();
      console.info(html)
      amount += parseInt(html.split(" ")[1]);
      
    }
    $('#grand_total').html('<b>₹ '+amount+'</b>')
    $('#grand_total_po').html('<b>₹ '+amount+'</b>')
    

    if(amount >= 3000){
    	$("#order_submit").attr("disabled", false);
    }else{
    	$("#order_submit").attr("disabled", true);
    }

}*/

//content18-v - phone
//content18-v - phone
var phone;
//content17-v - laptop
$(document).ready(function() {
$.unblockUI();
//$(window).load(function() { $.unblockUI(); });
$("#order_submit").attr("disabled", true);
const x = window.matchMedia("(max-width: 900px)");
//console.info(x);
if (x.matches) { // If media query matches
//document.body.style.backgroundColor = "yellow";
//alert('phone');
$("#order_div_foc").attr("href","index.html#content18-v");
$('#content17-v').remove()
phone = true;

} else {
//document.body.style.backgroundColor = "pink";
$("#order_div_foc").attr("href","index.html#content17-v");
$('#content18-v').remove()
//alert('laptop');
phone = false;
}

});


$('#accept').click(function(e) {
//alert('fdhdfh');
    var form = $('#order_form');
	//console.info(form);
	//console.info(for_url);
    //console.info(form);
	//form.validate();
    form.attr('action', for_url);
	var name = $('#pay_method_send').val();
	var radioValue = $("input[name='payment_option']:checked").val();
	if(radioValue == 1){
	$('#pay_method_send').val(name+' (Bank)');
	}else if(radioValue == 2){
	$('#pay_method_send').val(name+' (UPI)');
	}else if(radioValue == 3){
	$('#pay_method_send').val(name+' (COD)');
	}
	
	alert($('#pay_method_send').val());
    form.submit();
});


/*<tr> 
<td>10 CM electric sparkler</td>
<td>5</td>
<td>₹ 50</td>  
</tr>*/

$(document).on('click','#myBtn', function(){
  $('#exampleModal').modal('show');  
  var order_form = $('#order_form').serializeArray();
      dataObj = {};
//console.info(order_form);

$(order_form).each(function(i, field){
    if(field.name != 'name' && field.name != 'phone' && field.name != 'email' && field.name != 'address' && field.name != 'payment_option'){
        if(field.value != '0'){
            dataObj[field.name] = field.value;
        }
    }
});
$("#table_body").empty();
for(const property in dataObj){
    
    var input_ele = $('input[name="'+`${property}`+'"]');
    //console.info(input_ele);
    if(phone){
        var tot_price = $(input_ele).parent().next().find('.total_price').text()
        var title = $(input_ele).parent().prev().find('.title').text()
    }else{
        var title = $(input_ele).parent().prev().prev().find('.title').text()
        var tot_price = $(input_ele).parent().next().find('.total_price').text()      
    }

    //console.info(`${dataObj[property]}`);    
    var html = "<tr><td>"+title+"</td><td>"+`${dataObj[property]}`+"</td><td>"+tot_price+"</td></tr>"
    $('#table_body').append(html);
}

})