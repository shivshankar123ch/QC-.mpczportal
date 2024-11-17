////form Validation
function panNameValidation(){
let pan_name = document.getElementById("v_pan_name_t").value;
let RegExp_name = new RegExp(/^[A-Za-z ]+$/);
let Result = RegExp_name.test(pan_name);
if (pan_name == "") {
    document.getElementById('pan_name').innerHTML = "Please fill the required field ";
    return false;
} else {
    if (Result == false) {
        document.getElementById('pan_name').innerHTML = "Pan Name should be in alphanumeric  only.";
        return false;
    } else {
        document.getElementById('pan_name').innerHTML = "";
    }
}

}
function panNumberValidation(){

    let pan_num = document.getElementById('panCard').value;
    let RegExp_num =/^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let result = RegExp_num.test(pan_num);

    if (pan_num == "") {
        document.getElementById('pan_card').innerHTML = "Please fill the required field ";
        return false;
    } else {
        if (result == false) {
            document.getElementById('pan_card').innerHTML = "Pan Number should be in alpha numeric only.";
            return false;
        }
        else{
            document.getElementById('pan_card').innerHTML = "";
        }
    }   
}
function gstNumberValidation(){
    let GST_number = document.getElementById('inputName_12').value;
    let gstRGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;;
    let GST_Result = gstRGEX.test(GST_number);
    if (GST_number == "") {
        document.getElementById('gst_no').innerHTML = "Please fill the GST Number";
        return false;
    } else {
       if (GST_Result == false) {
           document.getElementById('gst_no').innerHTML = " Please fill the valid GST number format";
           return false;
       } else {
           document.getElementById('gst_no').innerHTML = "";
       }
        
    }

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



function validateForm() {
    let pan_name = document.getElementById("v_pan_name_t");
    let pan_number = document.getElementById('panCard').value;
    let issue_date = document.getElementById('v_date_issue_t').value;
    
    let upload_file = document.getElementById('inputNameChoseDoc').value;
    var allowedExtensions = /(\.pdf)$/i;
    let upload_file_result = allowedExtensions.test(upload_file);

    let state = document.getElementById('inputName').value;

    let GST_number = document.getElementById('inputName_12').value;
    let gstRGEX =/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;
    let GST_Result = gstRGEX.test(GST_number);

   
    var upload_file1 = document.getElementById('inputName_31').value;
    let upload_file_result1 = allowedExtensions.test(upload_file1);

   
    var upload_file2 = document.getElementById('inputName_2').value;
    let upload_file_result2 = allowedExtensions.test(upload_file2);

   
    var upload_file3 = document.getElementById('inputName_231').value;
    let upload_file_result3 = allowedExtensions.test(upload_file3);



    if (pan_name == "") {
        document.getElementById('pan_name').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('pan_name').innerHTML = "";
    }

    if (pan_number == "") {
        document.getElementById('pan_card').innerHTML = "Please fill the required field ";
        return false;
    }else {
            document.getElementById('pan_card').innerHTML = "";
        }

    if (issue_date == "") {
        document.getElementById('v_date_issue_t_span').innerHTML = "Please fill the required field";
        return false;
    } else {
        document.getElementById('v_date_issue_t_span').innerHTML = "";
    }
    
    if (upload_file == "") {
        document.getElementById('upload1').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
       
        if (upload_file_result == false) {
            document.getElementById('upload1').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
           
            const oFile = document.getElementById("inputNameChoseDoc").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputNameChoseDoc").value = "";
                return false;

            } else {
                document.getElementById('upload1').innerHTML = "";
            }
        }
    }

    if (state == "") {
        document.getElementById('inputName').innerHTML = "Please Enter a State ";
        return false;
    } else {
        document.getElementById('inputName').innerHTML = "";
    }

    if (GST_number == "") {
        document.getElementById('gst_no').innerHTML = "Please fill the GST Number";
        return false;
    } else {
       if (GST_Result == false) {
           document.getElementById('gst_no').innerHTML = " Please fill the valid GST number(11AAAAA1111Z1A1 format) ";
           return false;
       } else {
           document.getElementById('gst_no').innerHTML = "";
       }
        
    }

    if (upload_file1 == "") {
        document.getElementById('inputname_31_span').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        
        if (upload_file_result1 == false) {
            document.getElementById('inputname_31_span').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
           
            const oFile = document.getElementById("inputName_31").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_31").value = "";
                return false;

            } else {
                document.getElementById('inputname_31_span').innerHTML = "";
            }
        }
    }

    if (upload_file2 == "") {
        document.getElementById('inputName_2_span').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        
        if (upload_file_result2 == false) {
            document.getElementById('inputName_2_span').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            
            const oFile = document.getElementById("inputName_2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_2").value = "";
                return false;

            } else {
                document.getElementById('inputName_2_span').innerHTML = "";
            }
        }
    }

    if (upload_file3 == "") {
        document.getElementById('inputName_231_span').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        if (upload_file_result3 == false) {
            document.getElementById('inputName_231_span').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            
            const oFile = document.getElementById("inputName_231").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_231").value = "";
                return false;

            } else {
                document.getElementById('inputName_231_span').innerHTML = "";
            }
        }
    }
    if(!confirm("Are you sure you want to submit?")) {
        return false;
    }
    this.form.submit();
    
}