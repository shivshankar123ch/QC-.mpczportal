//state,District,Block fetch by Pincode

function setZipInfo(int_id) {
    var pin = document.getElementById(int_id).value;
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
function mobileValidation(inp_id){
    let mobileNumber = document.getElementById(inp_id);
    let mobileRGEX = /^[6789]\d{9}$/;
    let mobileResult = mobileRGEX.test(mobileNumber.value);
    let val = document.getElementById(inp_id+"_span");

    if (mobileNumber.value == "") {
        val.innerHTML = " Please fill the required details ";
        return false;
    } else {
        if(mobileResult == false)
        {
           val.innerHTML = "  Please fill the valid Mobile number";
            
        }else{
           val.innerHTML = "";
        }
    }

}
function aadharValidation(inp_id){
    let aadharNumber = document.getElementById(inp_id);
    let aadharRGEX = /^\d{12}$/;
    let aadharResult = aadharRGEX.test(aadharNumber.value);
    let val = document.getElementById(inp_id+"_span");

    if (aadharNumber.value == "") {
        val.innerHTML = " Please fill the required details ";
        return false;
    } else {
        if(aadharResult == false)
        {
           val.innerHTML = "Adhar number should be in number and 12 digit only.";
           
        }else{
           val.innerHTML = "";
        }
    }

}
function emailValidation(){
    let dir_emailData = document.getElementById('dir_email').value;
    let emailLowerCase = dir_emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let dir_emailResult = emailRgex.test(emailLowerCase);
    if (dir_email == "") {
        document.getElementById('dir_email_span').innerHTML = " Please fill the required details ";
        return false;
     }
     else {
        if(dir_emailResult == false){
            document.getElementById('dir_email_span').innerHTML = "  Please fill the valid Email ";
            return false;
        }else{
            document.getElementById('dir_email_span').innerHTML = "";
        }
     }

}
//form validation

function validateForm() {
    
    let mobileNumber = document.getElementById('mobile').value;
    let mobileRGEX = /^[6789]\d{9}$/;
    let mobileResult = mobileRGEX.test(mobileNumber);

    let date_of_birth = document.getElementById("dob").value;

    let aadharNumber = document.getElementById('aadhar').value;
    let aadharRGEX = /^\d{12}$/;
    let aadharResult = aadharRGEX.test(aadharNumber);

    let address = document.getElementById('txtadd5').value;
    let pin_code= document.getElementById('txtzip').value;
    let district = document.getElementById('txtdistrict').value;
    let state = document.getElementById('txtstate').value;
    let city = document.getElementById('txtcity').value;



    let dir_name = document.getElementById('dir_name').value;
    let nameRegExp = new RegExp(/^[A-Za-z ]+$/);
    let dir_nameResult = nameRegExp.test(dir_name);

    let dir_name_h = document.getElementById('dir_name_hindi').value;

    let dir_dob = document.getElementById('dir_dob').value;

    let dir_mobile = document.getElementById('dir_mobile').value;
    let dir_mobileResult = mobileRGEX.test(dir_mobile);

    let dir_emailData = document.getElementById('dir_email').value;
    let emailLowerCase = dir_emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let dir_emailResult = emailRgex.test(emailLowerCase);

    let dir_aadher = document.getElementById('dir_aadhar').value;
    let dir_aadharResult = aadharRGEX.test(dir_aadher);

    let address1 = document.getElementById('txtadd1').value;
    let pin_code1= document.getElementById('txtzip2').value;
    let district1 = document.getElementById('txtdistrict2').value;
    let state1 = document.getElementById('txtstate2').value;
    let city1 = document.getElementById('txtcity2').value;

    if (mobileNumber == "") {
        document.getElementById('mobile_span').innerHTML = " Please fill the required details ";
        return false;
    } else {
        if(mobileResult == false)
        {
            document.getElementById('mobile_span').innerHTML = "  Please fill the valid Mobile number";
            //phoneResult.focus();
            return false;
        }else{
            document.getElementById('mobile_span').innerHTML = "";
        }
    }
    if (date_of_birth == "") {
        document.getElementById('dob_span').innerHTML = " Please fill the required details  ";
        
        return false;
    } else {
        document.getElementById('dob_span').innerHTML = "";
    }
    
    if(aadharNumber == ""){
        document.getElementById('aadhar_span').innerHTML = " Please fill the required details  ";
        return false;

     } else{
            if (aadharResult == false) {
                document.getElementById('aadhar_span').innerHTML = "Adhar number should be in number and 12 digit only.";
                return false;
            }
            else{
                document.getElementById('aadhar_span').innerHTML = "";
             }

    }
    
    if (address == "") {
        document.getElementById('txtadd5_span').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        document.getElementById('txtadd5_span').innerHTML = "";
    }
   
    if (pin_code == "") {
        document.getElementById('pin_code1').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('pin_code1').innerHTML = "";
    }

   
    if (state == "") {
        document.getElementById('txtstate_span').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('txtstate_span').innerHTML = "";
    }
    if (district == "") {
        document.getElementById('txtdistrict_span').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('txtdistrict_span').innerHTML = "";
    }
  
    if (city == "") {
        document.getElementById('txtcity_span').innerHTML = " Please fill the required details  ";
        return false;
    }
    else {
        document.getElementById('txtcity_span').innerHTML = "";
    }


    if (dir_name == "") {
        document.getElementById('dir_name_span').innerHTML = " Please fill the required details";
        return false;
    } else {

            if(dir_nameResult == false)
            {
                document.getElementById('dir_name_span').innerHTML = "  Please fill the valid Aadhar number ";
                return false;
            }else{
                document.getElementById('dir_name_span').innerHTML = "";
            }
        }
        
    

    if (dir_name_h == "") {
        document.getElementById('dir_name_hindi_span').innerHTML = "  कृपया नाम भरें.. ";
        return false;
    } else {
        document.getElementById('dir_name_hindi_span').innerHTML = "";
    }

    if (dir_dob == "") {
        document.getElementById('dir_dob_span').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('dir_dob_span').innerHTML = "";
    }
   
    if (dir_mobile == "") {
        document.getElementById('dir_mobile_span').innerHTML = " Please fill the required details";
        return false;
    } else {
       
        if(dir_mobileResult == false)
        {
            document.getElementById('dir_mobile_span').innerHTML = "  Please fill the valid Mobile number ";
            return false;
        }else{
            document.getElementById('dir_mobile_span').innerHTML = "";
        }
    }


    if (dir_email == "") {
       document.getElementById('dir_email_span').innerHTML = " Please fill the required details ";
       return false;
    }
    else {
       if(dir_emailResult == false){
           document.getElementById('dir_email_span').innerHTML = "  Please fill the valid Email ";
           return false;
       }else{
           document.getElementById('dir_email_span').innerHTML = "";
       }
    }

    if (dir_aadher == "") {
        document.getElementById('dir_aadhar_span').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        if(dir_aadharResult == false)
        {
            document.getElementById('dir_aadhar_span').innerHTML = "  Please fill the valid Aadhar number ";
            return false;
        }else{
            document.getElementById('dir_aadhar_span').innerHTML = "";
        }
    }
    
    if (address1 == "") {
        document.getElementById('txtadd1_span').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        document.getElementById('txtadd1_span').innerHTML = "";
    }
   
    if (pin_code1 == "") {
        document.getElementById('pinCode2').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('pinCode2').innerHTML = "";
    }

    if (state1 == "") {
        document.getElementById('txtstate2_span').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('txtstate2_span').innerHTML = "";
    }

    if (district1 == "") {
        document.getElementById('txtdistrict2_span').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('txtdistrict2_span').innerHTML = "";
    }

    if (city1 == "") {
        document.getElementById('txtcity2_span').innerHTML = "Please fill the required details ";
        return false;
    }
    else {
        document.getElementById('txtcity2_span').innerHTML = "";
    }
    if(!confirm("Are you sure you want to submit?")) {
        return false;
    }
    this.form.submit();
    

}


function fill() {    
    let checkbox = document.getElementById("cbfill");
    let state = document.getElementById("txtstate").value;
    let city = document.getElementById("txtcity").value;
    let zip = document.getElementById("txtzip").value;
    let district = document.getElementById("txtdistrict").value;
    let add1 = document.getElementById("txtadd5").value;
    let add2 = document.getElementById("txtadd6").value;
    let nameE = document.getElementById("auth_naame").value;
    let nameH = document.getElementById("auth_name1").value;
    let BirthD = document.getElementById("dob").value;
    let mobile = document.getElementById("mobile").value;
    let email = document.getElementById("email").value;   
    // let aadhar = document.getElementById("aadhar").value; 
    if (checkbox.checked === true) { 
        document.getElementById("txtstate2").value = state;
        document.getElementById("txtcity2").value = city;
        document.getElementById("txtdistrict2").value = district;
        document.getElementById("txtzip2").value = zip;
        document.getElementById("dir_name").value = nameE;
        document.getElementById("dir_name_hindi").value = nameH;
        document.getElementById("dir_dob").value = BirthD;
        document.getElementById("dir_mobile").value = mobile;       
        document.getElementById("dir_email").value = email; 
        // document.getElementById("dir_aadhar").value = aadhar;  
 

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
        // let txt_aadhar2 = document.getElementById("dir_aadhar").value;



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
        document.getElementById("txtadd1").value = "";
        document.getElementById("txtadd2").value = "";
        document.getElementById("txtstate2").value = "";
        document.getElementById("txtcity2").value = "";
        document.getElementById("txtdistrict2").value = "";
        document.getElementById("txtzip2").value = "";
        document.getElementById("dir_name").value = "";
        document.getElementById("dir_name_hindi").value = "";
        document.getElementById("dir_dob").value = "";
        document.getElementById("dir_mobile").value = "";
        document.getElementById("dir_email").value = "";
        // document.getElementById("dir_aadhar").value = "";

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
       
        function hindiTyping(){
          pramukhIME.addLanguage(PramukhIndic);
          pramukhIME.enable();
          pramukhIME.onLanguageChange(scriptChangeCallback);
          var lang = (getCookie('pramukhime_language','pramukhindic:Hindi')).split(':');
          //console.log(lang);
          pramukhIME.setLanguage(lang[1], lang[0]);
    }

    
