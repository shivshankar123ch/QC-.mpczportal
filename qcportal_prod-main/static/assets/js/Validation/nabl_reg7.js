function validateForm() {
    console.log("function fire")
    let Work_experience = document.forms["myForm"]["work_experience"].value;
    let Turn_over = document.forms["myForm"]["turn_over"].value;
    let over_4 = document.forms["myForm"]["latitude"].value;
    let lat = document.getElementById("turn_over2").value;
    let pattern = new RegExp('^-?([1-8]?[1-9]|[1-9]0)\\.{1}\\d{1,6}');
    let data1 = pattern.test(lat);
    let over_5 = document.forms["myForm"]["longitude"].value;
    let long = document.getElementById("turn_over3").value;
    let data2 = pattern.test(long);



    if (Work_experience == "") {
        console.log("if me ayaaaa")
        document.getElementById('work').innerHTML = " Please fill the required field  ";
        return false;
    } else {
        document.getElementById('work').innerHTML = " ";
    }

    if (Turn_over == "") {
        document.getElementById('over_45').innerHTML = "Please fill the required field  ";
        return false;
    } else {
        document.getElementById('over_45').innerHTML = " ";
    }



    if (over_4 == "") {
        document.getElementById('over_4').innerHTML = "Please fill the required field (example 23.1996633)  ";
        return false;
    } else {
        //document.getElementById('over_4').innerHTML = "";
        if (data1 == false) {
            document.getElementById('over_4').innerHTML = "  Please fill the valid formate(23.1996633) ";
            return false;
        } else {
            document.getElementById('over_4').innerHTML = "";
        }
    }

    if (over_5 == "") {
        document.getElementById('over_5').innerHTML = "Please fill the required field (example 77.2658051)";
        return false;
    } else {
        //document.getElementById('over_5').innerHTML = "";
        if (data2 == false) {
            document.getElementById('over_5').innerHTML = "  Please fill the valid formate(77.2658051) ";
            return false;
        } else {
            document.getElementById('over_5').innerHTML = "";
        }
    }

}