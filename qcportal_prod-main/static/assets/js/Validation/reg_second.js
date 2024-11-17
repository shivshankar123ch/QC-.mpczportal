//pinCode data fetch
function errorFrom(inp_id){
    let inp = document.getElementById(inp_id);
    if(inp.value == ""){
    let x = document.getElementById(inp_id+"_span");

    x.innerHTML = "Please fill the required details";
    }else{
    let x = document.getElementById(inp_id+"_span");
    x.innerHTML = "";
    }
}

function panNumberValidation(){

    let pan_num = document.getElementById('pan1').value;
    let RegExp_num = new RegExp(/^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/);
    let result = RegExp_num.test(pan_num);

    if (pan_num == "") {
        document.getElementById('panNo').innerHTML = "Please fill the required field ";
        return false;
    } else {
        if (result == false) {
            document.getElementById('panNo').innerHTML = "Pan Number should be in alpha numeric  only.";
            return false;
        }
        else{
            document.getElementById('panNo').innerHTML = "";
        }
    }   
}
function gstNumberValidation(){
    let GST_number = document.getElementById('gst_no').value;
    let gstRGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
    let GST_Result = gstRGEX.test(GST_number);
    if (GST_number == "") {
        document.getElementById('gstNo').innerHTML = "Please fill the GST Number";
        return false;
    } else {
       if (GST_Result == false) {
           document.getElementById('gstNo').innerHTML = " Please fill the valid GST number format";
           return false;
       } else {
           document.getElementById('gstNo').innerHTML = "";
       }
        
    }

}
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
    

    let pan_number = document.getElementById('pan1').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(pan_number);

    let gst_number = document.getElementById('gst_no').value;
    let gstRGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
    let gstResult = gstRGEX.test(gst_number);

    let reg_date = document.getElementById('reg_date').value;

    let address = document.getElementById('txtadd1').value;
    let pin_code= document.getElementById('txtzip').value;
    let district = document.getElementById('txtdistrict').value;
    let state = document.getElementById('txtstate').value;
    let city = document.getElementById('txtcity').value;
   
    let address1 = document.getElementById('txtadd3').value;
    let pin_code1= document.getElementById('txtzip2').value;
    let district1 = document.getElementById('txtdistrict2').value;
    let state1 = document.getElementById('txtstate2').value;
    let city1 = document.getElementById('txtcity2').value;

    
    if (pan_number == "") {
        document.getElementById('panNo').innerHTML = "Please fill the Pan number(ABCTY1234D format) ";
        return false;
    } else {
        
        if (panResult == false) {
            document.getElementById('panNo').innerHTML = "Please fill the valid Pan number(ABCTY1234D format) ";
            return false;
        } else {
            document.getElementById('panNo').innerHTML = "";
        }
    }

    if (gst_number == "") {
        document.getElementById('gstNo').innerHTML = "  Please fill the GST number(11AAAAA1111Z1A1 format) ";
        return false;
    } else {
        if (gstResult == false) {
            document.getElementById('gstNo').innerHTML = "  Please fill the valid GST number(11AAAAA1111Z1A1 format) ";
            return false;
        } else {
            document.getElementById('gstNo').innerHTML = "";
        }
    }

    if (reg_date == "") {
        document.getElementById('reg_date_span').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('reg_date_span').innerHTML = "";
    }


    if (address == "") {
        document.getElementById('txtadd1_span').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('txtadd1_span').innerHTML = "";
    }


    if (pin_code == "") {
        document.getElementById('code').innerHTML = " Please fill the required details";
        return false;
    } else {

        if (pin_code.length != 6) {
            document.getElementById('code').innerHTML = " Please fill the validate pin code";
            return false;
        } else {
            document.getElementById('code').innerHTML = "";
        }
    }

    
    if (district == "") {
        document.getElementById('txtdistrict_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtdistrict_span').innerHTML = "";
    }

    if (state == "") {
        document.getElementById('txtstate_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtstate_span').innerHTML = "";
    }
    if (city == "") {
        document.getElementById('txtcity_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtcity_span').innerHTML = "";
    }

    
    if (address1 == "") {
        document.getElementById('txtadd3_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtadd3_span').innerHTML = "";
    }
    
    if (pin_code1 == "") {
        document.getElementById('code2').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('code2').innerHTML = "";
    }
    if (state1 == "") {
        document.getElementById('txtstate2_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtstate2_span').innerHTML = "";
    }
    if (district1 == "") {
        document.getElementById('txtdistrict2_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('txtdistrict2_span').innerHTML = "";
    }
    
    if (city1 == "") {

        document.getElementById('txtcity2_span').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('txtcity2_span').innerHTML = "";
    }
    if(!confirm("Are you sure you want to submit?")) {
        return false;
      }
      //this.form.submit();
    


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
        document.getElementById("txtstate2").value = "";
        document.getElementById("txtcity2").value = "";
        document.getElementById("txtdistrict2").value = "";
        document.getElementById("txtzip2").value = "";
        document.getElementById("txtadd3").value = "";
        document.getElementById("txtadd4").value = "";

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