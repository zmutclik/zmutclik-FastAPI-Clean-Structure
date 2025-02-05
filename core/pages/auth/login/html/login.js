var formLogin = $("#formLogin").validate({ rules: { email: { required: !0 }, password: { required: !0 } }, errorElement: "div", errorPlacement: function (i, e) { i.addClass("invalid-feedback"), e.next().after(i) }, highlight: function (i, e, r) { $(i).addClass("is-invalid") }, unhighlight: function (i, e, r) { $(i).removeClass("is-invalid") } });

$(document).ready(function () {
    $('#formLogin input[name=email]').focus();
    $("#formLogin").on("submit", function () {
        if (formLogin.valid()) {
            $('#formLogin input,#formLogin button').blur();
            $("#formLogin").LoadingOverlay("show");
            axios.post('{{prefix_url_post}}', { "email": $('#formLogin input[name=email]').val(), "password": $('#formLogin input[name=password]').val() }, { withCredentials: true })
                .then(function (response) {
                    Swal.fire({
                        icon: "success",
                        title: "Akun sukses Login.!",
                        showConfirmButton: false,
                        timer: 2000
                    }).then(() => {
                        window.location.href = "{{nextpage}}";
                    });
                })
                .catch(function (error) {
                    switch (error.response.data.error_code) {
                        case 422:
                            de = {}
                            $.each(error.response.data.detail, function (i, v) {
                                de[v.loc[1]] = v["message"];
                            });
                            formLogin.showErrors(de);
                            break;
                        case 404:
                            Swal.fire({
                                position: "top-end",
                                icon: "error",
                                title: error.response.status + " : " + error.response.data.message,
                            }).then((result) => {
                                window.location.href = "/auth/login/clear/client_id";
                            });
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
                    $("#formLogin").LoadingOverlay("hide");
                });
        }
        return false;
    });

});