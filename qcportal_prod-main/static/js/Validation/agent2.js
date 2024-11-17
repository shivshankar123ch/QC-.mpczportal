

console.log("123");
function validateForm() {
    console.log("function fireee")
    let Company_1 = document.forms["myForm"]["one"].value;
    if (Company_1 == "") {
        document.getElementById('Company_1').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('Company_1').innerHTML = " ";
    }
    let V_upload_file_ele = document.forms["myForm"]["two"].value;
    var fileInput1 = document.getElementById('v_upload_file_1').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);
    if (V_upload_file_ele == "") {
        document.getElementById('Company_2').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result1 == false) {
            document.getElementById('Company_2').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_1").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Company_2").value = "";
                return false

            } else {
                document.getElementById('Company_2').innerHTML = "";
            }


        }
    }
    let Company_3 = document.forms["myForm"]["three"].value;
    if (Company_3 == "") {
        document.getElementById('Company_3').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('Company_3').innerHTML = " ";
    }
    let Company_4 = document.forms["myForm"]["four"].value;
    var fileInput2 = document.getElementById('v_upload_file_2').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);
    if (Company_4 == "") {
        document.getElementById('Company_4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result2 == false) {
            document.getElementById('Company_4').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Company_2").value = "";
                return false

            } else {
                document.getElementById('Company_4').innerHTML = "";
            }


        }
    }
    // let pan = document.forms["myForm"]["five"].value;
    // if (pan == "") {
    //     document.getElementById('Company_5').innerHTML = " Please fill the required field.  ";
    //     return false;
    // } else {
    //     document.getElementById('Company_5').innerHTML = " ";
    // }
    let pan= document.forms["myForm"]["five"].value;
    let panNumber = document.getElementById('v_p_reg_number_6').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);
    if (pan == "") {
        document.getElementById('Company_5').innerHTML = "  Please fill the Pan number(ABCTY1234D format) ";
        return false;
    } else {
        //document.getElementById('panNo').innerHTML = "";
        if (panResult == false) {
            document.getElementById('Company_5').innerHTML = "  Please fill the valid Pan number(ABCTY1234D format) ";
            return false;
        } else {
            document.getElementById('Company_5').innerHTML = "";
        }
    }
    let panfile= document.forms["myForm"]["six"].value;
    var fileInput3 = document.getElementById('v_upload_file_3').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);
    if (panfile == "") {
        document.getElementById('Company_6').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result3 == false) {
            document.getElementById('Company_6').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_3").value = "";
                return false

            } else {
                document.getElementById('Company_6').innerHTML = "";
            }


        }
    }
    let Company_7 = document.forms["myForm"]["seven"].value;
    if (Company_7 == "") {
        document.getElementById('Company_7').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('Company_7').innerHTML = " ";
    }
    let Company_8= document.forms["myForm"]["six"].value;
    var fileInput4 = document.getElementById('v_upload_file_4').value;
    let fileInput_Result4 = allowedExtensions.test(fileInput4);
    if (Company_8 == "") {
        console.log("99999");
        document.getElementById('Company_8').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        console.log("999991");
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result4 == false) {
            document.getElementById('Company_8').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            console.log("99993");
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_4").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_4").value = "";
                return false

            } else {
                document.getElementById('Company_8').innerHTML = "";
            }


        }
    }
    var aadahrCard1 = document.forms["myForm"]["nine"].value;
    let aadharNumber1 = document.getElementById('adh_reg_number').value;
    let aadharRGEX = /^\d{12}$/;
    // let aadharRGEX1 = /^\d{16}$/;
    // let aadharResult16 = aadharRGEX1.test(aadharNumber1);

    let aadharResult1 = aadharRGEX.test(aadharNumber1);
    if (aadahrCard1 == "") {
        document.getElementById('Company_9').innerHTML = " Please fill the required details";
        return false;
    }
    else {
        if(aadharResult1 == false)
        {
            document.getElementById('Company_9').innerHTML = "  Please fill the valid Aadhar number ";
            return false;
        }else{
            document.getElementById('Company_9').innerHTML = "";
        }
    }
    let Company_10= document.forms["myForm"]["ten"].value;
    var fileInput5 = document.getElementById('v_upload_file_5').value;
    let fileInput_Result5 = allowedExtensions.test(fileInput5);
    if (Company_10 == "") {
        console.log("99999");
        document.getElementById('Company_10').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        console.log("999991");
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result5 == false) {
            document.getElementById('Company_10').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            console.log("99993");
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_5").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_5").value = "";
                return false

            } else {
                document.getElementById('Company_10').innerHTML = "";
            }


        }
    }
    let Company_11 = document.forms["myForm"]["eleven"].value;
    if (Company_11 == "") {
        document.getElementById('Company_11').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('Company_11').innerHTML = " ";
    }
    let Company_12= document.forms["myForm"]["twelve"].value;
    var fileInput6 = document.getElementById('v_upload_file_6').value;
    let fileInput_Result6 = allowedExtensions.test(fileInput5);
    if (Company_12 == "") {
        console.log("99999");
        document.getElementById('Company_12').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        console.log("999991");
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result6 == false) {
            document.getElementById('Company_12').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            console.log("99993");
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_6").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_6").value = "";
                return false

            } else {
                document.getElementById('Company_12').innerHTML = "";
            }


        }
    }
    let issueDate = document.forms["myForm"]["fifteen"].value;
    if (issueDate == "") {
        document.getElementById('issueDate').innerHTML = " Please fill the required field.  ";
        return false;
    } else {
        document.getElementById('issueDate').innerHTML = " ";
    }
    let Company_13= document.forms["myForm"]["sixteen"].value;
    if (Company_13 == "") {
        console.log("99999");
        document.getElementById('Company_13').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        console.log("999991");
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result6 == false) {
            document.getElementById('Company_13').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            console.log("99993");
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_7").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_7").value = "";
                return false

            } else {
                document.getElementById('Company_13').innerHTML = "";
            }


        }
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