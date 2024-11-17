///form Validation
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
function validateForm() {

    let name_office = document.getElementById("v_office_name_supply").value;
    let v_supply_criteria = document.getElementById("v_supply_criteria").value;

    var upload_file1 = document.getElementById('v_upload_file_ele').value;
    var allowedExtensions = /(\.pdf)$/i;
    let upload_file_Result1 = allowedExtensions.test(upload_file1);

    var upload_file2 = document.getElementById('v_file_upload_elev').value;
    let upload_file_Result2 = allowedExtensions.test(upload_file2);

    var upload_file3 = document.getElementById('v_upload_file_eleve').value;
    let upload_file_Result3 = allowedExtensions.test(upload_file3);

    
    var upload_file4 = document.getElementById('v_file_upload_eleven').value;
    let upload_file_Result4 = allowedExtensions.test(upload_file4);


    var upload_file5 = document.getElementById('v_upload_se1').value;
    let upload_file_Result5 = allowedExtensions.test(upload_file5);


    
    var upload_file6 = document.getElementById('upload_eight').value;
    let upload_file_Result6 = allowedExtensions.test(upload_file6);

    let name_of_method = document.getElementById('v_method_ten').value;
    var upload_file7 = document.getElementById('v_upload_ten').value;
    let upload_file_Result7 = allowedExtensions.test(upload_file7);


    var supplier_name = document.getElementById('v_eleven_source').value;
    var upload_file8 = document.getElementById('v_eleven_upload_one').value;
    let upload_file_Result8 = allowedExtensions.test(upload_file8);


    var name_of_items = document.getElementById('v_office_list_two').value;
    var upload_file9 = document.getElementById('v_upload_file_two').value;
    let upload_file_Result9 = allowedExtensions.test(upload_file9);

    let electricity_connection_no = document.getElementById('Twenty_four_78').value;
    var upload_file10 = document.getElementById('Twenty_five').value;Twenty_five
    let upload_file_Result10 = allowedExtensions.test(upload_file10);


    
    var upload_file11 = document.getElementById('Twenty_seven').value;
    let upload_file_Result11 = allowedExtensions.test(upload_file11);


    
    var upload_file12 = document.getElementById('Twenty_nineteen2').value;
    let upload_file_Result12 = allowedExtensions.test(upload_file12);



    if (name_office == "") {

        document.getElementById('v_office_name_supply_span').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('v_office_name_supply_span').innerHTML = "";
    }
    if (v_supply_criteria == "") {
        document.getElementById('v_supply_criteria_span').innerHTML = "  Please fill the required detail ";
        return false;
    } else {
        document.getElementById('v_supply_criteria_span').innerHTML = "";
    }

    if (upload_file1 == "") {
        document.getElementById('v_upload_file_ele_span').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (upload_file_Result1 == false) {
            document.getElementById('v_upload_file_ele_span').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            const oFile = document.getElementById("v_upload_file_ele").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_ele").value = "";
                return false;

            } else {
                document.getElementById('v_upload_file_ele_span').innerHTML = "";
            }


        }
    }
    if (upload_file2 == "") {
        document.getElementById('V_file_upload_elev').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (upload_file_Result2 == false) {
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

    if (upload_file3 == "") {
        document.getElementById('V_upload_file_eleve').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (upload_file_Result3 == false) {
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

    if (upload_file4 == "") {
        document.getElementById('V_file_upload_eleven').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        // document.getElementById('V_file_upload_eleven').innerHTML = "";
        if (upload_file_Result4 == false) {
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

    if (upload_file5 == "") {
        document.getElementById('bsi_11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (upload_file_Result5 == false) {
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


    if (upload_file6 == "") {
        document.getElementById('file_2').innerHTML = "Please upload the file in pdf required";
        return false;
    } else {
        if (upload_file_Result6 == false) {
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


    if (name_of_method == "") {

        document.getElementById('v_method_ten_span').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('v_method_ten_span').innerHTML = "";
    }


    if (upload_file7 == "") {
        document.getElementById('file4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (upload_file_Result7 == false) {
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


    if (supplier_name == "") {

        document.getElementById('v_eleven_source_span').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('v_eleven_source_span').innerHTML = "";
    }


    if (upload_file8 == "") {
        document.getElementById('data11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
       
        if (upload_file_Result8 == false) {
            document.getElementById('data11').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
           
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


    if (name_of_items == "") {
        document.getElementById('v_office_list_two_span').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('v_office_list_two_span').innerHTML = "";
    }


    if (upload_file9 == "") {
        document.getElementById('data13').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('V_upload_file_ele').innerHTML = "";
        if (upload_file_Result9 == false) {
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


    if (electricity_connection_no == "") {

        document.getElementById('Twenty_four_78_span').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('Twenty_four_78_span').innerHTML = "";
    }


    if (upload_file10 == "") {
        document.getElementById('data35').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (upload_file_Result10 == false) {
            document.getElementById('data35').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
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


    if (upload_file11 == "") {
        document.getElementById('data17').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (upload_file_Result11 == false) {
            document.getElementById('data17').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
           
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

    if (upload_file12 == "") {
        document.getElementById('data191').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        
        if (upload_file_Result12 == false) {
            document.getElementById('data191').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            
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
    if(!confirm("Are you sure you want to submit?")) {
        return false;
      }
      this.form.submit();
}


