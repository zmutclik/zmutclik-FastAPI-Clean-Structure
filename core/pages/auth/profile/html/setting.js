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
            api.post('/setting', {
                "full_name": $("#form_setting input[name='full_name']").val(),
                "email": $("#form_setting input[name='email']").val(),
                "nohp": $("#form_setting input[name='nohp']").val(),
            })
                .then(function (response) {
                    Swal.fire("Tersimpan!", "", "success");
                })
                .catch(function (error) {
                    switch (error.response.data.error_code) {
                        case 422:
                            de = {}
                            $.each(error.response.data.detail, function (i, v) {
                                console.log(v);
                                de[v.loc[1]] = v["message"];
                            });
                            console.log(de);

                            form_.showErrors(de);
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