function validateForm() {
    let doc_1 = document.forms["myForm"]["doc_name"].value;
    let issue_Date = document.forms["myForm"]["issue_date"].value;
    let expire_Date = document.forms["myForm"]["expire_date"].value;
    let file_upload = document.forms["myForm"]["file"].value;
    var fileInput1 = document.getElementById('file123').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);



    if (doc_1 == "") {
        document.getElementById('name').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('name').innerHTML = "";
    }
    if (issue_Date == "") {
        document.getElementById('issue').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('issue').innerHTML = "";
    }
    if (expire_Date == "") {
        document.getElementById('expire').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('expire').innerHTML = "";
    }
    if (file_upload == "") {
        document.getElementById('upoadFile').innerHTML = " Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('upoadFile').innerHTML = "";
        if (fileInput_Result1 == false) {

            document.getElementById('upoadFile').innerHTML = " Valid file format required(In .pdf)";
            return false;
        } else {

            document.getElementById('upoadFile').innerHTML = "";
        }

    }

}    

function valid(){
    console.log("functigrtgj")
    //   let docName = document.forms["myForm1"]["doc_name1"].value;
      let file1 = document.forms["myForm1"]["file2"].value;
      var fileinput = document.getElementById('file_file1').value;
      var allowedExtensions_1 = /(\.pdf)$/i;
      let result = allowedExtensions_1.test(fileinput);

    //   if (docName == "") {
    //     document.getElementById('doc_namee').innerHTML = " Please fill the required detail  ";
    //     return false;
    // } else {
    //     document.getElementById('doc_namee').innerHTML = "";
    // }
      if (file1 == "") {
        document.getElementById('file_file').innerHTML = " Please upload the file in pdf format only";
        return false;
    } else {
        //document.getElementById('file_file').innerHTML = "";
        if (result == false) {

            document.getElementById('file_file').innerHTML = " Valid file format required(In .pdf)";
            return false;
        } else {

            document.getElementById('file_file').innerHTML = "";
        }

    }
}