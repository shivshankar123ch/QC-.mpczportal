///form Validation
function validateForm() {
    let Name_office = document.forms["myForm"]["name_office"].value;
    let V_supply_criteria = document.forms["myForm"]["seven"].value;
    let V_upload_file_ele = document.forms["myForm"]["eight"].value;
    var fileInput1 = document.getElementById('v_upload_file_ele').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);


    let V_file_upload_elev = document.forms["myForm"]["nine"].value; //start here
    var fileInput2 = document.getElementById('v_file_upload_elev').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);

    let V_upload_file_eleve = document.forms["myForm"]["ten"].value;
    var fileInput3 = document.getElementById('v_upload_file_eleve').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);

    let V_file_upload_eleven = document.forms["myForm"]["eleven"].value;
    var fileInput4 = document.getElementById('v_file_upload_eleven').value;
    let fileInput_Result4 = allowedExtensions.test(fileInput4);


    let bsi = document.forms["myForm"]["thirteen"].value;
    var fileeee = document.getElementById('v_upload_se1').value;
    let fileInput_Result21 = allowedExtensions.test(fileeee);


    let V_upload_eight = document.forms["myForm"]["fifteen"].value;
    var fileInput6 = document.getElementById('upload_eight').value;
    let fileInput_Result6 = allowedExtensions.test(fileInput6);

    let V_product_nine = document.forms["myForm"]["eighteen"].value;
    let V_method_ten = document.forms["myForm"]["nineteen"].value;
    var fileInput7 = document.getElementById('v_upload_ten').value;
    let fileInput_Result7 = allowedExtensions.test(fileInput7);


    let V_upload_ten = document.forms["myForm"]["twenty"].value;
    let V_eleven_upload_one = document.forms["myForm"]["twenty_one"].value;
    var fileInput9 = document.getElementById('v_eleven_upload_one').value;
    let fileInput_Result9 = allowedExtensions.test(fileInput9);

    let V_office_list_two = document.forms["myForm"]["v_office_list_two"].value;
    let V_upload_file_two = document.forms["myForm"]["twenty_three"].value;
    var fileInput10 = document.getElementById('v_upload_file_two').value;
    let fileInput_Result10 = allowedExtensions.test(fileInput10);

    let data14 = document.forms["myForm"]["twenty_four"].value;
    let V_eleven_upload_one_89 = document.forms["myForm"]["twenty_five_90"].value;
    var fileInput20 = document.getElementById('Twenty_five').value;
    let fileInput_Result20 = allowedExtensions.test(fileInput20);

    // let data16 = document.forms["myForm"]["Twenty_seven"].value;

    let twenty_five_file = document.forms["myForm"]["Twenty_seven"].value;
    var fileInput22 = document.getElementById('Twenty_seven').value;
    let fileInput_Result22 = allowedExtensions.test(fileInput22);


    // let data18 = document.forms["myForm"]["Twenty_eight"].value;

    let data19 = document.forms["myForm"]["twenty_five_901"].value;
    var fileInput25 = document.getElementById('Twenty_nineteen2').value;
    let fileInput_Result25 = allowedExtensions.test(fileInput25);



    if (Name_office == "") {

        document.getElementById('Name_office').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('Name_office').innerHTML = "";
    }
    if (V_supply_criteria == "") {
        document.getElementById('V_supply_criteria').innerHTML = "  Please fill the required detail ";
        return false;
    } else {
        document.getElementById('V_supply_criteria').innerHTML = "";
    }
    if (V_upload_file_ele == "") {
        document.getElementById('V_upload_file_ele').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result1 == false) {
            document.getElementById('V_upload_file_ele').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_upload_file_ele').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_ele").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_ele").value = "";
                return false;

            } else {
                document.getElementById('V_upload_file_ele').innerHTML = "";
            }


        }
    }
    if (V_file_upload_elev == "") {
        document.getElementById('V_file_upload_elev').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (fileInput_Result2 == false) {
            document.getElementById('V_file_upload_elev').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            // document.getElementById('V_file_upload_elev').innerHTML = "";
            const oFile = document.getElementById("v_file_upload_elev").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_file_upload_elev").value = "";
                return false;

            } else {
                document.getElementById('V_file_upload_elev').innerHTML = "";
            }
        }
    }

    if (V_upload_file_eleve == "") {
        document.getElementById('V_upload_file_eleve').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (fileInput_Result3 == false) {
            document.getElementById('V_upload_file_eleve').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_upload_file_eleve').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_eleve").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_eleve").value = "";
                return false;

            } else {
                document.getElementById('V_upload_file_eleve').innerHTML = "";
            }
        }
    }
    if (V_file_upload_eleven == "") {
        document.getElementById('V_file_upload_eleven').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        // document.getElementById('V_file_upload_eleven').innerHTML = "";
        if (fileInput_Result4 == false) {
            document.getElementById('V_file_upload_eleven').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('V_file_upload_eleven').innerHTML = "";
            const oFile = document.getElementById("v_file_upload_eleven").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_file_upload_eleven").value = "";
                return false;

            } else {
                document.getElementById('V_file_upload_eleven').innerHTML = "";
            }
        }
    }

    if (bsi == "") {
        document.getElementById('bsi_11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result21 == false) {
            document.getElementById('bsi_11').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            // document.getElementById('bsi_11').innerHTML = "";
            const oFile = document.getElementById("v_upload_se1").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_se1").value = "";
                return false;

            } else {
                document.getElementById('bsi_11').innerHTML = "";
            }
        }
    }
    if (V_upload_eight == "") {
        document.getElementById('file_2').innerHTML = "Please upload the file in pdf required";
        return false;
    } else {
        if (fileInput_Result6 == false) {
            document.getElementById('file_2').innerHTML = "Valid file format required";
            return false;
        } else {
            // document.getElementById('file_2').innerHTML = "";
            const oFile = document.getElementById("upload_eight").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("upload_eight").value = "";
                return false;

            } else {
                document.getElementById('file_2').innerHTML = "";
            }
        }
    }

    if (V_product_nine == "") {

        document.getElementById('file3').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('file3').innerHTML = "";
    }

    if (V_method_ten == "") {
        document.getElementById('file4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (fileInput_Result7 == false) {
            document.getElementById('file4').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('file4').innerHTML = "";
            const oFile = document.getElementById("v_upload_ten").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_ten").value = "";
                return false;

            } else {
                document.getElementById('file4').innerHTML = "";
            }
        }
    }

    if (V_upload_ten == "") {
        document.getElementById('data1').innerHTML = "Please fill the required detail";
        return false;
    } else {
        document.getElementById('data1').innerHTML = " ";
    }

    if (V_eleven_upload_one == "") {
        document.getElementById('data11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result9 == false) {
            document.getElementById('data11').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('data11').innerHTML = "";
            const oFile = document.getElementById("v_eleven_upload_one").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_eleven_upload_one").value = "";
                return false;

            } else {
                document.getElementById('data11').innerHTML = "";
            }
        }
    }

    if (V_office_list_two == "") {
        document.getElementById('data12').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('data12').innerHTML = "";
    }

    if (V_upload_file_two == "") {
        document.getElementById('data13').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result10 == false) {
            document.getElementById('data13').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('data13').innerHTML = "";
            const oFile = document.getElementById("v_upload_file_two").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_two").value = "";
                return false;

            } else {
                document.getElementById('data13').innerHTML = "";
            }
        }
    }

    if (data14 == "") {

        document.getElementById('data14').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('data14').innerHTML = "";
    }

    if (V_eleven_upload_one_89 == "") {
        document.getElementById('data35').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        // document.getElementById('data35').innerHTML = "";
        if (fileInput_Result20 == false) {
            document.getElementById('data35').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('data35').innerHTML = "";
            const oFile = document.getElementById("Twenty_five").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Twenty_five").value = "";
                return false;

            } else {
                document.getElementById('data35').innerHTML = "";
            }
        }
    }

    // // if (data16 == "") {

    // //     document.getElementById('data16').innerHTML = "Please fill the required detail  ";
    // //     return false;
    // // } else {

    // //     document.getElementById('data16').innerHTML = "";
    // // }

    if (twenty_five_file == "") {
        document.getElementById('data17').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result22 == false) {
            document.getElementById('data17').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('data17').innerHTML = "";
            const oFile = document.getElementById("Twenty_seven").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Twenty_seven").value = "";
                return false;

            } else {
                document.getElementById('data17').innerHTML = "";
            }
        }
    }


    // if (data18 == "") {

    //     document.getElementById('data18').innerHTML = "Please fill the required detail  ";
    //     return false;
    // } else {
    //     document.getElementById('data18').innerHTML = "";
    // }

    // if(data19 ==""){
    //     document.getElementById('data191').innerHTML = "Please upload the file in pdf format only"; 
    // }
    // else{
    //     if(fileInput_Result25 == false){
    //         document.getElementById('data191').innerHTML = "Valid file format required(In .pdf)";
    //     }else{
    //         document.getElementById('data191').innerHTML = ""; 
    //     }
    //     document.getElementById('data191').innerHTML = "";
    // }
    if (data19 == "") {
        document.getElementById('data191').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (fileInput_Result25 == false) {
            document.getElementById('data191').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('data191').innerHTML = "";
            const oFile = document.getElementById("Twenty_nineteen2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Twenty_nineteen2").value = "";
                return false;

            } else {
                document.getElementById('data191').innerHTML = "";
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