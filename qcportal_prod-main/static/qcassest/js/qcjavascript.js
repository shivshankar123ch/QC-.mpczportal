$(document).ready(function () {
  $("#qcToggelMenu").click(function () {
    $("#qcsidenavMain").toggleClass("qc-collapsesidenav-block");
    $("#qccontantBlock").toggleClass("qc-contantcollpase-block");
    $("#qcheaderMenu").toggleClass("qc-collapseheader-block");
  });
});

$(document).ready(function () {
  $("#toggelMMenu").click(function () {
    $(".qc-sidenav-block").toggleClass("qc-mcollapsesidenav-block");
  });
});

$(document).ready(function () {
  $("#qcClosemenu").click(function () {
    $(".qc-sidenav-block").toggleClass("qc-mcollapsesidenav-block");
  });
});




$("#ed-menulist .nav-item").on("click", function () {
  // var target = $(this).attr('data-rel');
  $("#ed-menulist .nav-item .nav-link").removeClass("active");
  $("#ed-menulist .nav-item .ed-menudropdown-block").css("display", "none");
  $("#ed-menulist .nav-item").removeClass("active");
  $(this).addClass("active");
  // $('#ed-menulist .nav-item').addClass('active');
  $("#ed-menulist .nav-item.active .ed-menudropdown-block").css(
    "display",
    "block"
  );
  // alert();
  // $("#" + target).fadeIn('slow').siblings(".tab-box").hide();
  return false;
});
