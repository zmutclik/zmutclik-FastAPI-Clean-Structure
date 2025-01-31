var form_setting = $("#form_setting").validate({
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
$(document).ready(function () {
    $("#form_setting").on("submit", function () {

        if (form_setting.valid()) {
            $("form input, form button").blur();
            $("#form_setting").LoadingOverlay("show");

            api.post('', {
                "app_name": $("#form_setting input[name='app_name']").val(),
                "app_desc": $("#form_setting input[name='app_desc']").val(),
                "app_host": $("#form_setting input[name='app_host']").val(),
                "app_port": $("#form_setting input[name='app_port']").val(),
                "prefix_session": $("#form_setting input[name='prefix_session']").val(),
                "jwt_scret_key": $("#form_setting input[name='jwt_scret_key']").val(),
                "jwt_algorithm": $("#form_setting select[name='jwt_algorithm']").val(),
                "cookies_exp": $("#form_setting input[name='cookies_exp']").val(),
                "refresh_exp": $("#form_setting input[name='refresh_exp']").val(),
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
});