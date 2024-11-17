function validateForm() {
    var two_2 = document.forms["myForm"]["two"].value;
    var three_3 = document.forms["myForm"]["three"].value;
    var four_4 = document.forms["myForm"]["four"].value;
    var fileInput1 = document.getElementById('v_office_name_supply_4_file1').value;
    var allowedExtensions = /(\.pdf)$/i;
    let fileInput_Result1 = allowedExtensions.test(fileInput1);
    let aadharRGEX = /^\d{12}$/;
    let aadharResult1 = aadharRGEX.test(two_2);

    if (two_2 == "") {
        document.getElementById('doc1').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('doc1').innerHTML = "";
    }
    if (aadharResult1 == false) {
        document.getElementById('doc1').innerHTML = " Please fill the valid Aadhar number ";
        return false;
    } else {
        document.getElementById('doc1').innerHTML = "";
    }
    if (three_3 == "") {
        document.getElementById('issue1').innerHTML = "Please fill the required detail   ";
        return false;
    } else {
        document.getElementById('issue1').innerHTML = "";
    }


    if (four_4 == "") {
        document.getElementById('file1').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result1 == false) {
            document.getElementById('file1').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file1').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supply_4_file1").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supply_4_file1").value = "";
                return false;

            } else {
                document.getElementById('file1').innerHTML = "";
            }
        }
    }


    // if (four_4 == "") {
    //     document.getElementById('file1').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file1').innerHTML = "";
    //     if (fileInput_Result1 == false) {
    //         console.log("hii1");
    //         document.getElementById('file1').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         console.log("hii12");
    //         document.getElementById('file1').innerHTML = "";
    //     }
    // }

    var gstNUm = document.forms["myForm"]["six"].value;
    var issue1 = document.forms["myForm"]["seven"].value;
    // var expire1 = document.forms["myForm"]["eight"].value;
    var upload1 = document.forms["myForm"]["nine"].value;
    var fileInput2 = document.getElementById('v_office_name_supplyfile2').value;
    let fileInput_Result2 = allowedExtensions.test(fileInput2);
    let gstRGEX = /^([0-9]){2}([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}([0-9]){1}([a-zA-Z]){1}([0-9]){1}?$/;
    let gstResult = gstRGEX.test(gstNUm);

    if (gstNUm == "") {
        document.getElementById('doc2').innerHTML = " Please fill the required detail   ";
        return false;
    } else {
        document.getElementById('doc2').innerHTML = "";
    }
    // if (gstResult == false) {
    //     document.getElementById('doc2').innerHTML = " Please fill the valid GST number(11AAAAA1111Z1A1 format) ";
    //     return false;
    // } else {
    //     document.getElementById('doc2').innerHTML = "";
    // }
    if (issue1 == "") {
        document.getElementById('issue2').innerHTML = "Please fill the required detail   ";
        return false;
    } else {
        document.getElementById('issue2').innerHTML = "";
    }
    // if (expire1 == "") {
    //     document.getElementById('expire2').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire2').innerHTML = "";
    // }

    if (upload1 == "") {
        document.getElementById('file2').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result2 == false) {
            document.getElementById('file2').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file2').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile2").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile2").value = "";
                return false;

            } else {
                document.getElementById('file2').innerHTML = "";
            }
        }
    }

    // if (upload1 == "") {
    //     document.getElementById('file2').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file2').innerHTML = "";
    //     if (fileInput_Result2 == false) {
    //         document.getElementById('file2').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file2').innerHTML = "";
    //     }
    // }


    var number3 = document.forms["myForm"]["eleven"].value;
    var issue3 = document.forms["myForm"]["twelve"].value;
    // var expire3 = document.forms["myForm"]["thirteen"].value;
    var file3 = document.forms["myForm"]["fourteen"].value;
    var fileInput3 = document.getElementById('v_office_name_supplyfile3').value;
    let fileInput_Result3 = allowedExtensions.test(fileInput3);

    if (number3 == "") {
        document.getElementById('doc3').innerHTML = " Please fill the required detail   ";
        return false;
    } else {
        document.getElementById('doc3').innerHTML = "";
    }
    if (issue3 == false) {
        document.getElementById('issue3').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue3').innerHTML = "";
    }
    // if (expire3 == "") {
    //     document.getElementById('expire3').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire3').innerHTML = "";
    // }

    if (file3 == "") {
        document.getElementById('file3').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result3 == false) {
            document.getElementById('file3').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file3').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile3").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile3").value = "";
                return false;

            } else {
                document.getElementById('file3').innerHTML = "";
            }
        }
    }

    // if (file3 == "") {
    //     document.getElementById('file3').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file3').innerHTML = "";
    //     if (fileInput_Result3 == false) {
    //         document.getElementById('file3').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file3').innerHTML = "";
    //     }
    // }
    var number4 = document.forms["myForm"]["fifty_one"].value;
    var panNumber = document.getElementById('v_office_name_supplyPAN').value;
    var panRGEX = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    var panResult = panRGEX.test(panNumber);
    var issue4 = document.forms["myForm"]["fifty_two"].value;
    var file4 = document.forms["myForm"]["fifty_three"].value;
    var fileInput4 = document.getElementById('v_office_name_supplyfile4').value;
    let fileInput_Result4 = allowedExtensions.test(fileInput4);

    if (number4 == "") {
        document.getElementById('doc11').innerHTML = "Please fill the required detail ";
        return false;
    } else {
        if (panResult == false) {
            document.getElementById('doc11').innerHTML = "Please fill the valid Pan number(ABCTY1234D format)";
            return false;
        } else {
            document.getElementById('doc11').innerHTML = "";
        }
    }
    if (issue4 == false) {
        document.getElementById('issue11').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue11').innerHTML = "";
    }

    // if (file4 == "") {
    //     document.getElementById('file11').innerHTML = "Please the Upload file(In .pdf format)";
    //     return false;
    // } else {
    //     //document.getElementById('Twenty_two').innerHTML = "";
    //     if (fileInput_Result4 == false) {
    //         document.getElementById('file11').innerHTML = "  Please Upload valid file format(In .pdf) ";
    //         return false;
    //     } else {
    //         // document.getElementById('file11').innerHTML = "";
    //         const oFile = document.getElementById("v_office_name_supplyfile4").files[0].size / 1024 / 1024;
    //         if (oFile > 2) {
    //             alert("File size must be less than or equal to 2 MB");
    //             document.getElementById("v_office_name_supplyfile4").value = "";
    //             return false;

    //         } else {
    //             document.getElementById('file11').innerHTML = "";
    //         }
    //     }
    // }

    if (file4 == "") {
        document.getElementById('file11').innerHTML = " Please upload the file in pdf format only";
        return false;
    } else {
        document.getElementById('file11').innerHTML = "";
        // if (fileInput_Result4 == false) {
        //     document.getElementById('file11').innerHTML = " Valid file format required(In .pdf)";
        //     return false;
        // } else {
        //     document.getElementById('file11').innerHTML = "";
        // }
    }


    var number5 = document.forms["myForm"]["twentee_one"].value;
    var issue5 = document.forms["myForm"]["twentee_two"].value;
    var expire5 = document.forms["myForm"]["twentee_three"].value;
    var file_5 = document.forms["myForm"]["twentee_four"].value;
    var fileInput5 = document.getElementById('v_office_name_supplyfile5').value
    let fileInput_Result5 = allowedExtensions.test(fileInput5);


    if (number5 == "") {
        document.getElementById('doc5').innerHTML = "Please fill the required detail ";
        return false;
    } else {
        document.getElementById('doc5').innerHTML = "";
    }
    if (issue5 == false) {
        document.getElementById('issue5').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue5').innerHTML = "";
    }
    if (expire5 == "") {
        document.getElementById('expire5').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('expire5').innerHTML = "";
    }

    if (file_5 == "") {
        document.getElementById('file5').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result5 == false) {
            document.getElementById('file5').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file5').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile5").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile5").value = "";
                return false;

            } else {
                document.getElementById('file5').innerHTML = "";
            }
        }
    }

    // if (file_5 == "") {
    //     document.getElementById('file5').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file5').innerHTML = "";
    //     if (fileInput_Result5 == false) {
    //         document.getElementById('file5').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file5').innerHTML = "";
    //     }
    // }

    var number6 = document.forms["myForm"]["twentee_six"].value;
    var issue6 = document.forms["myForm"]["twentee_seven"].value;
    // var expire6 = document.forms["myForm"]["twentee_eight"].value;
    var file6 = document.forms["myForm"]["twentee_nine"].value;
    var fileInput6 = document.getElementById('v_office_name_supplyfile6').value
    let fileInput_Result6 = allowedExtensions.test(fileInput6);


    if (number6 == "") {
        document.getElementById('doc6').innerHTML = "Please fill the required detail ";
        return false;
    } else {
        document.getElementById('doc6').innerHTML = "";
    }
    if (issue6 == false) {
        document.getElementById('issue6').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue6').innerHTML = "";
    }
    // if (expire6 == "") {
    //     document.getElementById('expire6').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire6').innerHTML = "";
    // }

    if (file6 == "") {
        document.getElementById('file6').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result6 == false) {
            document.getElementById('file6').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file6').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile6").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile6").value = "";
                return false;

            } else {
                document.getElementById('file6').innerHTML = "";
            }
        }
    }

    // if (file6 == "") {
    //     document.getElementById('file6').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file6').innerHTML = "";
    //     if (fileInput_Result6 == false) {
    //         document.getElementById('file6').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file6').innerHTML = "";
    //     }
    // }

    var number7 = document.forms["myForm"]["thiety_one"].value;
    var issue7 = document.forms["myForm"]["thiety_two"].value;
    // var expire7 = document.forms["myForm"]["thiety_three"].value;
    var file7 = document.forms["myForm"]["thiety_four"].value;
    var fileInput7 = document.getElementById('v_office_name_supplyfile7').value
    let fileInput_Result7 = allowedExtensions.test(fileInput7);


    if (number7 == "") {
        document.getElementById('doc7').innerHTML = "Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('doc7').innerHTML = "";
    }
    if (issue7 == false) {
        document.getElementById('issue7').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue7').innerHTML = "";
    }
    // if (expire7 == "") {
    //     document.getElementById('expire7').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire7').innerHTML = "";
    // }

    if (file7 == "") {
        document.getElementById('file7').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result7 == false) {
            document.getElementById('file7').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file7').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile7").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile7").value = "";
                return false;

            } else {
                document.getElementById('file7').innerHTML = "";
            }
        }
    }

    // if (file7 == "") {
    //     document.getElementById('file7').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file7').innerHTML = "";
    //     if (fileInput_Result7 == false) {
    //         document.getElementById('file7').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file7').innerHTML = "";
    //     }
    // }
    var number8 = document.forms["myForm"]["thiety_six"].value;
    var issue8 = document.forms["myForm"]["thiety_seven"].value;
    // var expire8 = document.forms["myForm"]["thiety_eight"].value;
    var file8 = document.forms["myForm"]["thiety_nine"].value;
    var fileInput8 = document.getElementById('v_office_name_supplyfile8').value
    let fileInput_Result8 = allowedExtensions.test(fileInput8);


    if (number8 == "") {
        document.getElementById('doc8').innerHTML = "Please fill the required detail ";
        return false;
    } else {
        document.getElementById('doc8').innerHTML = "";
    }
    if (issue8 == false) {
        document.getElementById('issue8').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue8').innerHTML = "";
    }
    // if (expire8 == "") {
    //     document.getElementById('expire8').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire8').innerHTML = "";
    // }

    if (file8 == "") {
        document.getElementById('file8').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result8 == false) {
            document.getElementById('file8').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file8').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile8").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile8").value = "";
                return false;

            } else {
                document.getElementById('file8').innerHTML = "";
            }
        }
    }

    // if (file8 == "") {
    //     document.getElementById('file8').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file8').innerHTML = "";
    //     if (fileInput_Result8 == false) {
    //         document.getElementById('file8').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file8').innerHTML = "";
    //     }
    // }

    var number9 = document.forms["myForm"]["fourty_one"].value;
    var issue9 = document.forms["myForm"]["fourty_two"].value;
    // var expire9 = document.forms["myForm"]["fourty_three"].value;
    var file9 = document.forms["myForm"]["fourty_four"].value;
    var fileInput9 = document.getElementById('v_office_name_supplyfile9').value
    let fileInput_Result9 = allowedExtensions.test(fileInput9);


    if (number9 == "") {
        document.getElementById('doc9').innerHTML = "Please fill the required detail ";
        return false;
    } else {
        document.getElementById('doc9').innerHTML = "";
    }
    if (issue9 == false) {
        document.getElementById('issue9').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue9').innerHTML = "";
    }
    // if (expire9 == "") {
    //     document.getElementById('expire9').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire9').innerHTML = "";
    // }

    if (file9 == "") {
        document.getElementById('file9').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result9 == false) {
            document.getElementById('file9').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file9').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile9").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile9").value = "";
                return false;

            } else {
                document.getElementById('file9').innerHTML = "";
            }
        }
    }

    // if (file9 == "") {
    //     document.getElementById('file9').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file9').innerHTML = "";
    //     if (fileInput_Result9 == false) {
    //         document.getElementById('file9').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file9').innerHTML = "";
    //     }
    // }
    var number10 = document.forms["myForm"]["fourty_six"].value;
    var issue10 = document.forms["myForm"]["fourty_seven"].value;
    // var expire10 = document.forms["myForm"]["fourty_eight"].value;
    var file10 = document.forms["myForm"]["fourty_nine"].value;
    var fileInput10 = document.getElementById('v_office_name_supplyfile10').value
    let fileInput_Result10 = allowedExtensions.test(fileInput10);


    if (number10 == "") {
        document.getElementById('doc10').innerHTML = " Please fill the required detail  ";
        return false;
    } else {
        document.getElementById('doc10').innerHTML = "";
    }
    if (issue10 == false) {
        document.getElementById('issue10').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue10').innerHTML = "";
    }
    // if (expire10 == "") {
    //     document.getElementById('expire10').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire10').innerHTML = "";
    // }


    if (file10 == "") {
        document.getElementById('file10').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result10 == false) {
            document.getElementById('file10').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file10').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile10").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile10").value = "";
                return false;

            } else {
                document.getElementById('file10').innerHTML = "";
            }
        }
    }


    // if (file10 == "") {
    //     document.getElementById('file10').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file10').innerHTML = "";
    //     if (fileInput_Result10 == false) {
    //         document.getElementById('file10').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file10').innerHTML = "";
    //     }
    // }

    var number11 = document.forms["myForm"]["sixteen"].value;
    var issue11 = document.forms["myForm"]["seventeen"].value;
    // var expire11 = document.forms["myForm"]["eighteen"].value;
    var file11 = document.forms["myForm"]["nineteen"].value;
    var fileInput11 = document.getElementById('v_office_name_supplyfile4').value
    let fileInput_Result11 = allowedExtensions.test(fileInput11);
    let data_7 = document.forms["myForm"]["twenty_four"].value;

    let panNumbers = document.getElementById('Twenty_four_78').value;
    let panRGEXs = /^([a-zA-Z]){1}([0-9]){10,15}?$/;
    let panResults = panRGEXs.test(panNumbers);

    let V_eleven_upload_one_89 = document.forms["myForm"]["twenty_five_90"].value;
    var fileInput20 = document.getElementById('Twenty_five').value;
    let fileInput_Result20 = allowedExtensions.test(fileInput20);




    if (number11 == "") {
        document.getElementById('doc4').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('doc4').innerHTML = "";
    }

    if (issue11 == false) {
        document.getElementById('issue4').innerHTML = " Please fill the required detail ";
        return false;
    } else {
        document.getElementById('issue4').innerHTML = "";
    }
    // if (expire11 == false) {
    //     document.getElementById('expire4').innerHTML = " Please fill the required detail ";
    //     return false;
    // } else {
    //     document.getElementById('expire4').innerHTML = "";
    // }

    if (file11 == "") {
        document.getElementById('file4').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result11 == false) {
            document.getElementById('file4').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('file4').innerHTML = "";
            const oFile = document.getElementById("v_office_name_supplyfile4").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("v_office_name_supplyfile4").value = "";
                return false;

            } else {
                document.getElementById('file4').innerHTML = "";
            }
        }
    }
   

    // if (file11 == "") {
    //     document.getElementById('file4').innerHTML = " Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     //document.getElementById('file4').innerHTML = "";
    //     if (fileInput_Result11 == false) {
    //         document.getElementById('file4').innerHTML = " Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('file4').innerHTML = "";
    //     }
    // }


    if (data_7 == "") {
        console.log("hiiiiiiii789");
        document.getElementById('data14').innerHTML = "  Please fill the required detail  ";
        return false;
    } else {

        document.getElementById('data14').innerHTML = "";
        // if (panResults == false) {
        //     document.getElementById('data14').innerHTML = "  Please fill the valid Electricity Connection No.(A1234567898 format) ";
        //     return false;
        // } else {
        //     document.getElementById('data14').innerHTML = "";
        // }
    }


    if (V_eleven_upload_one_89 == "") {
        document.getElementById('data35').innerHTML = "Please the Upload file(In .pdf format)";
        return false;
    } else {
        //document.getElementById('Twenty_two').innerHTML = "";
        if (fileInput_Result20 == false) {
            document.getElementById('data35').innerHTML = "  Please Upload valid file format(In .pdf) ";
            return false;
        } else {
            // document.getElementById('data35').innerHTML = "";
            const oFile = document.getElementById("Twenty_five").files[0].size / 1024 / 1024;
            if (oFile > 2) {
                alert("File size must be less than or equal to 2 MB");
                document.getElementById("Twenty_five").value = "";
                return false;

            } else {
                document.getElementById('data35').innerHTML = "";
            }
        }
    }

    // if (V_eleven_upload_one_89 == "") {
    //     document.getElementById('data35').innerHTML = "Please upload the file in pdf format only";
    //     return false;
    // } else {
    //     // document.getElementById('data35').innerHTML = "";
    //     if (fileInput_Result20 == false) {
    //         document.getElementById('data35').innerHTML = "Valid file format required(In .pdf)";
    //         return false;
    //     } else {
    //         document.getElementById('data35').innerHTML = "";
    //     }
    // }





}

function validate(evt) {
    var theEvent = evt || window.event;

    // Handle paste
    if (theEvent.type === 'paste') {
        key = event.clipboardData.getData('text/plain');
    } else {
        // Handle key press
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key)
;
    }
    var regex = /[0-9]|\./;
    if (!regex.test(key)) {
        theEvent.returnValue = false;
        if (theEvent.preventDefault) theEvent.preventDefault();
    }
}