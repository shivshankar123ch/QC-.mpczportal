console.log("hiii123");

function validateForm() {
    let names = document.forms["myForm"]["nameData"].value;
    let Designations = document.forms["myForm"]["designation"].value;
    let Dobs = document.forms["myForm"]["dob"].value;
    let Firms = document.forms["myForm"]["firm"].value;
    let mobileNumber = document.forms["myForm"]["mobile"].value;

    let phoneNumber = document.getElementById('mobile1').value;
    let phoneRGEX = /^[6789]\d{9}$/;
    let phoneResult = phoneRGEX.test(phoneNumber);
    let emailAddress = document.forms["myForm"]["email"].value;
    let emailData = document.getElementById('email1').value;
    let emailLowerCase = emailData.toLowerCase();
    let emailRgex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    let emailResult = emailRgex.test(emailLowerCase);
    let V_upload_file_material = document.forms["myForm"]["photo"].value;
    var fileInput6 = document.getElementById('v1_upload_file_material').value;
    var allowedExtensions3 = /(http(s?):)|([/|.|\w|\s])*\.(?:jpg|jpeg|png)/
    let fileInput6_Result6 = allowedExtensions3.test(fileInput6);


    if (names == "") {
        document.getElementById('Names').innerHTML = " Please fill the required details";
    } else {
        document.getElementById('Names').innerHTML = "";
    }
    if (Designations == "") {
        document.getElementById('Designations').innerHTML = " Please fill the required details";
    } else {

        document.getElementById('Designations').innerHTML = "";
    }
    if (Dobs == "") {
        document.getElementById('Dobs').innerHTML = " Please fill the required details";
    } else {

        document.getElementById('Dobs').innerHTML = "";
    }
    if (Firms == "") {

        document.getElementById('Firms_1').innerHTML = " Please fill the required details";
    } else {

        document.getElementById('Firms_1').innerHTML = "";
    }
    if (mobileNumber == "") {
        console.log("hiii999oooo");
        document.getElementById('mobileNumber').innerHTML = " Please fill the required details";
    } else {
        console.log("hiii999");
        //document.getElementById('mobileNumber').innerHTML = "";
        if (phoneResult == false) {
            document.getElementById('mobileNumber').innerHTML = " Please fill the required details";
            return false;
        } else {
            document.getElementById('mobileNumber').innerHTML = "";
        }
    }
    if (emailAddress == "") {
        document.getElementById('emailAddress').innerHTML = "Please fill the required details ";
        return false;
    } else {
        if (emailResult == false) {
            document.getElementById('emailAddress').innerHTML = " Please fill the required details";
            return false;
        } else {
            document.getElementById('emailAddress').innerHTML = "";
        }
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
}