function FormError(inp_id){
    let inp = document.getElementById(inp_id);
    if(inp.value == ""){
    let x = document.getElementById(inp_id+"_span");

    x.innerHTML = "Please fill the required details";
    }else{
    let x = document.getElementById(inp_id+"_span");
    x.innerHTML = "";
    }
}
function aadharUserValidate(){
    let aadhar_holder_name = document.getElementById('v_p_aadhar_hoder_name');
    let RegExp_name = new RegExp(/^[A-Za-z ]+$/);
    if(aadhar_holder_name.value == ""){
        document.getElementById('v_p_aadhar_hoder_name_span').innerHTML = " Please fill the required details";
        return false;
        
    }else{
        let result = RegExp_name.test(aadhar_holder_name.value);
        if (result == false) {
            document.getElementById('v_p_aadhar_hoder_name_span').innerHTML = "Authorized Person should be in letter only.";
           
            return false;
        }
        else{
            document.getElementById('v_p_aadhar_hoder_name_span').innerHTML = "";
        }
    }
}
function aadharNumValidate(){

    let aadhar_holder_num = document.getElementById('v_p_aadhar_reg_number');
    let RegExp_adhar_num = /^\d{12}$/;
    
    if(aadhar_holder_num.value == ""){
        document.getElementById('v_p_aadhar_reg_number_span').innerHTML = " Please fill the required details";
        return false;
        
    }else{
        let result = RegExp_adhar_num.test(aadhar_holder_num.value);
        if (result == false) {
            document.getElementById('v_p_aadhar_reg_number_span').innerHTML = "Aadhar number should be in number & 12 digit only.";
           
            return false;
        }
        else{
            document.getElementById('v_p_aadhar_reg_number_span').innerHTML = "";
        }
    }

}
//form validation
function validateForm() {
   

    // let registration_num  = document.getElementById('inputName78').value;
    // let issue_date  = document.getElementById('v_issue_date').value;
    // let end_date  = document.getElementById('v_end_date').value;
    // let file_name1  = document.getElementById('v_upload_file_factory_19').value;
    var allowedExtensions = /(\.pdf)$/i;
    // let file_result1 = allowedExtensions.test(file_name1);
    let aadhar_holder_name = document.getElementById('v_p_aadhar_hoder_name').value;
    let aadhar_holder_num = document.getElementById('v_p_aadhar_reg_number').value;
    let issue_date1 = document.getElementById('v_p_issue_date').value;
    let upload_file1 = document.getElementById('v_upload_file_factory_789').value;
    let file_result2 = allowedExtensions.test(upload_file1);
    let Proof_registration_num = document.getElementById('v_p_reg_number').value;
    let end_date2 = document.getElementById('v_p_end_date').value;

    let upload_file2 = document.getElementById('v_upload_file').value;
    let file_result3 = allowedExtensions.test(upload_file2);
    let faculty_license_number = document.getElementById('v_faculty_license_number').value;
   
    var upload_file3 = document.getElementById('v_upload_file_factory_90').value;
    let file_result4 = allowedExtensions.test(upload_file3);

    var upload_file4 = document.getElementById('v1_upload_file_material').value;
    var allowedExtensions3 = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    let file_result5= allowedExtensions3.test(upload_file4);

    var upload_file5 = document.getElementById('v_upload_file_material').value;
    let file_result6 = allowedExtensions.test(upload_file5);
   

    
    // if (registration_num == "") {
    //     document.getElementById('inputName78_span').innerHTML = " Please fill the required details ";
    //     return false;
    // } else {
    //     document.getElementById('inputName78_span').innerHTML = "";
    // }
    // if (issue_date == "") {
    //     document.getElementById('v_issue_date_span').innerHTML = " Please fill the required details ";
    //     return false;
    // } else {
    //     document.getElementById('v_issue_date_span').innerHTML = "";
    // }
    // if (end_date == "") {
    //     document.getElementById('v_end_date_span').innerHTML = " Please fill the required details";
    //     return false;
    // } else {
    //     document.getElementById('v_end_date_span').innerHTML = "";
    // }
    // if (file_name1 == "") {
    //     document.getElementById('v_upload_file_factory_19_span').innerHTML = "Please upload the file in pdf format only";
    //     return false;
    // } else {

    //     if (file_result1 == false) {
    //         document.getElementById('v_upload_file_factory_19_span').innerHTML = " Please Upload valid file format(In .pdf format)";
    //         return false;
    //     } else {

    //         const oFile = document.getElementById("v_upload_file_factory_19").files[0].size / 1024 / 1024;
    //         if (oFile > 2) {
    //             alert("File size must be less than or equal to 2 MB");
    //             document.getElementById("v_upload_file_factory_19").value = "";
    //             return false;

    //         } else {
                
    //             document.getElementById('v_upload_file_factory_19_span').innerHTML = "";
    //         }
    //     }
    // }
     if (aadhar_holder_name == "") {
        document.getElementById('v_p_aadhar_hoder_name_span').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('v_p_aadhar_hoder_name_span').innerHTML = "";
    }
    if (aadhar_holder_num == "") {
        document.getElementById('v_p_aadhar_reg_number_span').innerHTML = " Please fill the required details";
        return false;
    } else {
            document.getElementById('v_p_aadhar_reg_number_span').innerHTML = "";
      }

    if (issue_date1 == "") {
        document.getElementById('v_p_issue_date_span').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('v_p_issue_date_span').innerHTML = "";
    }
    if (upload_file1 == "") {
        document.getElementById('v_upload_file_factory_789_span').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (file_result2 == false) {
            document.getElementById('v_upload_file_factory_789_span').innerHTML = " Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_factory_789").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_factory_789").value = "";
                return false;

            } else {

                document.getElementById('v_upload_file_factory_789_span').innerHTML = "";
            }
        }
    }

    // // ///////////////////////////////////////////////.............................................


    if (Proof_registration_num == "") {
        document.getElementById('v_p_reg_number_span').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('v_p_reg_number_span').innerHTML = "";
    }
    if (end_date2 == "") {
        document.getElementById('v_p_end_date_span').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('v_p_end_date_span').innerHTML = "";
    }
    if (upload_file2 == "") {
        document.getElementById('v_upload_file').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (file_result3 == false) {
            document.getElementById('v_upload_file_span').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file").value = "";
                return false;
                // $(file).val(''); //for clearing with Jquery
            } else {
                document.getElementById('v_upload_file_span').innerHTML = "";
            }
        }
    }

    if (faculty_license_number == "") {
        document.getElementById('v_faculty_license_number_span').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('v_faculty_license_number_span').innerHTML = "";
    }
    if (upload_file3 == "") {
        document.getElementById('v_upload_file_factory_90_span').innerHTML = " Please upload the file in pdf format only  ";
        return false;
    } else {

        if (file_result4 == false) {
            document.getElementById('v_upload_file_factory_90_span').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_factory_90").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_factory_90").value = "";
                return false;

            } else {

                document.getElementById('v_upload_file_factory_90_span').innerHTML = "";
            }
        }
    }

    // // ////////////////////////////////.............................
    if (upload_file4 == "") {
            document.getElementById('v1_upload_file_material_span').innerHTML = " Please upload the file  ";
            return false;
        } else {
            document.getElementById('v1_upload_file_material_span').innerHTML = "";
            if (file_result5 == false) {
                document.getElementById('v1_upload_file_material_span').innerHTML = "Please Upload valid file format(In png and jpg,jpeg)";
                return false;
            } else {
                document.getElementById('v1_upload_file_material_span').innerHTML = "";
            }
        }
       

    if (upload_file5 == "") {
         document.getElementById('v_upload_file_material_span').innerHTML = "Please upload the file in pdf format only  ";
        return false;
    } else {

        if (file_result6 == false) {
            document.getElementById('v_upload_file_material_span').innerHTML = " Please Upload valid file format(In .pdf format).. ";
            return false;
        } else {
            const oFile = document.getElementById("v_upload_file_material").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_material").value = "";
                return false;

            } else {
               
                document.getElementById('v_upload_file_material_span').innerHTML = "";
            }
        }
    }
    if(!confirm("Are you sure you want to submit?")) {
        return false;
      }
      this.form.submit();
    
      
    
}
function fileValidation() {
    var fileInput =
        document.getElementById('v1_upload_file_material');

    var filePath = fileInput.value;

    // Allowing file type
    var allowedExtensions =
        /(\.jpg|\.jpeg|\.png|\.gif)$/i;

    if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file type');
        fileInput.value = '';
        return false;
    } else {

        // Image preview
        if (fileInput.files && fileInput.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById(
                        'imagePreview').innerHTML =
                    '<img src="' + e.target.result +
                    '"/>';
            };

            reader.readAsDataURL(fileInput.files[0]);
        }
    }
}
