function errorFrom(inp_id){
    let inp = document.getElementById(inp_id);
    if(inp.value == ""){
    let x = document.getElementById(inp_id+"_span");

    x.innerHTML = "Please fill the required details";
    }else{
    let x = document.getElementById(inp_id+"_span");
    x.innerHTML = "";
    }
}

function validateForm(){
    let Material_1 = document.forms["myForm"]["Material"].value;
    let Specification_1 = document.forms["myForm"]["Specification"].value;
    let upload1 = document.forms["myForm"]["type_test_report"].value;
    var fileInput1 = document.getElementById('type_test_report1').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);
    let upload2 = document.forms["myForm"]["gtp_and_drawing"].value;
    var fileInput2 = document.getElementById('gtp_and_drawing1').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);
    let upload3 = document.forms["myForm"]["others"].value;
    var fileInput3 = document.getElementById('others1').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);

    if (Material_1 == "") {
        document.getElementById('country_span').innerHTML = " Please select the required field  ";
        return false;
    } else {
        document.getElementById('country_span').innerHTML = " ";
    }
    if (Specification_1 == "") {
        document.getElementById('Specification_1').innerHTML = " Please select the required field  ";
        return false;
    } else {
        document.getElementById('Specification_1').innerHTML = " ";
    }
    if (upload1 == "") {
        document.getElementById('upload1').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileInput_Result1 == false) {
            document.getElementById('upload1').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            // document.getElementById('upload1').innerHTML = "";
            const oFile = document.getElementById("type_test_report1").files[0].size / 1024 / 1024 ;
            if (oFile > 30) {
                alert("File size must be less than or equal to 30 MB");
                document.getElementById("type_test_report1").value = "";
                return false;

            } else {
                document.getElementById('upload1').innerHTML = "";
            }

        }
    }
    if (upload2 == "") {
        document.getElementById('upload2').innerHTML = "Please upload the file in pdf format only";
        return false;
    } else {

        if (fileInput_Result2 == false) {
            document.getElementById('upload2').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            // document.getElementById('upload2').innerHTML = "";
            const oFile = document.getElementById("gtp_and_drawing1").files[0].size / 1024 / 1024 ;
            if (oFile > 30) {
                alert("File size must be less than or equal to 30 MB");
                document.getElementById("gtp_and_drawing1").value = "";
                return false;

            } else {
                document.getElementById('upload2').innerHTML = "";
            }
        }
    }
    if (fileInput3 !== "") {
        
        if (fileInput_Result3 == false) {
            document.getElementById('upload3').innerHTML = "Valid file format required(In .pdf)";
            return false;
        } else {
            //document.getElementById('upload3').innerHTML = "";
            const oFile = document.getElementById("others1").files[0].size / 1024 / 1024;
            if (oFile > 4) {
                alert("File size must be less than or equal to 4 MB");
                document.getElementById("others1").value = "";
                return false;

            } else {
                document.getElementById('upload3').innerHTML = "";
            }
        }
    } else {
        console.log("others2");
        
    }
    if(!confirm("Are you sure you want to submit?")) {
        return false;
      }
      this.form.submit();
    

}