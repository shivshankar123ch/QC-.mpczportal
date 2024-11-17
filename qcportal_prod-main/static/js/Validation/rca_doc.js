function validateForm() {
    console.log("function fire")
    let Electricity = document.forms["myForm"]["one"].value;
    let file_up1 = document.forms["myForm"]["one"].value;
    let file_upload1 = document.getElementById("v_upload_file1").value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(file_upload1);
   
    let plant = document.forms["myForm"]["five"].value;
    let file_up2 = document.forms["myForm"]["eight"].value;
    let file_upload2 = document.getElementById("v_upload_file2").value;
    let fileInput_Result2 = allowedExtensions.test(file_upload2);

    let testing = document.forms["myForm"]["nine"].value;
    let file_up3 = document.forms["myForm"]["twelve"].value;
    let file_upload3 = document.getElementById("v_upload_file3").value;
    let fileInput_Result3 = allowedExtensions.test(file_upload3);


    let certificate = document.forms["myForm"]["thrteen"].value;
    let file_up4 = document.forms["myForm"]["sixteen"].value;
    let file_upload4 = document.getElementById("v_upload_file4").value;
    let fileInput_Result4 = allowedExtensions.test(file_upload4);





    if (Electricity == "") {
        document.getElementById('electric').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('electric').innerHTML = " ";
    }

    if (file_up1 == "") {
        document.getElementById('file1').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result1 == false) {
            document.getElementById('file1').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file1').innerHTML = "";
            const oFile = document.getElementById("v_upload_file1").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file1").value = "";
                return false;

            } else {
                document.getElementById('file1').innerHTML = "";
            }
        }
    }

    //----------------------------------------------------------------------------------------------------------------------------

    if (plant == "") {
        document.getElementById('mech').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('mech').innerHTML = " ";
    }

    if (file_up2 == "") {
        document.getElementById('file2').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result2 == false) {
            document.getElementById('file2').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file2').innerHTML = "";
            const oFile = document.getElementById("v_upload_file2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file2").value = "";
                return false;

            } else {
                document.getElementById('file2').innerHTML = "";
            }
        }
    }

    //-------------------------------------------------------------------------------------------------------------------------------

    if (testing == "") {
        console.log("if me ayaaaa")
        document.getElementById('test').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('test').innerHTML = " ";
    }

    if (file_up3 == "") {
        document.getElementById('file3').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result3 == false) {
            document.getElementById('file3').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file3').innerHTML = "";
            const oFile = document.getElementById("v_upload_file3").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file3").value = "";
                return false;

            } else {
                document.getElementById('file3').innerHTML = "";
            }
        }
    }

    //----------------------------------------------------------------------------------------------------------------------------

    if (certificate == "") {
        console.log("if me ayaaaa")
        document.getElementById('cert').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('cert').innerHTML = " ";
    }

    if (file_up4 == "") {
        document.getElementById('file4').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result4 == false) {
            document.getElementById('file4').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file4').innerHTML = "";
            const oFile = document.getElementById("v_upload_file4").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_upload_file4").value = "";
                return false;

            } else {
                document.getElementById('file4').innerHTML = "";
            }
        }
    }

}