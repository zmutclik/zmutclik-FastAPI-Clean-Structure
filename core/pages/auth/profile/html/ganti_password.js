var percentage = 0;
var form_gantipassword = $("#form_gantipassword").validate({
    errorElement: 'div',
    errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.after(error);
    },
    highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
    },
});
function check(n, m) {
    if (n < 6) {
        percentage = 0;
        $(".progress-bar").css("background", "#dd4b39");
    } else if (n < 8) {
        percentage = 20;
        $(".progress-bar").css("background", "#9c27b0");
    } else if (n < 10) {
        percentage = 40;
        $(".progress-bar").css("background", "#ff9800");
    } else {
        percentage = 60;
        $(".progress-bar").css("background", "#4caf50");
    }
    if ((m.match(/[a-z]/) != null)) {
        percentage += 10;
    }
    if ((m.match(/[A-Z]/) != null)) {
        percentage += 10;
    }
    if ((m.match(/0|1|2|3|4|5|6|7|8|9/) != null)) {
        percentage += 10;
    }
    if ((m.match(/\W/) != null) && (m.match(/\D/) != null)) {
        percentage += 10;
    }
    $(".progress-bar").css("width", percentage + "%");
    $(".progress-bar").html(percentage + "%");
}
$(document).ready(function () {
    $("#password_baru1").keyup(function () {
        var m = $(this).val();
        var n = m.length;
        check(n, m);
    });


    $("#form_gantipassword").on("submit", function () {
        if (form_gantipassword.valid()) {
            if (percentage <= 70) {
                form_gantipassword.showErrors({ "password_baru1": "Mohon kombinasi PASSWORD bernilai minimal 70%. !" });
            } else if ($("#form_gantipassword input[name='password_lama']").val() == $("#form_gantipassword input[name='password_baru1']").val()) {
                form_gantipassword.showErrors({ "password_baru1": "Password tidak boleh sama dengan yg lama." });
            } else {
                $("form input, form button").blur();
                $("#form_gantipassword").LoadingOverlay("show");
                api.post('/gantipassword', {
                    "password_lama": $("#form_gantipassword input[name='password_lama']").val(),
                    "password_baru1": $("#form_gantipassword input[name='password_baru1']").val(),
                    "password_baru2": $("#form_gantipassword input[name='password_baru2']").val(),
                })
                    .then(function (response) {
                        Swal.fire("Tersimpan!", "", "success");
                    })
                    .catch(function (error) {
                        switch (error.response.data.error_code) {
                            case 422:
                                de = {}
                                $.each(error.response.data.detail, function (i, v) {
                                    de[v.loc[1]] = v["message"];
                                });
                                form_gantipassword.showErrors(de);
                                break;
                            default:
                                Swal.fire({
                                    position: "top-end",
                                    icon: "error",
                                    title: error.response.data.error_code + " : " + error.response.data.message,
                                }).then((result) => {
                                    if (error.response.data.error_code in [10000, 10001, 10002])
                                        window.location.reload(true);
                                });
                        }
                    })
                    .finally(() => {
                        $("#form_gantipassword").LoadingOverlay("hide");
                    });
            }
        }
        return false;
    });
});