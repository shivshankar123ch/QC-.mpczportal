console.log("hii");

function validateForm() {
    let doc_office = document.forms["myForm"]["office"].value;
    let doc_name_1 = document.forms["myForm"]["doc_name"].value;
    let doc_issue = document.forms["myForm"]["issue_date"].value;
    let expire_issue = document.forms["myForm"]["expire_date"].value;
    let file_dtaa = document.forms["myForm"]["file"].value;
    var fileInput1 = document.getElementById('file_inputt').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);



    if (doc_office == "") {
        document.getElementById('office_1').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('office_1').innerHTML = "";
    }
    if (doc_name_1 == "") {
        document.getElementById('name_1').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('name_1').innerHTML = "";
    }
    if (doc_issue == "") {
        document.getElementById('issue').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('issue').innerHTML = "";
    }
    if (expire_issue == "") {
        document.getElementById('expire').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('expire').innerHTML = "";
    }
    if (file_dtaa == "") {
        document.getElementById('file_11').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileInput_Result1 == false) {

            document.getElementById('file_11').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            //document.getElementById('file_11').innerHTML = "";
            const oFile = document.getElementById("file_inputt").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("file_inputt").value = "";
                return false;

            } else {
                document.getElementById('file_11').innerHTML = "";
            }
        }
    }
}

function validateForm1() {
    let office_11 = document.forms["myForm"]["office"].value;
    let doc11 = document.forms["myForm"]["doc_name"].value;
    let isu = document.forms["myForm"]["issue_date"].value;
    let expirr = document.forms["myForm"]["expire_date"].value;
    let filet = document.forms["myForm"]["file"].value;
    var fileInput2 = document.getElementById('file_main').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);


    if (office_11 == "") {
        document.getElementById('ioffice').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('ioffice').innerHTML = "";
    }
    if (doc11 == "") {
        document.getElementById('docName').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('docName').innerHTML = "";
    }
    if (isu == "") {
        document.getElementById('issueDate').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('issueDate').innerHTML = "";
    }
    if (expirr == "") {
        document.getElementById('expireDate').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('expireDate').innerHTML = "";
    }
    if (filet == "") {
        document.getElementById('uploadFilee').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileInput_Result2 == false) {

            document.getElementById('uploadFilee').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {

            //document.getElementById('uploadFilee').innerHTML = "";
            const oFile = document.getElementById("file_main").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("file_main").value = "";
                return false;

            } else {
                document.getElementById('uploadFilee').innerHTML = "";
            }

        }
    }
}