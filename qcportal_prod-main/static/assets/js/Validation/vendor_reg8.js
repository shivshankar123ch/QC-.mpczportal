
//form validation
    function FormError(inp_id){
        let inp = document.getElementById(inp_id);
        if(inp.value == ""){
        let x = document.getElementById(inp_id+"_span");

        x.innerHTML = "Please fill the required details";
        }else{
        let x = document.getElementById(inp_id+"_span");
        x.innerHTML = "";
        }
    }

function validateForm() {
    let Work_experience = document.getElementById("work_experience").value;
    let Turn_over = document.getElementById("turn_over").value;
    if (Work_experience == "") {
        document.getElementById('work_experience_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('work_experience_span').innerHTML = "";
    }
    if (Turn_over == "") {
        document.getElementById('turn_over_span').innerHTML = "Please fill the required details";
        return false;
    } else {
        document.getElementById('turn_over_span').innerHTML = "";
    }
    
}
