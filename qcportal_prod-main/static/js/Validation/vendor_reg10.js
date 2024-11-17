//form validation
function validateForm() {
    console.log("vendor 10 functionn fireeeeeeeeeeeeeeeeeeeee")
    let reg_Number = document.forms["myForm"]["one"].value;
    let V_issue_date = document.forms["myForm"]["two"].value;
    let V_end_date = document.forms["myForm"]["three"].value;
    let file1 = document.forms["myForm"]["todays"].value;
    let fileCheck1 = document.getElementById('v_upload_file_factory_19').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileResult1 = allowedExtensions.test(fileCheck1);

    let V_p_aadhar_hoder_name = document.forms["myForm"]["four"].value;
    let V_p_aadhar_reg_number1 = document.forms["myForm"]["five"].value;
    let adharCheck1 = document.getElementById('v_p_aadhar_reg_number').value;
    let aadharRGEX = /^\d{12}$/;
    let V_p_aadhar_reg_Result1 = aadharRGEX.test(adharCheck1);
    let file2 = document.forms["myForm"]["new"].value;
    let fileCheck2 = document.getElementById('v_upload_file_factory_789').value;
    let fileResult2 = allowedExtensions.test(fileCheck2);

    let V_p_issue_date = document.forms["myForm"]["six"].value;
    let V_p_reg_number = document.forms["myForm"]["seven"].value;
    let V_p_end_date = document.forms["myForm"]["eight"].value;
    var fileInput1 = document.getElementById('v_upload_file').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);

    let V_faculty_license_number = document.forms["myForm"]["sixteen"].value;
    let V_upload_file_factory = document.forms["myForm"]["seventeen"].value;
    var fileInput4 = document.getElementById('v_upload_file_factory_90').value;
    let fileInput3_Result4 = allowedExtensions.test(fileInput4);

    // let Past_experienceUpload_file = document.forms["myForm"]["eighteen"].value;
    // var fileInput5 = document.getElementById('past_experienceUpload_file_67').value;
    // let fileInput5_Result5 = allowedExtensions.test(fileInput5);

    let V_area_occupied = document.forms["myForm"]["nineteen"].value;
    let V_working_shift = document.forms["myForm"]["twenty"].value;

    let V_personal_work_factroy = document.forms["myForm"]["twenty_one"].value;
    let V_buit_up = document.forms["myForm"]["twenty_two"].value;

    let V_upload_file_material = document.forms["myForm"]["twenty_three"].value;
    var fileInput6 = document.getElementById('v1_upload_file_material').value;
    var allowedExtensions3 = /(http(s?):)|([/|.|\w|\s])*\.(?:jpg|gif|png)/
    let fileInput6_Result6 = allowedExtensions3.test(fileInput6);
    let V_upload_file_material2 = document.forms["myForm"]["twenty_four"].value;
    var fileInput7 = document.getElementById('v_upload_file_material').value;
    let fileInput7_Result7 = allowedExtensions.test(fileInput7);



    if (reg_Number == "") {
        document.getElementById('registrationNumber').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('registrationNumber').innerHTML = "";
    }
    if (V_issue_date == "") {
        document.getElementById('V_issue_date').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('V_issue_date').innerHTML = "";
    }
    if (V_end_date == "") {
        document.getElementById('V_end_date').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('V_end_date').innerHTML = "";
    }
    if (file1 == "") {
        document.getElementById('file_data1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult1 == false) {
            document.getElementById('file_data1').innerHTML = " Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_factory_19").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_factory_19").value = "";
                return false;

            } else {
                // Proceed further
                console.log("jjjjj999");
                document.getElementById('file_data1').innerHTML = "";
            }
        }
    }

    /////////////////////////////////////////////////........................................

    if (V_p_aadhar_hoder_name == "") {
        document.getElementById('V_p_aadhar_hoder_name').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('V_p_aadhar_hoder_name').innerHTML = "";
    }
    if (V_p_aadhar_reg_number1 == "") {
        document.getElementById('adharNO').innerHTML = " Please fill the required details";
        return false;
    } else {

        if (V_p_aadhar_reg_Result1 == false) {
            document.getElementById('adharNO').innerHTML = "Please fill the valid Aadhaar number";
            return false;
        } else {
            document.getElementById('adharNO').innerHTML = "";
        }
    }
    if (V_p_issue_date == "") {
        document.getElementById('V_p_issue_date').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('V_p_issue_date').innerHTML = "";
    }
    if (file2 == "") {
        document.getElementById('file_data2').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        if (fileResult2 == false) {
            document.getElementById('file_data2').innerHTML = " Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_factory_789").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_factory_789").value = "";
                return false;

            } else {

                document.getElementById('file_data2').innerHTML = "";
            }
        }
    }

    // ///////////////////////////////////////////////.............................................


    if (V_p_reg_number == "") {
        document.getElementById('V_p_reg_number').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('V_p_reg_number').innerHTML = "";
    }
    if (V_p_end_date == "") {
        document.getElementById('V_p_end_date').innerHTML = " Please fill the required details";
        return false;
    } else {
        document.getElementById('V_p_end_date').innerHTML = "";
    }
    if (V_upload_file == "") {
        document.getElementById('V_upload_file').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileInput_Result1 == false) {
            document.getElementById('V_upload_file').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file").value = "";
                return false;
                // $(file).val(''); //for clearing with Jquery
            } else {
                document.getElementById('V_upload_file').innerHTML = "";
            }
        }
    }

    if (V_faculty_license_number == "") {
        document.getElementById('lisence').innerHTML = " Please fill the required details ";
        return false;
    } else {
        document.getElementById('lisence').innerHTML = "";
    }
    if (V_upload_file_factory == "") {
        document.getElementById('fileCheck3').innerHTML = " Please upload the file in pdf format only  ";
        return false;
    } else {

        if (fileInput3_Result4 == false) {
            document.getElementById('fileCheck3').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_factory_90").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_factory_90").value = "";
                return false;

            } else {

                document.getElementById('fileCheck3').innerHTML = "";
            }
        }
    }

    // ////////////////////////////////.............................

    // if (Past_experienceUpload_file == "") {
    //     document.getElementById('fileCheck4').innerHTML = "Please upload the file in pdf format only  ";
    //     return false;
    // } else {

    //     if (fileInput5_Result5 == false) {
    //         document.getElementById('fileCheck4').innerHTML = " Please Upload valid file format(In .pdf format).. ";
    //         return false;
    //     } else {
    //         const oFile = document.getElementById("past_experienceUpload_file_67").files[0].size / 1024 / 1024;
    //         if (oFile > 2) {
    //             alert("File size must be less than or equal to 2 MB");
    //             document.getElementById("past_experienceUpload_file_67").value = "";
    //             return false;

    //         } else {
    //             // Proceed further
    //             console.log("jjjjj999");
    //             document.getElementById('fileCheck4').innerHTML = "";
    //         }
    //     }
    // }

    if (V_area_occupied == "") {
        document.getElementById('area').innerHTML = " Please fill the Area Of Land Occupied By Factory (sq. ft.) ..  ";
        return false;
    } else {
        document.getElementById('area').innerHTML = "";
    }
    if (V_working_shift == "") {
        document.getElementById('shift').innerHTML = " Please fill the Number Of Working Shift in Factory..  ";
        return false;
    } else {
        document.getElementById('shift').innerHTML = "";
    }
    if (V_personal_work_factroy == "") {
        document.getElementById('work_factory').innerHTML = " Please fill the Number Of Working Employee..  ";
        return false;
    } else {
        document.getElementById('work_factory').innerHTML = "";
    }
    if (V_buit_up == "") {
        document.getElementById('built').innerHTML = " Please fill the Buit Up Area Of Factory (sq. ft.)..  ";
        return false;
    } else {
        document.getElementById('built').innerHTML = "";
    }
    if (V_upload_file_material == "") {
        document.getElementById('factoryMaterial').innerHTML = " Please upload the file  ";
        return false;
    } else {
        document.getElementById('factoryMaterial').innerHTML = "";
        if (fileInput6_Result6 == false) {
            document.getElementById('factoryMaterial').innerHTML = "Please Upload valid file format(In png and jpg,jpeg)";
            return false;
        } else {
            document.getElementById('factoryMaterial').innerHTML = "";
        }
    }

    if (V_upload_file_material2 == "") {
        document.getElementById('factoryMaterial2').innerHTML = " Please upload the file in pdf format only  ";
        return false;
    } else {

        if (fileInput7_Result7 == false) {
            document.getElementById('factoryMaterial2').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {

            const oFile = document.getElementById("v_upload_file_material").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file_material").value = "";
                return false;

            } else {
                document.getElementById('factoryMaterial2').innerHTML = "";
            }
        }
    }
}