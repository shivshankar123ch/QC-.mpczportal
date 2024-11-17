window.onload=initAll;
var specification;
function initAll(){
specification = document.getElementById('product');
specification.change = specification_list;
}
 function specification_list(){
 alert()
 }

$('#product').change(function () {
    var selection = this.value;
    alert(selection)
    $.getJSON('platypus.json', selection, data() {
    . . .
    });
});

$('#product').change(function(){
                console.log('countrychange');
                getState();
            })