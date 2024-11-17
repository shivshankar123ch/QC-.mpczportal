function validateForm() {

    let amount = document.forms["myForm"]["v_balance_sheet_1"].value;
    let rupees = document.forms["myForm"]["Amount"].value;

    // var fileInput2 = document.getElementById('authentication_1').value;
    // console.log(fileInput2);
    
    let amount2 = document.forms["myForm"]["v_balance_sheet_2"].value;
    let rupees2 = document.forms["myForm"]["Amount2"].value;

    // var fileInput3 = document.getElementById('authentication_31').value;
    // console.log(fileInput3);
    
    let amount3 = document.forms["myForm"]["v_balance_sheet_3"].value;
    let rupees3 = document.forms["myForm"]["Amount3"].value;

    // var fileInput5 = document.getElementById('authentication_11').value;

    let amount4 = document.forms["myForm"]["v_balance_sheet_4"].value;
    let rupees4 = document.forms["myForm"]["Amount4"].value;


    // var fileInput6 = document.getElementById('authentication_23').value;


    let amount5 = document.forms["myForm"]["v_balance_sheet_5"].value;
    let rupees5 = document.forms["myForm"]["Amount5"].value;


    // var fileInput7 = document.getElementById('authentication_45').value;


    let amount6 = document.forms["myForm"]["v_balance_sheet_6"].value;
    let rupees6 = document.forms["myForm"]["Amount6"].value;





    if (amount === "") {
        document.getElementById('amount_1').innerHTML = " Please fill the required detail  "
        return false;

    } else {
        document.getElementById('amount_1').innerHTML = " "

    }
    if (rupees == "") {
        document.getElementById('rupess1').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('rupess1').innerHTML = "";
    }



    if (amount2 === "") {
        document.getElementById('data').innerHTML = " Please fill the required detail  "
        return false;

    } else {
        document.getElementById('data').innerHTML = " "

    }
    if (rupees2 == "") {
        document.getElementById('reu1').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('reu1').innerHTML = "";
    }






   
if (amount3 === "") {
    document.getElementById('data2').innerHTML = " Please fill the required detail  "
    return false;

} else {
    document.getElementById('data2').innerHTML = " "

}
if (rupees3 == "") {
    document.getElementById('res3').innerHTML = " Please fill the required detail  ";
    return false;
} else {
    document.getElementById('res3').innerHTML = "";
}


if (amount4 === "") {
    document.getElementById('data4').innerHTML = " Please fill the required detail  "
    return false;

} else {
    document.getElementById('data4').innerHTML = " "

}
if (rupees4 == "") {
    document.getElementById('res4').innerHTML = " Please fill the required detail  ";
    return false;
} else {
    document.getElementById('res4').innerHTML = "";
}


if (amount5 === "") {
    document.getElementById('data5').innerHTML = " Please fill the required detail  "
    return false;

} else {
    document.getElementById('data5').innerHTML = " "

}
if (rupees5 == "") {
    document.getElementById('res5').innerHTML = " Please fill the required detail  ";
    return false;
} else {
    document.getElementById('res5').innerHTML = "";
}


if (amount6 === "") {
    document.getElementById('data6').innerHTML = " Please fill the required detail  "
    return false;

} else {
    document.getElementById('data6').innerHTML = " "

}
if (rupees6 == "") {
    document.getElementById('res6').innerHTML = " Please fill the required detail  ";
    return false;
} else {
    document.getElementById('res6').innerHTML = "";
}




}
