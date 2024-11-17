
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
function mobileValidation(){
    let mobile_Num = document.getElementById("mobile1");
    let RegExp_mobile = /^[6789]\d{9}$/;
    if(mobile_Num.value == ""){
        document.getElementById('mobile_number').innerHTML = "Please fill the company name ";
        return false;

    }else{
        let result = RegExp_mobile.test(mobile_Num.value);
        if (result == false) {
           
            document.getElementById('mobile_number').innerHTML = "Please fill mobile number should be in valid number.";
            return false;
        }
        else{
            document.getElementById('mobile_number').innerHTML = "";

        }
    }

}
function emailvalidate(){
    let user_email = document.getElementById('email1').value;
    let emailLowerCase = user_email.toLowerCase();
    let RegExp_email = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if(user_email == ""){
        document.getElementById('email_address').innerHTML = "Please fill the Email ";
        return false;
    }else{
        let result = RegExp_email.test(emailLowerCase);
        if (result == false) {
            document.getElementById('email_address').innerHTML = " Please enter email should be in valid format.";
            return false;
        } else {
                document.getElementById('email_address').innerHTML = "";
                }
    }

}

function validateFrom(){
    
   
    let companyName_e = document.getElementById("company_name_e");
    let name_of_authorized_e = document.getElementById("name_of_authorized_e");
    let RegExp_name = new RegExp(/^[A-Za-z ]+$/);
    let mobile_Num = document.getElementById("mobile1");
    let RegExp_mobile = /^[6789]\d{9}$/;
  
    let user_email = document.getElementById('email1').value;
    let emailLowerCase = user_email.toLowerCase();
    
    let RegExp_email = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    var Captcha = document.getElementById('capt').value;
    var Enter_captcha = document.getElementById('textinput').value;


    if(companyName_e.value == ""){
        document.getElementById("companyname").innerHTML="Please fill the company name";
        return false;
        
    }else{
       
            document.getElementById('companyname').innerHTML = "";
    } 

    if(name_of_authorized_e.value == ""){
        document.getElementById("authorized_person").innerHTML="Please fill the authorized person name";
        return false;
     } else{
        let result = RegExp_name.test(name_of_authorized_e.value);
        if (result == false) {
            document.getElementById('authorized_person').innerHTML = "Authorized Person should be in letter only.";
           
            return false;
        }
        else{
            document.getElementById('authorized_person').innerHTML = "";
        }
    }
    if(mobile_Num.value == ""){

            document.getElementById('mobile_number').innerHTML = "Please fill the mobile number ";
            return false;
    
        }else{
            let result = RegExp_mobile.test(mobile_Num.value);
            if (result == false) {
               
                document.getElementById('mobile_number').innerHTML = "Please fill mobile number should be in valid number.";
                return false;
            }
            else{
                document.getElementById('mobile_number').innerHTML = "";
    
            }
        }
    
    if(user_email == ""){
        document.getElementById('email_address').innerHTML = "Please fill the Email ";
        return false;
    }else{
        let result = RegExp_email.test(emailLowerCase);
        if (result == false) {
            document.getElementById('email_address').innerHTML = " Please enter email should be in valid format.";
            return false;
        } else {
                document.getElementById('email_address').innerHTML = "";
                }
    }

    if (Enter_captcha == "") {
           document.getElementById('captchaInput').innerHTML = "Please fill the required details";
            return false;
        } 
    
    if (Captcha != Enter_captcha) {
        document.getElementById('captchaInput').innerHTML = "Please enter a valid captcha";
        return false;
    } 
    if(!confirm("Are you sure you want to submit?")) {
        return false;
    }
    //this.form.submit();

}
    


function cap() {
    console.log("fire thefgfdgdf function")
    var alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '@', '#', '$', '%', '^', '&', '*', '+'
    ];
    var a = alpha[Math.floor(Math.random() * 53)];
    var b = alpha[Math.floor(Math.random() * 53)];
    var c = alpha[Math.floor(Math.random() * 53)];
    var d = alpha[Math.floor(Math.random() * 53)];
    var e = alpha[Math.floor(Math.random() * 53)];
    var f = alpha[Math.floor(Math.random() * 53)];

    var final = a + b + c + d + e + f;
    document.getElementById("capt").value = final;
}

