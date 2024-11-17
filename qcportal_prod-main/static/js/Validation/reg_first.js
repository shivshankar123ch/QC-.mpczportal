// //english and hindi typing
//     function englishTyping(){
//         pramukhIME.addLanguage(PramukhIndic);
//         pramukhIME.enable();
//         pramukhIME.onLanguageChange(scriptChangeCallback);
//         var lang = (getCookie('pramukhime_language','pramukhindic:English')).split(':');
//         console.log(lang);
//         pramukhIME.setLanguage(lang[1], lang[0]);
//     }
//     document.getElementsByClassName('text1').focus();
//     function hindiTyping(){
//       pramukhIME.addLanguage(PramukhIndic);
//       pramukhIME.enable();
//       pramukhIME.onLanguageChange(scriptChangeCallback);
//       var lang = (getCookie('pramukhime_language','pramukhindic:Hindi')).split(':');
//       console.log(lang);
//       pramukhIME.setLanguage(lang[1], lang[0]);
//     }

//form validation
console.log("hiii123");
function validateForm() {
    let slect1 = document.forms["myForm"]["user"].value;
    let slect2 = document.forms["myForm"]["zone"].value;

    let slect3 = document.forms["myForm"]["service_type"].value;

    let companyName_e = document.forms["myForm"]["company_name_e"].value;
    let companyName_h = document.forms["myForm"]["company_name_h"].value;
    let Name_of_authorized_e = document.forms["myForm"]["name_of_authorized_e"].value;
    let Name_of_authorized_h = document.forms["myForm"]["name_of_authorized_h"].value;
    let mobile_number = document.forms["myForm"]["mobile"].value;
    let email_address = document.forms["myForm"]["email"].value;
    // let Service_type = document.forms["myForm"]["service_type"].value;
    let Captcha = document.forms["myForm"]["captcha"].value;
    let sector = document.forms["myForm"]["firm"].value;
    let g = document.forms["myForm"]["captcha1"].value;
    let phoneNumber = document.getElementById('mobile1').value;
    let phoneRGEX = /^[6789]\d{9}$/;
    let phoneResult = phoneRGEX.test(phoneNumber);
    let emailData = document.getElementById('email1').value;
    let emailLowerCase = emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult = emailRgex.test(emailLowerCase);


    if (sector == "") {
        document.getElementById('Firm').innerHTML = " Please fill the required details";
    } else {
        document.getElementById('Firm').innerHTML = "";
    }

    // if (Service_type == "") {
    //     document.getElementById('firmName1').innerHTML = " Please fill the required details      //     return false;
    // }else {
    //     document.getElementById('firmName1').innerHTML = "";
    // }
    if (slect1 == "") {
        document.getElementById('User').innerHTML = " Please fill the required details";
        return false;
    } else {
        //alert("hiii ns");
        document.getElementById('User').innerHTML = "";
    }
    if (slect2 == "") {
        document.getElementById('Zone').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('Zone').innerHTML = "";
    }
    if (slect3 == "") {
        document.getElementById('firmName1').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('firmName1').innerHTML = "";
    }
    if (companyName_e == "") {
        document.getElementById('companyNameEnglish').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('companyNameEnglish').innerHTML = "";
    }
    if (companyName_h == "") {
        document.getElementById('companyNameHindi').innerHTML = " ** कृपया कंपनी का नाम भरें.. ";
        return false;
    } else {
        document.getElementById('companyNameHindi').innerHTML = "";
    }
    if (Name_of_authorized_e == "") {
        document.getElementById('nameOfAauthorizedEnglish').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('nameOfAauthorizedEnglish').innerHTML = "";
    }
    if (Name_of_authorized_h == "") {
        document.getElementById('nameOfAauthorizedHindi').innerHTML = " कृपया अधिकृत का नाम भरें";
        return false;
    } else {
        document.getElementById('nameOfAauthorizedHindi').innerHTML = "";
    }
    if (mobile_number == "") {
        document.getElementById('mobileNumber').innerHTML = " Please fill the required details";
        return false;
    } else {
        if (phoneResult == false) {
            document.getElementById('mobileNumber').innerHTML = " Please fill the required details";
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
    if (Captcha == "") {
        document.getElementById('captchaInput').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('captchaInput').innerHTML = "";
    }
    let captcha_number1 = document.getElementById("capt").value;
    let capcha_number2 = document.getElementById("textinput").value;
    if (captcha_number1 !== capcha_number2) {
        document.getElementById('captchaInput').innerHTML = " Captcha Code not match";
        return false;
    } else {
        console.log("hh");
        document.getElementById('captchaInput').innerHTML = "";
    }
}

//Captcha Input
function cap() {
    console.log("fire the function")
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

function validcap() {
    var stg1 = document.getElementById('capt').value;
    var stg2 = document.getElementById('textinput').value;
    if (stg1 == stg2) {
        alert("Form is validated Succesfully");
        return true;
    } else {
        alert("Please enter a valid captcha");
        return false;
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