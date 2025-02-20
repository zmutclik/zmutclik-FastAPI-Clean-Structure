var form_setting = $("#form_setting").validate({ errorElement: "div", errorPlacement: function (i, n) { i.addClass("invalid-feedback"), n.after(i) }, highlight: function (i, n, a) { $(i).addClass("is-invalid") }, unhighlight: function (i, n, a) { $(i).removeClass("is-invalid") } });
var form_auth = $("#form_auth").validate({ errorElement: "div", errorPlacement: function (i, a) { i.addClass("invalid-feedback"), a.after(i) }, highlight: function (i, a, e) { $(i).addClass("is-invalid") }, unhighlight: function (i, a, e) { $(i).removeClass("is-invalid") } });

$(document).ready(function () {
    $("#form_setting").on("submit", function () {
        if (form_setting.valid()) {
            $("form input, form button").blur();
            $("#form_setting").LoadingOverlay("show");

            api.post('core', {
                "app_name": $("#form_setting input[name='app_name']").val(),
                "app_desc": $("#form_setting input[name='app_desc']").val(),
                "app_host": $("#form_setting input[name='app_host']").val(),
                "app_port": $("#form_setting input[name='app_port']").val(),
                "host_url": $("#form_setting input[name='host_url']").val(),
                "environment": $("#form_setting select[name='environment']").val(),
                "debug": $("#form_setting select[name='debug']").val(),
            })
                .then(function (response) {
                    Swal.fire("Tersimpan!", "", "success")
                        .then((result) => {
                            Swal.fire({
                                text: "Mohon Restart System untuk mendapatkan Pengaruh Perubahan.",
                                icon: "error"
                            });
                        });
                })
                .catch(function (error) {
                    switch (error.response.data.error_code) {
                        case 422:
                            de = {}
                            $.each(error.response.data.detail, function (i, v) {
                                de[v.loc[1]] = v["message"];
                            });
                            form_setting.showErrors(de);
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
                    $("#form_setting").LoadingOverlay("hide");
                });
        }
        return false;
    });

    $("#form_auth").on("submit", function () {
        if (form_auth.valid()) {
            $("form input, form button").blur();
            $("#form_auth").LoadingOverlay("show");

            api.post('auth', {
                "sso_login_url": $("#form_auth input[name='sso_login_url']").val(),
                "sso_token_url": $("#form_auth input[name='sso_token_url']").val(),
                "sso_client_id": $("#form_auth input[name='sso_client_id']").val(),
                "jwt_scret_key": $("#form_auth input[name='jwt_scret_key']").val(),
                "jwt_algorithm": $("#form_auth select[name='jwt_algorithm']").val(),
                "cookies_prefix": $("#form_auth input[name='cookies_prefix']").val(),
                "cookies_https": $("#form_auth select[name='cookies_https']").val(),
                "cookies_exp": $("#form_auth input[name='cookies_exp']").val(),
                "refresh_exp": $("#form_auth input[name='refresh_exp']").val(),
                "timeout_exp": $("#form_auth input[name='timeout_exp']").val(),
                "register_account": $("#form_auth select[name='register_account']").val(),
                "login_by_otp": $("#form_auth select[name='login_by_otp']").val(),
            })
                .then(function (response) {
                    Swal.fire("Tersimpan!", "", "success")
                        .then((result) => {
                            Swal.fire({
                                text: "Mohon Restart System untuk mendapatkan Pengaruh Perubahan.",
                                icon: "error"
                            });
                        });
                })
                .catch(function (error) {
                    switch (error.response.data.error_code) {
                        case 422:
                            de = {}
                            $.each(error.response.data.detail, function (i, v) {
                                de[v.loc[1]] = v["message"];
                            });
                            form_auth.showErrors(de);
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
                    $("#form_auth").LoadingOverlay("hide");
                });
        }
        return false;
    });
});