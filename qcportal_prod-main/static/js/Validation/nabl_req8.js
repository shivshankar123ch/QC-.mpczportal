function validateForm() {

    let N_office_name_supply_01 = document.forms["myForm"]["Accreditation_Certificate_office"].value;
    let N_office_name_supply_02 = document.forms["myForm"]["Accreditation_Certificate_doc_name"].value;
    let N_office_name_supply_03 = document.forms["myForm"]["Accreditation_Certificate_issue_date1"].value;
    let N_office_name_supply_04 = document.forms["myForm"]["Accreditation_Certificate_expire_date"].value;
    let File_name_supply_05 = document.forms["myForm"]["Accreditation_Certificate_file"].value;
    var fileInput1 = document.getElementById('file_name_supply_05').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);
    let N_office_name_supply_06 = document.forms["myForm"]["Accreditation_office"].value;
    let N_office_name_supply_07 = document.forms["myForm"]["Accreditation_Certificate_doc_name_021"].value;
    let N_office_name_supply_08 = document.forms["myForm"]["Accreditation_issue_date"].value;
    let N_office_name_supply_09 = document.forms["myForm"]["Accreditation_expire_date"].value;
    let N_file_supply_10 = document.forms["myForm"]["Accreditation_file"].value;
    var fileInput2 = document.getElementById('n_file_supply_10').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);

    let N_name_supply_11 = document.forms["myForm"]["Pan_Card_doc_name"].value;
    let panNumber = document.getElementById('n_name_supply_11').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);

    let issueDate_012 = document.forms["myForm"]["Pan_Card_issue_date"].value;
    let N_Nabl_Pan_Card_details_013 = document.forms["myForm"]["Pan_Card_file"].value;
    var fileInput3 = document.getElementById('n_Nabl_Pan_Card_details_013').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);
    let N_office_name_supply_014 = document.forms["myForm"]["GST_doc_name"].value;
    let N_office_name_supply7 = document.forms["myForm"]["GST_issue_date"].value;
    let gstFile_015 = document.forms["myForm"]["GST_file"].value;
    var fileInput4 = document.getElementById('n_Nabl_GST_Certificate_015').value;
    let fileInput_Result4 = allowedExtensions.test(fileInput4);

    if (N_office_name_supply_01 == "") {
        document.getElementById('N_office_name_supply_01').innerHTML = " Please fill the required field   ";
        return false;
    } else {
        document.getElementById('N_office_name_supply_01').innerHTML = " ";
    }
    if (N_office_name_supply_02 == "") {
        document.getElementById('N_office_name_supply_02').innerHTML = " Please fill the required field   ";
        return false;
    } else {
        document.getElementById('N_office_name_supply_02').innerHTML = " ";
    }
    if (N_office_name_supply_03 == "") {
        document.getElementById('N_office_name_supply_03').innerHTML = " Please fill the required field   ";
        return false;
    } else {
        document.getElementById('N_office_name_supply_03').innerHTML = " ";
    }
    if (N_office_name_supply_04 == "") {
        document.getElementById('N_office_name_supply_04').innerHTML = " Please fill the required field   ";
        return false;
    } else {
        document.getElementById('N_office_name_supply_04').innerHTML = " ";
    }
    if (File_name_supply_05 == "") {
        document.getElementById('File_name_supply_05').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('File_name_supply_05').innerHTML = " ";
        if (fileInput_Result1 == false) {

            document.getElementById('File_name_supply_05').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            //document.getElementById('File_name_supply_05').innerHTML = "";
            const oFile = document.getElementById("file_name_supply_05").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("file_name_supply_05").value = "";
                return false;

            } else {
                document.getElementById('File_name_supply_05').innerHTML = "";
            }
        }
    }
    if (N_office_name_supply_06 == "") {
        document.getElementById('N_office_name_supply_06').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_06').innerHTML = " ";
    }
    if (N_office_name_supply_07 == "") {
        document.getElementById('N_office_name_supply_07').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_07').innerHTML = " ";
    }
    if (N_office_name_supply_08 == "") {
        document.getElementById('N_office_name_supply_08').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_08').innerHTML = " ";
    }
    if (N_office_name_supply_08 == "") {
        document.getElementById('N_office_name_supply_08').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_08').innerHTML = " ";
    }
    if (N_office_name_supply_09 == "") {
        document.getElementById('N_office_name_supply_09').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_09').innerHTML = " ";
    }
    if (N_file_supply_10 == "") {
        document.getElementById('N_file_supply_10').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('N_file_supply_10').innerHTML = " ";
        if (fileInput_Result2 == false) {

            document.getElementById('N_file_supply_10').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            //document.getElementById('N_file_supply_10').innerHTML = "";
            const oFile = document.getElementById("n_file_supply_10").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("n_file_supply_10").value = "";
                return false;

            } else {
                document.getElementById('N_file_supply_10').innerHTML = "";
            }
        }
    }

    if (N_name_supply_11 == "") {
        document.getElementById('pan_no').innerHTML = "  Please fill the required fieldss";
        return false;
    } else {
        //document.getElementById('pan_no').innerHTML = "";
        if (panResult == false) {
            document.getElementById('pan_no').innerHTML = "  Please fill the valid Pan number(ABCTY1234D format) ";
            return false;
        } else {
            document.getElementById('pan_no').innerHTML = "";
        }
    }
    // if (N_name_supply_11 == "") {
    //     document.getElementById('N_name_supply_11').innerHTML = " Please fill the required field";
    //     return false;
    // } else {
    //     document.getElementById('N_name_supply_11').innerHTML = " ";
    // }
    if (issueDate_012 == "") {
        document.getElementById('issueDate_012').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('issueDate_012').innerHTML = " ";
    }
    if (N_Nabl_Pan_Card_details_013 == "") {
        document.getElementById('N_Nabl_Pan_Card_details_013').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('N_Nabl_Pan_Card_details_013').innerHTML = " ";
        if (fileInput_Result3 == false) {

            document.getElementById('N_Nabl_Pan_Card_details_013').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            //document.getElementById('N_Nabl_Pan_Card_details_013').innerHTML = "";
            const oFile = document.getElementById("n_Nabl_Pan_Card_details_013").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("n_Nabl_Pan_Card_details_013").value = "";
                return false;

            } else {
                document.getElementById('N_Nabl_Pan_Card_details_013').innerHTML = "";
            }
        }
    }
    if (N_office_name_supply_014 == "") {
        document.getElementById('N_office_name_supply_014').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply_014').innerHTML = " ";
    }
    if (N_office_name_supply7 == "") {
        document.getElementById('N_office_name_supply7').innerHTML = " Please fill the required field";
        return false;
    } else {
        document.getElementById('N_office_name_supply7').innerHTML = " ";
    }
    if (gstFile_015 == "") {
        document.getElementById('gstFile_015').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {
        // document.getElementById('gstFile_015').innerHTML = " ";
        if (fileInput_Result4 == false) {

            document.getElementById('gstFile_015').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            // document.getElementById('gstFile_015').innerHTML = "";
            const oFile = document.getElementById("n_Nabl_GST_Certificate_015").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("n_Nabl_GST_Certificate_015").value = "";
                return false;

            } else {
                document.getElementById('gstFile_015').innerHTML = "";
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
