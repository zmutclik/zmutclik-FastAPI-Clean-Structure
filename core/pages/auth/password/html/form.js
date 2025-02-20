var form_ = $("#form_").validate({ rules: { email: { required: !0 }, password: { required: !0 } }, errorElement: "div", errorPlacement: function (i, e) { i.addClass("invalid-feedback"), e.next().after(i) }, highlight: function (i, e, r) { $(i).addClass("is-invalid") }, unhighlight: function (i, e, r) { $(i).removeClass("is-invalid") } });

$(document).ready(function () {
    $('#code').focus();

    $("#password").keyup(function () {
        var m = $(this).val();
        var n = m.length;
        check(n, m);
    });

    $("#form_").on("submit", function () {
        if (form_.valid()) {
            if (percentage <= 70) {
                form_.showErrors({ "password": "Mohon kombinasi PASSWORD bernilai minimal 70%. !" });
            } else {
                $('#form_ input,#form_ button').blur();
                $("#form_").LoadingOverlay("show");
                var datapost = {};
                datapost["email"] = $('#form_ input[name=email]').val();
                datapost["code"] = $('#form_ input[name=code]').val();
                datapost["password"] = $('#form_ input[name=password]').val();
                datapost["password2"] = $('#form_ input[name=password2]').val();
                axios.post('{{prefix_url_post}}/{{salt}}', datapost, { withCredentials: true })
                    .then(function (response) {
                        Swal.fire({
                            icon: "success",
                            title: "Reset Password berhasil.!",
                            showConfirmButton: false,
                            timer: 2000
                        }).then(() => {
                            window.location.href = response.data['redirect_uri'];
                        });
                    })
                    .catch(function (error) {
                        switch (error.response.data.error_code) {
                            case 422:
                                de = {}
                                $.each(error.response.data.detail, function (i, v) {
                                    de[v.loc[1]] = v["message"];
                                });
                                form_.showErrors(de);
                                break;
                            default:
                                Swal.fire({
                                    position: "top-end",
                                    icon: "error",
                                    title: error.response.status + " : " + error.response.data.message,
                                });
                        }
                    })
                    .finally(() => {
                        $("#form_").LoadingOverlay("hide");
                    });
            }
        }
        return false;
    });
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