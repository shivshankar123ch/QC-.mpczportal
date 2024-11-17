console.log("hii maya");
//form validation
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
}