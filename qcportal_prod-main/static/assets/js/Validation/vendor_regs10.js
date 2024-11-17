//form validation
function validateForm() { 
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
    let V_upload_file = document.forms["myForm"]["nine"].value;
    var fileInput1 = document.getElementById('v_upload_file').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);


    // let V_father_aadhar_name = document.forms["myForm"]["ten"].value;
    //  let V_father_aadhaar_number = document.forms["myForm"]["eleven"].value;
    // let V_father_aadhaar2 = document.getElementById('v_father_aadhaar_number').value;
    // let V_father_aadhaarResult2 = aadharRGEX.test(V_father_aadhaar2);
    // let V_upload_file_fathers = document.forms["myForm"]["twelve"].value;
    // var fileInput3 = document.getElementById('v_upload_file_father').value;
    // let fileInput2_Result3 = allowedExtensions.test(fileInput3);

///////////////////////////..................................


    let V_faculty_license_number = document.forms["myForm"]["sixteen"].value;
    let V_upload_file_factory = document.forms["myForm"]["seventeen"].value;
    var fileInput4 = document.getElementById('v_upload_file_factory_90').value;
    let fileInput3_Result4 = allowedExtensions.test(fileInput4);

//////////////////////////////.................................


    let Past_experienceUpload_file = document.forms["myForm"]["eighteen"].value;
    var fileInput5 = document.getElementById('past_experienceUpload_file_67').value;
    let fileInput5_Result5 = allowedExtensions.test(fileInput5);

///////////////////////////////////.........................................

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



    if(reg_Number == ""){
        document.getElementById('registrationNumber').innerHTML = " Please fill the required details ";
        return false;
    }else {
        document.getElementById('registrationNumber').innerHTML = "";
    }
    if(V_issue_date == ""){
        document.getElementById('V_issue_date').innerHTML = " Please fill the required details ";
        return false;
    }else {
        document.getElementById('V_issue_date').innerHTML = "";
    }
    if(V_end_date == ""){
        document.getElementById('V_end_date').innerHTML = " Please fill the required details";
        return false;
    }else {
        document.getElementById('V_end_date').innerHTML = "";
    }
    if(file1 == ""){
        document.getElementById('file_data1').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('file_data1').innerHTML = "";
        if(fileResult1 == false)
        {
            document.getElementById('file_data1').innerHTML = " Please Upload valid file format(In .pdf format)";
            return false;
        }else{
              document.getElementById('file_data1').innerHTML = "";
        }
    }

/////////////////////////////////////////////////........................................

    if(V_p_aadhar_hoder_name == ""){
        document.getElementById('V_p_aadhar_hoder_name').innerHTML = " Please fill the required details";
        return false;
    }else {
        document.getElementById('V_p_aadhar_hoder_name').innerHTML = "";
    }
    if(V_p_aadhar_reg_number1 == ""){
        document.getElementById('adharNO').innerHTML = " Please fill the required details";
        return false;
    }else {
        //document.getElementById('adharNO').innerHTML = "";
        if(V_p_aadhar_reg_Result1 == false)
        {
            document.getElementById('adharNO').innerHTML = "Please fill the valid Aadhaar number";
            return false;
        }else{
              document.getElementById('adharNO').innerHTML = "";
        }
    }
    if(V_p_issue_date == ""){
        document.getElementById('V_p_issue_date').innerHTML = " Please fill the required details ";
        return false;
    }else {
        document.getElementById('V_p_issue_date').innerHTML = "";
    }
    if(file2 == ""){
        document.getElementById('file_data2').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('file_data2').innerHTML = "";
        if(fileResult2 == false)
        {
            document.getElementById('file_data2').innerHTML = " Please Upload valid file format(In .pdf format)";
            return false;
        }else{
              document.getElementById('file_data2').innerHTML = "";
        }
    }

///////////////////////////////////////////////.............................................


    if(V_p_reg_number == ""){
        document.getElementById('V_p_reg_number').innerHTML = " Please fill the required details ";
        return false;
    }else {
        document.getElementById('V_p_reg_number').innerHTML = "";
    }
    if(V_p_end_date == ""){
        document.getElementById('V_p_end_date').innerHTML = " Please fill the required details";
        return false;
    }else {
        document.getElementById('V_p_end_date').innerHTML = "";
    }
    if(V_upload_file == ""){
        document.getElementById('V_upload_file').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('V_upload_file').innerHTML = "";
        if(fileInput_Result1 == false)
        {
            document.getElementById('V_upload_file').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        }else{
              document.getElementById('V_upload_file').innerHTML = "";
        }
    }




    ///start
    // if(fileInput3 !== ""){
    //     document.getElementById('V_upload_file_fatherS').innerHTML = "Please Upload valid file format(In .pdf format)";
    //     return false;

    // }else{
    //     document.getElementById('V_upload_file_fatherS').innerHTML = "";
    // }

    ///////////////////////////////////////////////..............................

    // if(V_father_aadhar_name == ""){
    //     document.getElementById('V_father_aadhar_name').innerHTML = " Please fill the required details  ";
    //     return false;
    // }else {
    //     document.getElementById('V_father_aadhar_name').innerHTML = "";
    // }
    // if(V_father_aadhaar_number !== ""){
    //     if(V_father_aadhaarResult2 == false)
    //     {
    //         document.getElementById('V_father_aadhaar_number').innerHTML = " Please fill the valid Aadhaar number ";
    //         return false;
    //     }else{
    //           document.getElementById('V_father_aadhaar_number').innerHTML = "";
    //     }
    // }else {
    //     document.getElementById('V_father_aadhaar_number').innerHTML = "";
    // }
    // if(V_upload_file_father == ""){
    //     document.getElementById('V_upload_file_father').innerHTML = "Please fill the required details";
    //     return false;
    // }else {
        //document.getElementById('V_upload_file_father').innerHTML = "";
    //     if(fileInput2_Result2 == false)
    //     {
    //         document.getElementById('V_upload_file_father').innerHTML = " Please Upload valid file format(In .pdf format) ";
    //         return false;
    //     }else{
    //           document.getElementById('V_upload_file_father').innerHTML = "";
    //     }
    // }

    /////////////////////////...................................................

    if(V_faculty_license_number == ""){
        document.getElementById('lisence').innerHTML = " Please fill the required details ";
        return false;
    }else {
        document.getElementById('lisence').innerHTML = "";
    }
    if(V_upload_file_factory == ""){
        document.getElementById('fileCheck3').innerHTML = " Please upload the file in pdf format only  ";
        return false;
    }else {
        //document.getElementById('fileCheck3').innerHTML = "";
        if(fileInput3_Result4 == false)
        {
            document.getElementById('fileCheck3').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        }else{
              document.getElementById('fileCheck3').innerHTML = "";
        }
    }
    
    ////////////////////////////////.............................


    if(Past_experienceUpload_file == ""){
        document.getElementById('fileCheck4').innerHTML = "Please upload the file in pdf format only  ";
        return false;
    }else {
       // document.getElementById('fileCheck4').innerHTML = "";
       if(fileInput5_Result5 == false)
       {
           document.getElementById('fileCheck4').innerHTML = " Please Upload valid file format(In .pdf format).. ";
           return false;
       }else{
             document.getElementById('fileCheck4').innerHTML = "";
       }
    }

    if(V_area_occupied == ""){
        document.getElementById('area').innerHTML = " Please fill the Area Of Land Occupied By Factory (sq. ft.) ";
        return false;
    }else {
        document.getElementById('area').innerHTML = "";
    }
    if(V_working_shift == ""){
        document.getElementById('shift').innerHTML = " Please fill the Number Of Working Shift in Factory";
        return false;
    }else {
        document.getElementById('shift').innerHTML = "";
    }
    if(V_personal_work_factroy == ""){
        document.getElementById('work_factory').innerHTML = " Please fill the Number Of Working Employee";
        return false;
    }else {
        document.getElementById('work_factory').innerHTML = "";
    }
    if(V_buit_up == ""){
        document.getElementById('built').innerHTML = " Please fill the Buit Up Area Of Factory (sq. ft.)";
        return false;
    }else {
        document.getElementById('built').innerHTML = "";
    }
    if(V_upload_file_material == ""){
        document.getElementById('factoryMaterial').innerHTML = " Please upload the file  ";
        return false;
    }else {
        document.getElementById('factoryMaterial').innerHTML = "";
        if(fileInput6_Result6 == false)
       {
           document.getElementById('factoryMaterial').innerHTML = "Please Upload valid file format(In. PNG formate)";
           return false;
       }else{
             document.getElementById('factoryMaterial').innerHTML = "";
       }
    }
    
    if(V_upload_file_material2 == ""){
        document.getElementById('factoryMaterial2').innerHTML = " Please upload the file in pdf format only  ";
        return false;
    }else {
        //document.getElementById('factoryMaterial2').innerHTML = "";
        if(fileInput7_Result7 == false)
        {
            document.getElementById('factoryMaterial2').innerHTML = "Please Upload valid file format(In .pdf format)";
            return false;
        }else{
              document.getElementById('factoryMaterial2').innerHTML = "";
        }
    }
}

function compare(){
    
    let area_all = document.forms["myForm"]["nineteen"].value;
    let bulit_all = document.forms["myForm"]["twenty_two"].value;

    if (area_all > bulit_all) {
       
        document.getElementById('area').innerHTML = "Land area is larger than Buit Up Area ";
    } else {
        document.getElementById('area').innerHTML = "Buit Up area is smaller than Land Area ";
    }
}

// function compare2(){
    
//     let area_all = document.forms["myForm"]["nineteen"].value;
//     let bulit_all = document.forms["myForm"]["twenty_two"].value;

//     if (area_all < bulit_all) {
       
//         document.getElementById('built').innerHTML = "Buit Up area is smaller than Land Aera";
//     } else {
//         document.getElementById('built').innerHTML = "Land area is larger than Buit Up Area ";
//     }
// }