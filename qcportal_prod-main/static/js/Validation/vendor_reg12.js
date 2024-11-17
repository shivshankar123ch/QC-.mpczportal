////form Validation
function validateForm() {
    console.log("eleve")
    let pan_name = document.forms["myForm"]["thirteen"].value;
    let PanCard = document.forms["myForm"]["fourteen"].value;
    let panNumber = document.getElementById('panCard').value;
    let panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    let panResult = panRGEX.test(panNumber);

    let V_date_issue_t = document.forms["myForm"]["fifteen"].value;

    let InputNameChoseDoc = document.forms["myForm"]["sixteen"].value;
    var fileInput1 = document.getElementById('inputNameChoseDoc').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);

    let Twenty = document.forms["myForm"]["twenty"].value;

    let Twenty_one = document.forms["myForm"]["twenty_one"].value;
    let gstNumber = document.getElementById('inputName_12').value;
    let gstRGEX = /^([0-9]){2}([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}([0-9]){1}([a-zA-Z]){1}([0-9]){1}?$/;
    let gstResult = gstRGEX.test(gstNumber);

    let Twenty_two = document.forms["myForm"]["twenty_two"].value;
    var fileInput2 = document.getElementById('inputName_31').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);

    let Four = document.forms["myForm"]["five"].value;
    var fileInput3 = document.getElementById('inputName_2').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);

    let Four23 = document.forms["myForm"]["four"].value;
    var fileInput4 = document.getElementById('inputName_231').value;
    let fileInput_Result4 = allowedExtensions.test(fileInput4);



    if (pan_name == "") {
        document.getElementById('panName').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('panName').innerHTML = "";
    }
    if (PanCard == "") {
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

    if (V_date_issue_t == "") {
        document.getElementById('issueDate').innerHTML = "Please fill the required field";
        return false;
    } else {
        document.getElementById('issueDate').innerHTML = "";
    }

    if (InputNameChoseDoc == "") {
        document.getElementById('upload1').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        // /document.getElementById('upload1').innerHTML = "";
        if (fileInput_Result1 == false) {
            document.getElementById('upload1').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            //document.getElementById('upload1').innerHTML = "";
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

    if (Twenty == "") {
        document.getElementById('data1').innerHTML = "Please fill the required field";
        return false;
    } else {
        document.getElementById('data1').innerHTML = "";
    }



    if (Twenty_one == "") {
        document.getElementById('gst_no').innerHTML = "Please fill the required field";
        return false;
    } else {
//        if (gstResult == false) {
//            document.getElementById('gst_no').innerHTML = " Please fill the valid GST number(11AAAAA1111Z1A1 format) ";
//            return false;
//        } else {
//            document.getElementById('gst_no').innerHTML = "";
//        }
         document.getElementById('gst_no').innerHTML = "";
    }
    // if (Twenty_one == "") {
    //     document.getElementById('Twenty_one').innerHTML = " Please fill the required field";
    //     return false;
    // } else {
    //     // document.getElementById('Twenty_one').innerHTML = "";
    //     if (gstResult == false) {
    //         document.getElementById('Twenty_one').innerHTML = "  Please fill the valid GST number(11AAAAA1111Z1A1 format)";
    //         return false;
    //     } else {
    //         document.getElementById('Twenty_one').innerHTML = "";
    //     }
    // }

    if (Twenty_two == "") {
        document.getElementById('Twenty_two').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result2 == false) {
            document.getElementById('Twenty_two').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            //document.getElementById('Twenty_two').innerHTML = "";
            const oFile = document.getElementById("inputName_31").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_31").value = "";
                return false;

            } else {
                document.getElementById('Twenty_two').innerHTML = "";
            }
        }
    }

    if (Four == "") {
        document.getElementById('Four1').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result3 == false) {
            document.getElementById('Four1').innerHTML = "Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            //document.getElementById('Four1').innerHTML = "";
            const oFile = document.getElementById("inputName_2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_2").value = "";
                return false;

            } else {
                document.getElementById('Four1').innerHTML = "";
            }
        }
    }


    if (Four23 == "") {
        document.getElementById('Four23').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result4 == false) {
            document.getElementById('Four23').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('Four23').innerHTML = "";
            const oFile = document.getElementById("inputName_231").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("inputName_231").value = "";
                return false;

            } else {
                document.getElementById('Four23').innerHTML = "";
            }
        }
    }
}