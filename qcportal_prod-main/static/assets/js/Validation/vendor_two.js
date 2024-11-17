function validateForm() {
    
    let subjectMaterial = document.forms["myForm"]["subject"].value;
    let material2 = document.forms["myForm"]["Material"].value;
    let material3 = document.forms["myForm"]["Specification"].value;
    let material4 = document.forms["myForm"]["type_test_report"].value;
    var fileInput1 = document.getElementById('type_test_report1').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);
    let report = document.forms["myForm"]["gtp_and_drawing"].value;
    var fileInput2 = document.getElementById('gtp_and_drawing1').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);

    let report1 = document.forms["myForm"]["others"].value;
    var fileInput3 = document.getElementById('others1').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);


    if (subjectMaterial == "") {
        document.getElementById('select1').innerHTML = " Please select the required field  ";
        return false;
    } else {
        document.getElementById('select1').innerHTML = " ";
    }

    if (material2 == "") {
        document.getElementById('select2').innerHTML = "Please select the required field  ";
        return false;
    } else {
        document.getElementById('select2').innerHTML = " ";
    }

    if (material3 == "") {
        document.getElementById('select3').innerHTML = "Please select the required field  ";
        return false;
    } else {
        document.getElementById('select3').innerHTML = " ";
    }
    if(material4 == ""){
        document.getElementById('upload1').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('upload1').innerHTML = "";
        if(fileInput_Result1 == false)
        {
            document.getElementById('upload1').innerHTML = " Please Upload valid file format(In .pdf format).. ";
            return false;
        }else{
              document.getElementById('upload1').innerHTML = "";
        }
    }
    if(report == ""){
        document.getElementById('upload2').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('upload2').innerHTML = "";
        if(fileInput_Result2 == false)
        {
            document.getElementById('upload2').innerHTML = " Please Upload valid file format(In .pdf format).. ";
            return false;
        }else{
              document.getElementById('upload2').innerHTML = "";
        }
    }
    if(report1 == ""){
        document.getElementById('upload3').innerHTML = "Please upload the file in pdf format only";
        return false;
    }else {
        //document.getElementById('upload3').innerHTML = "";
        if(fileInput_Result3 == false)
        {
            document.getElementById('upload3').innerHTML = " Please Upload valid file format(In .pdf format).. ";
            return false;
        }else{
              document.getElementById('upload3').innerHTML = "";
        }
    }

}