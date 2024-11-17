function validateForm() {
    console.log("function fire")
    let product_1 = document.forms["myForm"]["product"].value;
    let specificationn = document.forms["myForm"]["specification"].value;
    let test = document.forms["myForm"]["Test"].value;

    if (product_1 == "") {
        console.log("if me ayaaaa")
        document.getElementById('User').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('User').innerHTML = " ";
    }

    if (specificationn == "") {
        document.getElementById('specification_1').innerHTML = "Please fill the required field  ";
        return false;
    } else {
        document.getElementById('specification_1').innerHTML = " ";
    }
    if (test == "") {
        document.getElementById('Test_1').innerHTML = "Please fill the required field  ";
        return false;
    } else {
        document.getElementById('Test_1').innerHTML = " ";
    }
}