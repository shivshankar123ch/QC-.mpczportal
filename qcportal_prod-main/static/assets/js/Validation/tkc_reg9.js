$(document).ready(function(){  
    $("select").change(function() {   
      $("select").not(this).find("option[value="+ $(this).val() + "]").attr('disabled', true);
    }); 
  }); 


 
 function  incomeValidation(inp_id){
    let get_income = document.getElementById(inp_id);
    
    if(get_income.value == ""){
    let x = document.getElementById(inp_id+"_span");

    x.innerHTML = "Please fill the income";
    }else{
    let x = document.getElementById(inp_id+"_span");
    x.innerHTML = "";
    }
    

}
function  taxValidation(inp_id){
    let get_income = document.getElementById(inp_id);
    
    if(get_income.value == ""){
    let x = document.getElementById(inp_id+"_span");

    x.innerHTML = "Please fill the tax";
    }else{
    let x = document.getElementById(inp_id+"_span");
    x.innerHTML = "";
    }
    

}
function isNumberKey(evt)
{
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    return true;
}
   

function validateForm(){
    valid = true;
    
        if ( document.myForm.year12.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_income.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_tex.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.year13.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_income1.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_tex1.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.year14.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_income2.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }
        if ( document.myForm.input_tex2.value == "" )
        {
            alert ( "Please fill in the required detail" );
            valid = false;
        }

        if(!confirm("Are you sure you want to submit?")) {
                valid= false;
                }
    
        return valid;

}
