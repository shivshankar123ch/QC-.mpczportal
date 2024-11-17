console.log("HIIIIIIII");
//form validation
function validateForm() {
    let bankName = document.forms["myForm"]["bank_name"].value;
    let x = document.forms["myForm"]["ac_number"].value;
    let y = document.forms["myForm"]["re_ac_number"].value;
    let ifsc_code = document.forms["myForm"]["ifsc"].value;
    let ac_holderName = document.forms["myForm"]["ac_holder_name"].value;
    let ifscData = document.getElementById('ifsc').value;
    let ifscRgex = /^[A-Za-z]{4}[a-zA-Z0-9]{7}$/;
    let ifscResult = ifscRgex.test(ifscData);

    if (bankName == "") {
        document.getElementById('bank_Name').innerHTML = "  Please fill the required details  ";
        return false;
    } else {
        document.getElementById('bank_Name').innerHTML = "";
    }

    var theSelect = myForm.bank_name;
    var bank_data2 = theSelect[theSelect.selectedIndex].text;

    var ifsc_data = document.getElementById("ifsc").value.toUpperCase();



    if (ifsc_data) {
        $.ajax({
            type: 'get',
            url: 'https://ifsc.razorpay.com/' + ifsc_data,

            success: function(data) {
                //    console.log(data.BANK);
                //    console.log(bank_data2);
                if (ifsc_code == "") {
                    document.getElementById('ifscCode').innerHTML = "  Please fill the required details";
                    return false;
                } else {
                    document.getElementById('ifscCode').innerHTML = "";
                    // if (ifscResult == false) {
                    //     document.getElementById('ifscCode').innerHTML = "Please fill the valid IFSC  Code";
                    //     return false;
                    // } else {

                    //     var ac_number1 = document.getElementById("protocol").value;
                    //     var re_ac_number1 = document.getElementById("re_ac_number").value;
                    //     if (bank_data2 !== data.BANK) {
                    //         console.log("bank name  not matched by ifsc");
                    //         document.getElementById('ifscCode').innerHTML = "BANK Name and  IFSC  Code not match";
                    //         return false;

                    //     } else {
                    //         console.log('kkkk');
                    //         document.getElementById('ifscCode').innerHTML = "";
                    //     }
                    // }
                }


            },
            error: function(error) {
                document.getElementById('ifscCode').innerHTML = " Invalid IFSC Code..";

            }
        })

    } else {
        document.getElementById('ifscCode').innerHTML = "  Please fill the required details  ";
    }


    //match ifsc data and bank name

    if (ac_holderName == "") {
        document.getElementById('ac_holderName').innerHTML = " Please fill the required details   ";
        return false;
    } else {
        document.getElementById('ac_holderName').innerHTML = "";
    }
    if (x == "") {
        document.getElementById('ac_tNumber').innerHTML = "  Please fill the required details ";
        return false;
    } else {
        document.getElementById('ac_tNumber').innerHTML = "";
    }
    if (y == "") {
        document.getElementById('Re_ac_Number').innerHTML = " Please fill the Re-enter Account number.. ";
        return false;
    } else {
        document.getElementById('Re_ac_Number').innerHTML = "";
    }

    let err = document.getElementById('ifscCode').innerHTML;
    if (err) {
        return false;
    }
    var ac_number1 = document.getElementById("protocol").value;
    var re_ac_number1 = document.getElementById("re_ac_number").value;
    // console.log(ac_number1);
    // console.log(re_ac_number1);
    if (ac_number1 !== re_ac_number1) {
        document.getElementById('Re_ac_Number').innerHTML = "  Account number not match..  ";
        return false;
    } else {
        // console.log("hh");
        document.getElementById('Re_ac_Number').innerHTML = "";
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
    if (!regex.test(key)

    ) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
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
    if (!regex.test(key)

    ) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}

function filterFunction() {
    console.log("optonnnnnnnnn")
    var options = document.getElementById('bank_name').options;
    for (let i = 0; i < options.length; i++) {
        console.log(options[i].value); //log the value
    }
}