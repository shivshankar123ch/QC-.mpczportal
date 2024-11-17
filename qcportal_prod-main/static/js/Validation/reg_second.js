//pinCode data fetch
function setZipInfo() {
    var pin = document.getElementById('txtzip').value;
    var url = 'https://api.postalpincode.in/pincode/' + pin

    fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            $("#txtstate").val(data[0].PostOffice[0].State);
            $("#txtdistrict").val(data[0].PostOffice[0].District);
            $("#txtcity").val(data[0].PostOffice[0].Block);
            $("#txtzip").val(data[0].PostOffice[0].Pincode);

        })
        .catch(function(err) {
            console.log(err)
                // document.getElementById('code').innerHTML = "  This pincode data are not get..  ";
                // return false;

        })
}

function setZipInfo2() {
    var pin = document.getElementById('txtzip2').value;
    var url = 'https://api.postalpincode.in/pincode/' + pin

    fetch(url)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            $("#txtstate2").val(data[0].PostOffice[0].State);
            $("#txtdistrict2").val(data[0].PostOffice[0].District);
            $("#txtcity2").val(data[0].PostOffice[0].Block);
            $("#txtzip2").val(data[0].PostOffice[0].Pincode);

        })
        .catch(function(err) {
            console.log(err)
                //  document.getElementById('code2').innerHTML = "  This pincode data are not get..  ";
                //  return false;

        })
}


//form valiadtion
function validateForm() {
    let fax_data = document.forms["myForm"]["fax"].value;
    let faxNumber = document.getElementById('fax').value;
    let faxRGEX = /^(\+?\d{1,}(\s?|\-?)\d*(\s?|\-?)\(?\d{2,}\)?(\s?|\-?)\d{3,}\s?\d{3,})$/;
    let faxResult = faxRGEX.test(faxNumber);
    let pan_data = document.forms["myForm"]["pan"].value;
    let Reg_no = document.forms["myForm"]["reg_no"].value;
    let gst_data = document.forms["myForm"]["gst"].value;
    let gstNumber = document.getElementById('gst_no').value;
    let gstRGEX = /^([0-9]){2}([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}([0-9]){1}([a-zA-Z]){1}([0-9]){1}?$/;
    let gstResult = gstRGEX.test(gstNumber);
    let Reg_date = document.forms["myForm"]["reg_date"].value;
    let Add1 = document.forms["myForm"]["add1"].value;
    let Add2 = document.forms["myForm"]["add2"].value;
    let pinCode = document.forms["myForm"]["zip"].value;
    let district = document.forms["myForm"]["add3"].value;
    let state = document.forms["myForm"]["add4"].value;
    let city = document.forms["myForm"]["city"].value;


    let add5 = document.forms["myForm"]["add5"].value;
    let add6 = document.forms["myForm"]["add6"].value;

    let pinCode2 = document.forms["myForm"]["zip2"].value;

    let district2 = document.forms["myForm"]["add8"].value;
    let state2 = document.forms["myForm"]["add7"].value;
    let city2 = document.forms["myForm"]["city2"].value;


    let pin_Code = document.getElementById('txtzip').value;
    let panNumber = document.getElementById('pan1').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);
    //let d = document.forms["myForm"]["add1"].value;

    if (pan_data == "") {
        document.getElementById('panNo').innerHTML = "  Please fill the Pan number(ABCTY1234D format) ";
        return false;
    } else {
        //document.getElementById('panNo').innerHTML = "";
        if (panResult == false) {
            document.getElementById('panNo').innerHTML = "  Please fill the valid Pan number(ABCTY1234D format) ";
            return false;
        } else {
            document.getElementById('panNo').innerHTML = "";
        }
    }

    if (Reg_no == "") {
        document.getElementById('gumastaNo').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('gumastaNo').innerHTML = "";
    }
    if (gst_data == "") {
        document.getElementById('gstNo').innerHTML = "  Please fill the GST number(11AAAAA1111Z1A1 format) ";
        return false;
    } else {
        document.getElementById('gstNo').innerHTML = "";
        // if (gstResult == false) {
        //     document.getElementById('gstNo').innerHTML = "  Please fill the valid GST number(11AAAAA1111Z1A1 format) ";
        //     return false;
        // } else {
        //     document.getElementById('gstNo').innerHTML = "";
        // }
    }
    if (Reg_date == "") {
        document.getElementById('regDate').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('regDate').innerHTML = "";
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
    // if (add6 == "") {
    //     document.getElementById('txt_add4').innerHTML = "  Please fill the Company Address..";
    //     return false;
    // }else {
    //     document.getElementById('txt_add4').innerHTML = "";
    // }
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
    // if (state2 == "") {
    //     document.getElementById('state_2').innerHTML = "Please fill the required details";
    //     return false;
    // } else {
    //     document.getElementById('state_2').innerHTML = "";
    // }
    if (city2 == "") {

        document.getElementById('city_2').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('city_2').innerHTML = "";
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