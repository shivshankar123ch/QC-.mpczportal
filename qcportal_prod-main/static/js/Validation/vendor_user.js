function validateForm() {

    let Work_experience = document.forms["myForm"]["work_experience"].value;
    let Turn_over = document.forms["myForm"]["turn_over"].value;

    if (Work_experience == "") {
        document.getElementById('Work_experience').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('Work_experience').innerHTML = "";
    }
    if (Turn_over == "") {
        document.getElementById('Turn_over').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('Turn_over').innerHTML = "";
    }
    ////////////////////////////////////////////////////////////////////////////

    let reg_no = document.forms["myForm"]["one"].value;
    let issue1 = document.forms["myForm"]["two"].value;
    let expire1 = document.forms["myForm"]["three"].value;
    let file1 = document.forms["myForm"]["todays"].value;
    let fileCheck1 = document.getElementById('v_upload_file_factory_19').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileResult1 = allowedExtensions.test(fileCheck1);



    if (reg_no == "") {
        document.getElementById('registrationNumber').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('registrationNumber').innerHTML = "";
    }
    if (issue1 == "") {
        document.getElementById('V_issue_date').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('V_issue_date').innerHTML = "";
    }
    if (expire1 == "") {
        document.getElementById('V_end_date').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('V_end_date').innerHTML = "";
    }
    if (file1 == "") {
        document.getElementById('file_data1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult1 == false) {
            document.getElementById('file_data1').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            console.log("hwgwhgihwieghwighi")
            document.getElementById('file_data1').innerHTML = "";
        }
    }
    //////////////////.................................................s.....

    let adhar_name = document.forms["myForm"]["v_p_aadhar_hoder_name"].value;
    let adhar_no = document.forms["myForm"]["v_p_aadhar_reg_number"].value;
    let adharCheck1 = document.getElementById('v_p_aadhar_reg_number').value;
    let aadharRGEX = /^\d{12}$/;
    let V_p_aadhar_reg_Result1 = aadharRGEX.test(adharCheck1);
    let issue2 = document.forms["myForm"]["v_p_issue_date1"].value;
    let file2 = document.forms["myForm"]["v_upload_file_factory_789"].value;
    let fileCheck2 = document.getElementById('v_upload_file_factory_19').value;
    let fileResult2 = allowedExtensions.test(fileCheck2);


    if (adhar_name == "") {
        document.getElementById('V_p_aadhar_hoder_name1').innerHTML = "Please fill the required details";
        return false;
    } else {
        console.log("elsee")
        document.getElementById('V_p_aadhar_hoder_name1').innerHTML = "";
    }

    if (adhar_no == "") {
        console.log("comddjkc")
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
    if (issue2 == "") {
        document.getElementById('V_p_issue_date').innerHTML = "Please fill the required details";
        return false;
    } else {
        console.log("elsee")
        document.getElementById('V_p_issue_date').innerHTML = "";
    }

    if (file2 == "") {
        document.getElementById('file_data2').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult2 == false) {
            document.getElementById('file_data2').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            console.log("hwgwhgihwieghwighi")
            document.getElementById('file_data2').innerHTML = "";
        }
    }

    //////////////////////////////////........................................

    let reg_no1 = document.forms["myForm"]["v_p_reg_number"].value;
    let expire3 = document.forms["myForm"]["v_p_end_date1"].value;
    let file3 = document.forms["myForm"]["v_upload_file3"].value;
    let fileCheck3 = document.getElementById('v_upload_file3').value;
    let fileResult3 = allowedExtensions.test(fileCheck3);


    if (reg_no1 == "") {
        document.getElementById('V_p_reg_number').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('V_p_reg_number').innerHTML = "";
    }

    if (expire3 == "") {
        document.getElementById('V_p_end_date').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('V_p_end_date').innerHTML = "";
    }

    if (file3 == "") {
        document.getElementById('V_upload_file').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult3 == false) {
            document.getElementById('V_upload_file').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            console.log("hwgwhgihwieghwighi")
            document.getElementById('V_upload_file').innerHTML = "";
        }
    }

    ///////////////////////////////////////////////.......................................

    let fac_no = document.forms["myForm"]["v_faculty_license_number"].value;
    let file4 = document.forms["myForm"]["v_upload_file_factory_90"].value;
    let fileCheck4 = document.getElementById('v_upload_file_factory_90').value;
    let fileResult4 = allowedExtensions.test(fileCheck4);

    let file5 = document.forms["myForm"]["past_experienceUpload_file_67"].value;
    let fileCheck5 = document.getElementById('past_experienceUpload_file_67').value;
    let fileResult5 = allowedExtensions.test(fileCheck5);




    if (fac_no == "") {
        document.getElementById('lisence').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('lisence').innerHTML = "";
    }

    if (file4 == "") {
        document.getElementById('fileCheck3').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult4 == false) {
            document.getElementById('fileCheck3').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('fileCheck3').innerHTML = "";
        }
    }

    if (file5 == "") {
        document.getElementById('fileCheck4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult5 == false) {
            document.getElementById('fileCheck4').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('fileCheck4').innerHTML = "";
        }
    }

    /////////////////////////////////...............................................................


    let area = document.forms["myForm"]["v_area_occupied"].value;
    let working = document.forms["myForm"]["v_working_shift"].value;
    let employe = document.forms["myForm"]["v_personal_work_factroy_89"].value;
    let factory = document.forms["myForm"]["v_buit_up"].value;

    if (area == "") {
        document.getElementById('area').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('area').innerHTML = "";
    }

    if (working == "") {
        document.getElementById('shift').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('shift').innerHTML = "";
    }

    if (employe == "") {
        document.getElementById('work_factory').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('work_factory').innerHTML = "";
    }

    if (factory == "") {
        document.getElementById('built').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('built').innerHTML = "";
    }

    ////////////////////////////////////....................................................

    let doc_issue = document.forms["myForm"]["name_office"].value;
    let doc_num = document.forms["myForm"]["v_supply_criteria"].value;


    if (doc_issue == "") {
        document.getElementById('Name_office').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('Name_office').innerHTML = "";
    }

    if (doc_num == "") {
        document.getElementById('V_supply_criteria').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('V_supply_criteria').innerHTML = "";
    }

    ////////////////////////////////////////////////..............................................

    let file6 = document.forms["myForm"]["v_upload_file_ele"].value;
    let fileCheck6 = document.getElementById('v_upload_file_ele').value;
    let fileResult6 = allowedExtensions.test(fileCheck6);

    let file7 = document.forms["myForm"]["v_file_upload_elev"].value;
    let fileCheck7 = document.getElementById('v_file_upload_elev').value;
    let fileResult7 = allowedExtensions.test(fileCheck7);

    let file8 = document.forms["myForm"]["v_upload_file_eleve"].value;
    let fileCheck8 = document.getElementById('v_upload_file_eleve').value;
    let fileResult8 = allowedExtensions.test(fileCheck8);

    let file9 = document.forms["myForm"]["v_file_upload_eleven"].value;
    let fileCheck9 = document.getElementById('v_file_upload_eleven').value;
    let fileResult9 = allowedExtensions.test(fileCheck9);


    if (file6 == "") {
        document.getElementById('doc_data1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult6 == false) {
            document.getElementById('doc_data1').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('doc_data1').innerHTML = "";
        }
    }

    if (file7 == "") {
        document.getElementById('doc_data2').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult7 == false) {
            document.getElementById('doc_data2').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('doc_data2').innerHTML = "";
        }
    }

    if (file8 == "") {
        document.getElementById('doc_data3').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult8 == false) {
            document.getElementById('doc_data3').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('doc_data3').innerHTML = "";
        }
    }

    if (file9 == "") {
        document.getElementById('doc_data4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult9 == false) {
            document.getElementById('doc_data4').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('doc_data4').innerHTML = "";
        }
    }

    /////////////////////////////////////////.................................................

    let quality = document.forms["myForm"]["v_method_ten"].value;
    let file10 = document.forms["myForm"]["v_upload_ten"].value;
    let fileCheck10 = document.getElementById('v_upload_ten').value;
    let fileResult10 = allowedExtensions.test(fileCheck10);


    if (quality == "") {
        document.getElementById('quality1').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('quality1').innerHTML = "";
    }

    if (file10 == "") {
        document.getElementById('file4').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult10 == false) {
            document.getElementById('file4').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('file4').innerHTML = "";
        }
    }

    ///////////////////////////////////////.....................................

    let address1 = document.forms["myForm"]["v_eleven_source"].value;
    let file12 = document.forms["myForm"]["v_eleven_upload_one"].value;
    let fileCheck12 = document.getElementById('v_eleven_upload_one').value;
    let fileResult12 = allowedExtensions.test(fileCheck12);

    if (address1== "") {
        document.getElementById('data1').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('data1').innerHTML = "";
    }

    if (file12 == "") {
        document.getElementById('data11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult12 == false) {
            document.getElementById('data11').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('data11').innerHTML = "";
        }
    }

    /////////////////////////////////////////////...........................................

    let address2 = document.forms["myForm"]["v_office_list_two1"].value;
    let file13 = document.forms["myForm"]["v_upload_file_two"].value;
    let fileCheck13 = document.getElementById('v_upload_file_two').value;
    let fileResult13 = allowedExtensions.test(fileCheck13);

    if (address2 == "") {
        document.getElementById('data12').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('data12').innerHTML = "";
    }

    if (file13 == "") {
        document.getElementById('data13').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult13 == false) {
            document.getElementById('data13').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('data13').innerHTML = "";
        }
    }

    // ////////////////////////////////////////////////////////////////////................................


    let address3 = document.forms["myForm"]["Twenty_four_78"].value;
    let file14 = document.forms["myForm"]["Twenty_five"].value;
    let fileCheck14 = document.getElementById('Twenty_five').value;
    let fileResult14 = allowedExtensions.test(fileCheck14);

    if (address3 == "") {
        document.getElementById('data14').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('data14').innerHTML = "";
    }

    if (file14 == "") {
        document.getElementById('data35').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult14 == false) {
            document.getElementById('data35').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('data35').innerHTML = "";
        }
    }

    // ////////////////////////////...............................................................

    let address4 = document.forms["myForm"]["v_p_issue_date"].value;
    let file15 = document.forms["myForm"]["Twenty_seven1"].value;
    let fileCheck15 = document.getElementById('Twenty_seven1').value;
    let fileResult15 = allowedExtensions.test(fileCheck15);

    if (address4 == "") {
        document.getElementById('data16').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('data16').innerHTML = "";
    }

    if (file15 == "") {
        document.getElementById('data17').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult15 == false) {
            document.getElementById('data17').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('data17').innerHTML = "";
        }
    }

    ///////////////////////////////////............................................................

    let address5 = document.forms["myForm"]["v_p_issue_date_2"].value;
    let file16= document.forms["myForm"]["Twenty_nineteen2"].value;
    let fileCheck16= document.getElementById('Twenty_nineteen2').value;
    let fileResult16= allowedExtensions.test(fileCheck16);

    if (address5 == "") {
        document.getElementById('data18').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('data18').innerHTML = "";
    }

    if (file16== "") {
        document.getElementById('data191').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult16== false) {
            document.getElementById('data191').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('data191').innerHTML = "";
        }
    }

    ////////////////////////////////////////////////////////////....................................

    
    let pan = document.forms["myForm"]["v_pan_name_t"].value;
    let pan_no = document.forms["myForm"]["v_pan_name_t"].value;
    let panNumber = document.getElementById('panCard').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);
    let pan_issue = document.forms["myForm"]["v_date_issue_t"].value;

    let file_Pan= document.forms["myForm"]["inputNameChoseDoc"].value;
    let fileCheck_Pan= document.getElementById('inputNameChoseDoc').value;
    let fileResult_Pan= allowedExtensions.test(fileCheck_Pan);


    if (pan == "") {
        document.getElementById('panName').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('panName').innerHTML = "";
    }

    if (pan_no == "") {
        document.getElementById('Pan_Card').innerHTML = "Please fill the required field ";
        return false;
    } else {
        if (panResult == false) {
            document.getElementById('Pan_Card').innerHTML = "Please fill the valid Pan number(ABCTY1234D format)";
            return false;
        } else {
            document.getElementById('Pan_Card').innerHTML = "";
        }
    }

    if (pan_issue == "") {
        document.getElementById('issueDate').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('issueDate').innerHTML = "";
    }

    if (file_Pan == "") {
        document.getElementById('upload1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult_Pan == false) {
            document.getElementById('upload1').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('upload1').innerHTML = "";
        }
    }

    ////////////////////////////////////////////////////............................................

    let state = document.forms["myForm"]["inpu_tName"].value;
    let gst_no = document.forms["myForm"]["inputName_12"].value;



    if (state == "") {
        document.getElementById('satae2').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('satae2').innerHTML = "";
    }

    if (gst_no == "") {
        document.getElementById('gst_no').innerHTML = "Please fill the required details";
        return false;
    } else {

        document.getElementById('gst_no').innerHTML = "";
    }

    ////////////////////////////////////////////////////////////........................................

    let file_satae1= document.forms["myForm"]["inputName_31"].value;
    let fileCheck_satae1= document.getElementById('inputName_31').value;
    let fileResult_satae1= allowedExtensions.test(fileCheck_satae1);

    let file_state2= document.forms["myForm"]["inputName_2"].value;
    let fileCheck_state2= document.getElementById('inputName_2').value;
    let fileResult_state2= allowedExtensions.test(fileCheck_state2);

    let file_state3= document.forms["myForm"]["inputName_231"].value;
    let fileCheck_state3= document.getElementById('inputName_231').value;
    let fileResult_state3= allowedExtensions.test(fileCheck_state3);


    if (file_satae1 == "") {
        document.getElementById('Twenty_two').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult_satae1 == false) {
            document.getElementById('Twenty_two').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('Twenty_two').innerHTML = "";
        }
    }
    if (file_state2 == "") {
        document.getElementById('Four1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult_state2 == false) {
            document.getElementById('Four1').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('Four1').innerHTML = "";
        }
    }
    if (file_state3 == "") {
        document.getElementById('Four23').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileResult_state3 == false) {
            document.getElementById('Four23').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        } else {
            document.getElementById('Four23').innerHTML = "";
        }
    }
}