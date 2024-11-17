//form validation
function validateForm() {
    let Work_experience = document.forms["myForm"]["work_experience"].value;
    let Turn_over = document.forms["myForm"]["turn_over"].value;
    let select_1 = document.forms["myForm"]["VendorType"].value;
    console.log("ayeeee",select_1)

    if (Work_experience == "") {
        document.getElementById('workk').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('workk').innerHTML = "";
    }
    if (Turn_over == "") {
        document.getElementById('over').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('over').innerHTML = "";
    }
    if (select_1 == "") {
        console.log("come in slect")
        document.getElementById('select2').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('select2').innerHTML = "";
    }
}