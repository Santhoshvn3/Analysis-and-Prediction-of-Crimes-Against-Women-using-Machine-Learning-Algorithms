$("form[name=signup_form]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/admin/signup",
        type:"POST",
        data: data,
        dataType: "json",
        success:function (response) {
            if (response.d == true) {
                 alert("You will now be redirected.");
                 window.location.href = "/dashboard/";
             }
         },
        error: function(resp) {
            console.log(resp)
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
})

$("form[name=login_form]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/admin/login",
        type:"POST",
        data: data,
        dataType: "json",
        success:function (response) {
            if (response.d == true) {
                 alert("You will now be redirected.");
                 window.location.href = "/dashboard/";
             }
         },
        error: function(resp) {
            console.log(resp)
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
})