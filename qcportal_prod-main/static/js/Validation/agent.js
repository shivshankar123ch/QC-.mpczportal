function validateForm() {
    console.log("function fireee")
    // let selct_name = document.froms["myForm"]["user"].value;
    let agency_name = document.forms["myForm"]["one"].value;
    let person_name = document.forms["myForm"]["two"].value;

    let mobile_no = document.forms["myForm"]["three"].value;
    let phoneNumber = document.getElementById('input3').value;
    let phoneRGEX = /^[6789]\d{9}$/;
    let phoneResult = phoneRGEX.test(phoneNumber);

    let person_email = document.forms["myForm"]["four"].value;
    let emailData = document.getElementById('input4').value;
    let emailLowerCase = emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult = emailRgex.test(emailLowerCase);

    let person_pan = document.forms["myForm"]["five"].value;
    let panNumber = document.getElementById('input5').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);

    let person_gst = document.forms["myForm"]["six"].value;
    let person_address = document.getElementById("input7").value;
    
    // if (selct_name == "") {
    //     document.getElementById('slect').innerHTML = " Please select the required field.  ";
    //     return false;
    // } else {
    //     document.getElementById('slect').innerHTML = " ";
    // }

    if (agency_name == "") {
        document.getElementById('name').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('name').innerHTML = " ";
    }
    if (person_name == "") {
        document.getElementById('person').innerHTML = " Please fill the required field . ";
        return false;
    } else {
        document.getElementById('person').innerHTML = " ";
    }
    if (mobile_no == "") {
        document.getElementById('mobile').innerHTML = " Please fill the required details.";
        return false;
    } else {
        if (phoneResult == false) {
            document.getElementById('mobile').innerHTML = " Please fill the valid mobile no.";
            return false;
        } else {
            document.getElementById('mobile').innerHTML = "";
        }
    }
    if (person_email == "") {
        document.getElementById('email').innerHTML = "Please fill the required details. ";
        return false;
    } else {
        if (emailResult == false) {
            document.getElementById('email').innerHTML = " Please fill the valid email ID.";
            return false;
        } else {
            document.getElementById('email').innerHTML = "";
        }
    }
    if (person_pan == "") {
        document.getElementById('pan_no').innerHTML = "  Please fill the Pan number(ABCTY1234D format) .";
        return false;
    } else {
        if (panResult == false) {
            document.getElementById('pan_no').innerHTML = "  Please fill the valid Pan number(ABCTY1234D format). ";
            return false;
        } else {
            document.getElementById('pan_no').innerHTML = "";
        }
    }

    if (person_gst == "") {
        document.getElementById('gst_no').innerHTML = " Please fill the required field . ";
        return false;
    } else {
        document.getElementById('gst_no').innerHTML = " ";
    }

    if (person_address == "") {
        document.getElementById('addresss').innerHTML = " Please fill the required field . ";
        return false;
    } else {
        document.getElementById('addresss').innerHTML = " ";
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
        key = String.fromCharCode(key);
    }
    var regex = /[0-9]|\./;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}