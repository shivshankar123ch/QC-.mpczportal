//form validation
// function validateForm() { 
// let mobile =document.getElementById('mobile').value ;
// let RegExp_mobile = /^[6789]\d{9}$/;

// if (mobile == "") {
//     document.getElementById('mobileNumber').innerHTML = "Please fill the required details ";
//     return false;
//     }
//     else{
//       let result = RegExp_mobile.test(mobile_Num.value);
//               if(result == false)
//               {
//                   document.getElementById('mobileNumber').innerHTML = "  Please  enter mobile number should be in valid format. ";
//                   return false;
//                 }else{
//                     document.getElementById('mobileNumber').innerHTML = "";
//                 }
//         }

// return false;
// }
// function validateForm() {
//   let mobile = document.forms["myForm"]["mobile"].value;
//   let phoneNumber = document.getElementById('mobile').value;
//   let phoneRGEX = /^[6789]\d{9}$/;
//   let phoneResult = phoneRGEX.test(phoneNumber);
//   let Captcha = document.forms["myForm"]["captcha"].value;



//     if (mobile == "") {
//           document.getElementById('mobileNumber').innerHTML = "Please fill the required details ";
//           return false;
//       }
//       else{
//             if(phoneResult == false)
//             {
//                 document.getElementById('mobileNumber').innerHTML = "  Please fill the valid Mobile number ";
//                 return false;
//               }else{
//                   document.getElementById('mobileNumber').innerHTML = "";
//               }
//       }
//       if (Captcha == "") {
//         document.getElementById('captchaInput').innerHTML = "Please fill the required details ";
//         return false;
//       }else {
//         document.getElementById('captchaInput').innerHTML = "";
//       }
//       let captcha_number1 = document.getElementById("capt").value;  
//       let capcha_number2 = document.getElementById("textinput").value;
//       if(captcha_number1 !== capcha_number2)  
//         {   
//            document.getElementById('captchaInput').innerHTML = " Captcha Code not match  ";
//            return false;
//         } else{
//              console.log("hh");
//              document.getElementById('captchaInput').innerHTML = "";
//          }
    

// }




//     //Captcha Input
// function cap(){
//       var alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V'
//                    ,'W','X','Y','Z','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i',
//                    'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', '!','@','#','$','%','^','&','*','+'];
//                    var a = alpha[Math.floor(Math.random()*53)];
//                    var b = alpha[Math.floor(Math.random()*53)];
//                    var c = alpha[Math.floor(Math.random()*53)];
//                    var d = alpha[Math.floor(Math.random()*53)];
//                    var e = alpha[Math.floor(Math.random()*53)];
//                    var f = alpha[Math.floor(Math.random()*53)];
  
//                    var final = a+b+c+d+e+f;
//                    document.getElementById("capt").value=final;
//                  }
//                  function validcap(){
//                   var stg1 = document.getElementById('capt').value;
//                   var stg2 = document.getElementById('textinput').value;
//                   if(stg1==stg2){
//                     alert("Form is validated Succesfully");
//                     return true;
//                   }else{
//                     alert("Please enter a valid captcha");
//                     return false;
//                   }
//   }

//   function validate(evt) {
//     var theEvent = evt || window.event;
    
//     // Handle paste
//     if (theEvent.type === 'paste') {
//         key = event.clipboardData.getData('text/plain');
//     } else {
//     // Handle key press
//         var key = theEvent.keyCode || theEvent.which;
//         key = String.fromCharCode(key)
    
//     ;
//     }
//     var regex = /[0-9]|\./;
//     if( !regex.test(key)
    
//     ) {
//       theEvent.returnValue = false;
//       if(theEvent.preventDefault) theEvent.preventDefault();
//     }
//     }
    