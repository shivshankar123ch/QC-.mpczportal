//state,District,Block fetch by Pincode
function setZipInfo() {
    console.log("pin function firee")
    var pin = document.getElementById('txtzip').value;
    var url = `https://api.postalpincode.in/pincode/${pin}`
    console.log("urlll",url)
   fetch(url)
        .then(function (response) {
            console.log("responseeee",response)
            return response.json();
        })
        .then(function (data) {
            console.log("data",data)
            $("#txtstate").val(data[0].PostOffice[0].State);
            console.log("ayeeeeeeeee,",data[0].PostOffice[0].State)
            $("#txtdistrict").val(data[0].PostOffice[0].District);
            $("#txtcity").val(data[0].PostOffice[0].Block);
            $("#txtzip").val(data[0].PostOffice[0].Pincode);

        })
        .catch(function (err) {
            console.log(err)
        //    document.getElementById('code').innerHTML = "  This pincode data are not get..  ";
        //     return false;
        })
}

function setZipInfo2() {
    var pin = document.getElementById('txtzip2').value;
    var url = 'https://api.postalpincode.in/pincode/' + pin;
    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            $("#txtstate2").val(data[0].PostOffice[0].State);
            $("#txtdistrict2").val(data[0].PostOffice[0].District);
            $("#txtcity2").val(data[0].PostOffice[0].Block);
            $("#txtzip2").val(data[0].PostOffice[0].Pincode);

        })
        .catch(function (err) {
            console.log(err)
        })
}
//form validation

function validateForm() {
    var date = document.forms["myForm"]["dob"].value;
    var mobileNumber = document.forms["myForm"]["mobile"].value;
    var addharNum = document.forms["myForm"]["aadhar"].value;
    var addresss1 = document.forms["myForm"]["txtadd5"].value;
    var addresss2 = document.forms["myForm"]["txtadd6"].value;
    var pinCode = document.forms["myForm"]["zip"].value;let  pinregex = /^[1-9]{1}[0-9]{2}\\s{0, 1}[0-9]{3}$/;
    let pinResult = pinregex.test(pinCode);
    var name = document.forms["myForm"]["dir_name"].value;
    var name1 = document.forms["myForm"]["dir_name_hindi"].value;
    var date_1 = document.forms["myForm"]["dir_dob"].value;
    var mobileNumber1 = document.forms["myForm"]["dir_mobile"].value;
    let mobileNumber2 = document.getElementById('dir_mobile').value;
    let mobileRGEX = /^[6789]\d{9}$/;
    let mobileResult = mobileRGEX.test(mobileNumber2);
    var aadahrCard1 = document.forms["myForm"]["dir_aadhar"].value;
    var emails = document.forms["myForm"]["dir_email"].value;
    // console.log(emails);
    var dir_add1 = document.forms["myForm"]["dir_add1"].value;
    var pincode1 = document.forms["myForm"]["txtzip2"].value;

    var state1 = document.forms["myForm"]["state"].value;
    var district1 = document.forms["myForm"]["district"].value;
    var city1 = document.forms["myForm"]["city"].value;

    var state2 = document.forms["myForm"]["dir_state"].value;
    var district2 = document.forms["myForm"]["dir_district"].value;
    var city2 = document.forms["myForm"]["dir_city"].value;


    let phoneNumber = document.getElementById('mobile').value;
    let phoneRGEX = /^[6789]\d{9}$/;
    let phoneResult = phoneRGEX.test(phoneNumber);
    let aadharNumber1 = document.getElementById('aadhar').value;
    let aadharRGEX = /^\d{12}$/;
    // let aadharRGEX1 = /^\d{16}$/;
    // let aadharResult16 = aadharRGEX1.test(aadharNumber1);

    let aadharResult1 = aadharRGEX.test(aadharNumber1);
    let aadharNumber2 = document.getElementById('dir_aadhar').value;
    let aadharResult2 = aadharRGEX.test(aadharNumber2);
    let emailData = document.getElementById('dir_email').value;
    let emailLowerCase = emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult = emailRgex.test(emailLowerCase);
    if (date == "") {
        document.getElementById('birthDate').innerHTML = " Please fill the required details  ";
        return false;
    } else {
        document.getElementById('birthDate').innerHTML = "";
    }
    if (mobileNumber == "") {
        document.getElementById('mob_no').innerHTML = " Please fill the required details ";
        return false;
    } else {
        if(phoneResult == false)
        {
            document.getElementById('mob_no').innerHTML = "  Please fill the valid Mobile number";
            return false;
        }else{
            document.getElementById('mob_no').innerHTML = "";
        }
    }
    if (addharNum == "") {
        document.getElementById('aadhar_no').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('aadhar_no').innerHTML = "";
    }
    if(aadharResult1 == false )
    {
        document.getElementById('aadhar_no').innerHTML = "  Please fill the valid Aadhar number..";
        return false;
    }else{
        document.getElementById('aadhar_no').innerHTML = "";
    }
    if (addresss1 == "") {
        document.getElementById('address1').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        document.getElementById('address1').innerHTML = "";
    }
    // if (addresss2 == "") {
    //     document.getElementById('address2').innerHTML = " Please fill the required details";
    //     return false;
    // }
    // else {
    //     document.getElementById('address2').innerHTML = "";
    // }
    if (pinCode == "") {
        document.getElementById('pin_code1').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('pin_code1').innerHTML = "";
    }
    if (state1 == "") {
        document.getElementById('state_1').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('state_1').innerHTML = "";
    }
    if (district1 == "") {
        document.getElementById('district_1').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('district_1').innerHTML = "";
    }
  
    if (city1 == "") {
        document.getElementById('city_1').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('city_1').innerHTML = "";
    }
    if (name == "") {
        document.getElementById('proName').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('proName').innerHTML = "";
    }
    if (name1 == "") {
        document.getElementById('proName1').innerHTML = "  कृपया नाम भरें.. ";
        return false;
    } else {
        document.getElementById('proName1').innerHTML = "";
    }
    if (date_1 == "") {
        document.getElementById('birthDate_1').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('birthDate_1').innerHTML = "";
    }
    // if (mobileNumber1 == "") {
    //     document.getElementById('mob_no_1').innerHTML = "  Please fill Mobile Number is Required..  ";
    //     return false;
    // }
    // if(mobileNumber1.length != 10) {
    //     document.getElementById('mob_no_1').innerHTML = "  Please fill 10 digit only..  ";
    //     return false;
    // }
    // else {
    //     document.getElementById('mob_no_1').innerHTML = "";
    // }//mobileResult
    if (mobileNumber1 == "") {
        document.getElementById('mob_no_1').innerHTML = " Please fill the required details";
        return false;
    } else {
        //document.getElementById('mob_no_1').innerHTML = "";
        if(mobileResult == false)
        {
            document.getElementById('mob_no_1').innerHTML = "  Please fill the valid Mobile number ";
            return false;
        }else{
            document.getElementById('mob_no_1').innerHTML = "";
        }
    }


    if (emails == "") {
       document.getElementById('email_1').innerHTML = " Please fill the required details ";
       return false;
    }
    else {
       if(emailResult == false)
       {
           document.getElementById('email_1').innerHTML = "  Please fill the valid Email ";
           return false;
       }else{
           document.getElementById('email_1').innerHTML = "";
       }
    }
    if (aadahrCard1 == "") {
        document.getElementById('aadhar_1').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        if(aadharResult2 == false)
        {
            document.getElementById('aadhar_1').innerHTML = "  Please fill the valid Aadhar number ";
            return false;
        }else{
            document.getElementById('aadhar_1').innerHTML = "";
        }
    }
    if (dir_add1 == "") {
        document.getElementById('dir_Add1').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        document.getElementById('dir_Add1').innerHTML = "";
    }
   
    if (pincode1 == "") {
        document.getElementById('pinCode2').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('pinCode2').innerHTML = "";
    }
    if (state2 == "") {
        document.getElementById('state_2').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('state_2').innerHTML = "";
    }
    if (district2 == "") {
        document.getElementById('district_2').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('district_2').innerHTML = "";
    }
    if (city2 == "") {
        document.getElementById('city_2').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('city_2').innerHTML = "";
    }
}
function fill() {
    console.log("function fireeeeeeeeeeeeeee")
    let checkbox = document.getElementById("cbfill");
    console.log("checkedddd")
    let state = document.getElementById("txtstate").value;
    let city = document.getElementById("txtcity").value;
    let zip = document.getElementById("txtzip").value;
    let district = document.getElementById("txtdistrict").value;
    let add1 = document.getElementById("txtadd5").value;
    let add2 = document.getElementById("txtadd6").value;
    let nameE = document.getElementById("auth_name").value;
    let nameH = document.getElementById("auth_name1").value;
    let BirthD = document.getElementById("dob").value;
    let mobile = document.getElementById("mobile").value;
    let email = document.getElementById("email").value;
    let aadhar = document.getElementById("aadhar").value;

    if (checkbox.checked === true) {
        console.log("if me ayeeeeeeeeee")
        document.getElementById("txtstate2").value = state;
        document.getElementById("txtcity2").value = city;
        document.getElementById("txtdistrict2").value = district;
        document.getElementById("txtzip2").value = zip;
        document.getElementById("dir_name").value = nameE;
        document.getElementById("dir_name_hindi").value = nameH;
        document.getElementById("dir_dob").value = BirthD;
        document.getElementById("dir_mobile").value = mobile;
        document.getElementById("dir_email").value = email;
        document.getElementById("dir_aadhar").value = aadhar;


        let add3 = document.getElementById("txtadd1").value = add1;
        document.getElementById("txtadd2").value = add2;
        if(add1 === add3){
            add1 = add3;
        }
        let txt_add2 = document.getElementById("txtadd2").value;
        let txt_add4 = document.getElementById("txtadd2").value;
        if(txt_add2 === txt_add4){
            txt_add2 = txt_add4;
        }
        let txt_nameE1 = document.getElementById("auth_name").value;
        let txt_nameE2 = document.getElementById("dir_name").value;

        let txt_nameH1 = document.getElementById("auth_name1").value;
        let txt_nameH2 = document.getElementById("dir_name_hindi").value;

        let txt_email1 = document.getElementById("email").value;
        let txt_email2 = document.getElementById("dir_email").value;

        let txt_birth1 = document.getElementById("dob").value;
        let txt_birth2 = document.getElementById("dir_dob").value;

        let txt_mobile1 = document.getElementById("mobile").value;
        let txt_mobile2 = document.getElementById("dir_mobile").value;

        let txt_aadhar1 = document.getElementById("aadhar").value;
        let txt_aadhar2 = document.getElementById("dir_aadhar").value;



        let txt_zip1 = document.getElementById("txtzip").value;
        let txt_zip2 = document.getElementById("txtzip2").value;
        let txt_city = document.getElementById("txtcity").value;
        let txt_city2 = document.getElementById("txtcity2").value;
        let txt_state = document.getElementById("txtstate").value;
        let txt_state2 = document.getElementById("txtstate2").value;
        let txt_district = document.getElementById("txtdistrict").value;
        let txt_district2 = document.getElementById("txtdistrict2").value;
        if(txt_zip1 === txt_zip2){
            txt_zip1 = txt_zip2;
            txt_city = txt_city2;
            txt_state = txt_state2;
            txt_district = txt_district2;
        }

    } else {
        

    }

}

//hindi & English Typing
function englishTyping(){
        pramukhIME.addLanguage(PramukhIndic);
        pramukhIME.enable();
        pramukhIME.onLanguageChange(scriptChangeCallback);
        var lang = (getCookie('pramukhime_language','pramukhindic:English')).split(':');
        //console.log(lang);
        pramukhIME.setLanguage(lang[1], lang[0]);
        }
        document.getElementsByClassName('text1').focus();
    function hindiTyping(){
          pramukhIME.addLanguage(PramukhIndic);
          pramukhIME.enable();
          pramukhIME.onLanguageChange(scriptChangeCallback);
          var lang = (getCookie('pramukhime_language','pramukhindic:Hindi')).split(':');
          //console.log(lang);
          pramukhIME.setLanguage(lang[1], lang[0]);
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
