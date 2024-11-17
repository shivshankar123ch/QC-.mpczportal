


console.log("123");



function validateForm() {
    console.log("hiiiii");
    let slect1 = document.forms["myForm"]["user"].value;
    let slect2 = document.forms["myForm"]["zone"].value;
    let slect3 = document.forms["myForm"]["service_type"].value;
    let companyName_e = document.forms["myForm"]["company_name_e"].value;
    // let companyName_h = document.forms["myForm"]["company_name_h"].value;
    let Name_of_authorized_e = document.forms["myForm"]["name_of_authorized_e"].value;
    // let Name_of_authorized_h = document.forms["myForm"]["name_of_authorized_h"].value;
    let mobile_number_one = document.forms["myForm"]["mobile1"].value;
    let phoneNumber = document.getElementById('mobile1').value;
    let phoneRGEX = /^[6789]\d{9}$/;
    let phoneResult = phoneRGEX.test(phoneNumber);
    let email_address = document.forms["myForm"]["email"].value;
    let emailData = document.getElementById('email1').value;
    let emailLowerCase = emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult = emailRgex.test(emailLowerCase);
    let gst_data = document.forms["myForm"]["gst"].value;
    let pan_data = document.forms["myForm"]["pan"].value;
    let panNumber = document.getElementById('pan1').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);
    let Add1 = document.forms["myForm"]["add1"].value;
    let pinCode = document.forms["myForm"]["zip"].value;
    let district = document.forms["myForm"]["add3"].value;
    let state = document.forms["myForm"]["add4"].value;
    let city = document.forms["myForm"]["city"].value;
    let add5 = document.forms["myForm"]["add5"].value;
    let pinCode2 = document.forms["myForm"]["zip2"].value;
    let district2 = document.forms["myForm"]["add8"].value;
    let state2 = document.forms["myForm"]["add7"].value;
    let city2 = document.forms["myForm"]["city2"].value;
    // let date = document.forms["myForm"]["dob"].value;
    // let mobileNumber = document.forms["myForm"]["mobiles"].value;
    // let phoneNumber2 = document.getElementById('mobile_2').value;
    // let phoneResult2 = phoneRGEX.test(phoneNumber2);
    let aadahrCard1 = document.forms["myForm"]["aadhar_2"].value;
    let aadharNumber1 = document.getElementById('Aadhar_2').value;
    let aadharRGEX = /^\d{12}$/;
    let aadharResult1 = aadharRGEX.test(aadharNumber1);
    let dirName = document.forms["myForm"]["dir_name"].value;
    //let name1 = document.forms["myForm"]["dir_name_hindi"].value;
    //let name1 = document.forms["myForm"]["dir_name_hindi"].value;
    // var date_1 = document.forms["myForm"]["dir_dob"].value;
    var mobileNumber1 = document.forms["myForm"]["dir_mobile"].value;
    let mobileNumber2 = document.getElementById('dir_mobile').value;
    let mobileRGEX = /^[6789]\d{9}$/;
    let mobileResult = mobileRGEX.test(mobileNumber2);
    let emails = document.forms["myForm"]["dir_email"].value;
    let emailData1 = document.getElementById('dirEmail').value;
    let emailLowerCase1 = emailData1.toLowerCase();
    let emailRgex1 = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult1 = emailRgex1.test(emailLowerCase1);
    let aadahrCard2 = document.forms["myForm"]["dir_aadhar"].value;
    let aadharNumber2 = document.getElementById('dir_aadhar_2').value;
    let aadharResult2 = aadharRGEX.test(aadharNumber2);
    let dir_add1 = document.forms["myForm"]["dir_add1"].value;
    let pincode_dir = document.forms["myForm"]["dirZip"].value;
    let state_2 = document.forms["myForm"]["dirState"].value;
    let district_2 = document.forms["myForm"]["dir_district_2"].value;
    let city_2 = document.forms["myForm"]["dir_city2"].value;


    if (slect1 == "") {
        document.getElementById('User1').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('User1').innerHTML = "";
    }
    if (slect2 == "") {
        document.getElementById('Zone').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('Zone').innerHTML = "";
    }
    // if (slect3 == "") {
    //     document.getElementById('firmName1').innerHTML = " Please fill the required details";
    //     return false;
    // } else {
    //     document.getElementById('firmName1').innerHTML = "";
    // }
    if (companyName_e == "") {
        document.getElementById('companyNameEnglish').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('companyNameEnglish').innerHTML = "";
    }
    // if (companyName_h == "") {
    //     document.getElementById('companyNameHindi').innerHTML = " ** कृपया कंपनी का नाम भरें.. ";
    //     return false;
    // } else {
    //     document.getElementById('companyNameHindi').innerHTML = "";
    // }
    if (Name_of_authorized_e == "") {
        document.getElementById('nameOfAauthorizedEnglish').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('nameOfAauthorizedEnglish').innerHTML = "";
    }
    // if (Name_of_authorized_h == "") {
    //     document.getElementById('nameOfAauthorizedHindi').innerHTML = " कृपया अधिकृत का नाम भरें";
    //     return false;
    // } else {
    //     document.getElementById('nameOfAauthorizedHindi').innerHTML = "";
    // }

    if (mobile_number_one == "") {
        document.getElementById('mobileNumber').innerHTML = "Please fill the required details";
        return false;
    } else {
        if (phoneResult == false) {
            document.getElementById('mobileNumber').innerHTML = "Please fill the required details";
            return false;
        } else {
            document.getElementById('mobileNumber').innerHTML = "";
        }
    }


    if (email_address == "") {
        document.getElementById('emailAddress').innerHTML = "Please fill the required details ";
        return false;
    } else {
        if (emailResult == false) {
            document.getElementById('emailAddress').innerHTML = " Please fill the required details";
            return false;
        } else {
            document.getElementById('emailAddress').innerHTML = "";
        }
    }
    if (pan_data == "") {
        document.getElementById('panNo').innerHTML = " Please fill the required details";
        return false;
    } else {
        // document.getElementById('panNo').innerHTML = "";
        if (panResult == false) {
            document.getElementById('panNo').innerHTML = "  Please fill the valid Pan number(ABCTY1234D format) ";
            return false;
        } else {
            document.getElementById('panNo').innerHTML = "";
        }
    }
    if (gst_data == "") {
        document.getElementById('gstNo').innerHTML = "  Please fill the GST number(11AAAAA1111Z1A1 format) ";
        return false;
    } else {
        document.getElementById('gstNo').innerHTML = "";

    }
    if (Add1 == "") {
        document.getElementById('address').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('address').innerHTML = "";
    }
    if (pinCode == "") {
        document.getElementById('code').innerHTML = " Please fill the required details";
        return false;
    } else {

        if (pinCode.length != 6) {
            document.getElementById('code').innerHTML = " Please fill the required details";
            return false;
        } else {
            document.getElementById('code').innerHTML = "";
        }
    }
    if (district == "") {
        document.getElementById('Add3').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('Add3').innerHTML = "";
    }
    if (state == "") {
        document.getElementById('state1').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('state1').innerHTML = "";
    }
    if (city == "") {
        document.getElementById('city1').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('city1').innerHTML = "";
    }
    if (add5 == "") {
        document.getElementById('txt_add3').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txt_add3').innerHTML = "";
    }
    if (pinCode2 == "") {
        document.getElementById('code2').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('code2').innerHTML = "";
    }
    if (state2 == "") {
        document.getElementById('state_2').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('state_2').innerHTML = "";
    }
    if (district2 == "") {
        document.getElementById('district_2').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('district_2').innerHTML = "";
    }
    if (city2 == "") {

        document.getElementById('city_2').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('city_2').innerHTML = "";
    }
    // if (date == "") {
    //     document.getElementById('birthDate').innerHTML = " Please fill the required details  ";
    //     return false;
    // } else {
    //     document.getElementById('birthDate').innerHTML = "";
    // }
    if (mobileNumber == "") {
        document.getElementById('mob_no_2').innerHTML = " Please fill the required details ";
        return false;
    } else {
        if (phoneResult2 == false) {
            document.getElementById('mob_no_2').innerHTML = "  Please fill the valid Mobile number";
            return false;
        } else {
            document.getElementById('mob_no_2').innerHTML = "";
        }
    }
    if (aadahrCard1 == "") {
        document.getElementById('aadhar_no_2').innerHTML = " Please fill the required details";
        return false;
    } else {
        if (aadharResult1 == false) {
            document.getElementById('aadhar_no_2').innerHTML = "  Please fill the valid Aadhar number ";
            return false;
        } else {
            document.getElementById('aadhar_no_2').innerHTML = "";
        }
    }
    if (dirName == "") {
        document.getElementById('proName').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('proName').innerHTML = "";
    }
    // if (name1 == "") {
    //     document.getElementById('proName1').innerHTML = "  कृपया नाम भरें.. ";
    //     return false;
    // } else {
    //     document.getElementById('proName1').innerHTML = "";
    // // }
    // if (date_1 == "") {
    //     document.getElementById('birthDate_1').innerHTML = " Please fill the required details";
    //     return false;
    // } else {
    //     document.getElementById('birthDate_1').innerHTML = "";
    // }
    if (mobileNumber1 == "") {
        document.getElementById('mob_no_12').innerHTML = " Please fill the required details";
        return false;
    } else {
        //document.getElementById('mob_no_1').innerHTML = "";
        if (mobileResult == false) {
            document.getElementById('mob_no_12').innerHTML = "  Please fill the valid Mobile number ";
            return false;
        } else {
            document.getElementById('mob_no_12').innerHTML = "";
        }
    }
    if (emails == "") {
        document.getElementById('email_121').innerHTML = " Please fill the required details ";
        return false;
    } else {
        if (emailResult1 == false) {
            document.getElementById('email_121').innerHTML = "  Please fill the valid Email ";
            return false;
        } else {
            document.getElementById('email_121').innerHTML = "";
        }
    }

    if (aadahrCard2 == "") {
        document.getElementById('aadhar_9').innerHTML = " Please fill the required details";
        return false;
    } else {
        if (aadharResult2 == false) {
            document.getElementById('aadhar_9').innerHTML = "  Please fill the valid Aadhar number ";
            return false;
        } else {
            document.getElementById('aadhar_9').innerHTML = "";
        }
    }
    if (dir_add1 == "") {
        document.getElementById('dir_Add1').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('dir_Add1').innerHTML = "";
    }
    if (pincode_dir == "") {
        document.getElementById('pinCode_21').innerHTML = "Please fill the required details ";
        return false;
    } else {
        document.getElementById('pinCode_21').innerHTML = "";
    }
    if (state_2 == "") {
        document.getElementById('state_21').innerHTML = "Please fill the required details ";
        return false;
    } else {
        document.getElementById('state_21').innerHTML = "";
    }
    if (district_2 == "") {
        document.getElementById('district_2').innerHTML = "Please fill the required details ";
        return false;
    } else {
        document.getElementById('district_2').innerHTML = "";
    }
    if (city_2 == "") {
        document.getElementById('city_21').innerHTML = "Please fill the required details ";
        return false;
    } else {
        document.getElementById('city_21').innerHTML = "";
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


//autofill address by checked
function fill() {
    let checkbox = document.getElementById("cbfill");
    let state = document.getElementById("txtstate").value;
    let city = document.getElementById("txtcity").value;
    let zip = document.getElementById("txtzip").value;
    let district = document.getElementById("txtdistrict").value;
    let add1 = document.getElementById("txtadd1").value;
    let add2 = document.getElementById("txtadd2").value;
    // /let add3 = document.getElementById("txtadd2").value;

    if (checkbox.checked === true) {
        document.getElementById("txtstate2").value = state;
        document.getElementById("txtcity2").value = city;
        document.getElementById("txtdistrict2").value = district;
        document.getElementById("txtzip2").value = zip;
        document.getElementById("txtadd3").value = add1;
        document.getElementById("txtadd4").value = add2;
        if (add1 === add2) {
            add1 = add2;

        }
        let txt_add2 = document.getElementById("txtadd2").value;
        let txt_add4 = document.getElementById("txtadd4").value;
        if (txt_add2 === txt_add4) {
            txt_add2 = txt_add4;
        }
        let txt_zip1 = document.getElementById("txtzip").value;
        let txt_zip2 = document.getElementById("txtzip2").value;
        let txt_city = document.getElementById("txtcity").value;
        let txt_city2 = document.getElementById("txtcity2").value;
        let txt_state = document.getElementById("txtstate").value;
        let txt_state2 = document.getElementById("txtstate2").value;
        let txt_district = document.getElementById("txtdistrict").value;
        let txt_district2 = document.getElementById("txtdistrict2").value;
        if (txt_zip1 === txt_zip2) {
            txt_zip1 = txt_zip2;
            txt_city = txt_city2;
            txt_state = txt_state2;
            txt_district = txt_district2;
        }
    } else {
        // document.getElementById("txtstate2").value = "";
        // document.getElementById("txtcity2").value = "";
        // document.getElementById("txtdistrict2").value = "";
        // document.getElementById("txtzip2").value = "";
        // document.getElementById("txtadd3").value = "";
        // document.getElementById("txtadd4").value = "";

    }

}