function validateForm() {
    let Work_experience = document.forms["myForm"]["doc_name"].value;
    let fileee = document.forms["myForm"]["file"].value;
    console.log("fileeee",fileee)
    var fileInput1 = document.getElementById('file_id').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);


    if (Work_experience == "") {
       document.getElementById('number').innerHTML = " Please fill the required detail  ";
       return false;
    } else {
       document.getElementById('number').innerHTML = "";
    }

    if (fileee == "") {
      document.getElementById('file_1').innerHTML = "Please the Upload file(In .pdf format)";
      return false;
  } else {
      //document.getElementById('Twenty_two').innerHTML = "";
      if (fileInput_Result1 == false) {
          document.getElementById('file_1').innerHTML = "  Please Upload valid file format(In .pdf) ";
          return false;
      } else {
          // document.getElementById('file_1').innerHTML = "";
          const oFile = document.getElementById("file_id").files[0].size / 1024 / 1024;
          if (oFile > 2) {
              alert("File size must be less than or equal to 2 MB");
              document.getElementById("file_id").value = "";
              return false;

          } else {
              document.getElementById('file_1').innerHTML = "";
          }
      }
  }


   //  if (fileee == "") {
   //     console.log("come idddddddddddddddfff")
   //     document.getElementById('file_1').innerHTML = " Please upload the file in pdf format only";
   //     return false;
   //  } else {
   //     //document.getElementById('file_1').innerHTML = "";
   //     if (fileInput_Result1 == false) {
   //        console.log("hii1");
   //        document.getElementById('file_1').innerHTML = " Valid file format required(In .pdf)";
   //        return false;
   //     } else {
   //        console.log("hii12");
   //        document.getElementById('file_1').innerHTML = "";
   //     }
   //  }
 }