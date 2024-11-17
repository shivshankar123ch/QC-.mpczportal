function validateForm() {
    let bankName = document.forms["myForm"]["bgbank"].value;
    let bankNumber = document.forms["myForm"]["bg_no"].value;
    let issue = document.forms["myForm"]["bg_issu_date"].value;
    let valid = document.forms["myForm"]["bg_valid_upto"].value;
    let amount = document.forms["myForm"]["amount"].value;


    if (bankName == "") {
        document.getElementById('bank_Name').innerHTML = " ** Please fill the Detail... ";
        return false;
    } else {
        document.getElementById('bank_Name').innerHTML = "";
    }
    if (bankNumber == "") {
        document.getElementById('bank_no').innerHTML = " ** Please fill the Detail... ";
        return false;
    } else {
        document.getElementById('bank_no').innerHTML = "";
    }
    if (issue == "") {
        document.getElementById('issueDate').innerHTML = " ** Please Select the Issue Date... ";
        return false;
    } else {
        document.getElementById('issueDate').innerHTML = "";
    }
    if (valid == "") {
        document.getElementById('validDate').innerHTML = " ** Please Select the ValidUpto Date... ";
        return false;
    } else {
        document.getElementById('validDate').innerHTML = "";
    }
    if (amount == "") {
        document.getElementById('amount1').innerHTML = " ** Please fill the Amount... ";
        return false;
    } else {
        document.getElementById('amount1').innerHTML = "";
    }

}

function validate(evt) {
    var theEvent = evt || window.event;
    
    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
    // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key)
    ;
    }
    var regex = /[0-9]|\./;
    if( !regex.test(key)
    ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
    }
    }