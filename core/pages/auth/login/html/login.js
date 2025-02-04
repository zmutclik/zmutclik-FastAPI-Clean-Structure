var formLogin = $("#formLogin").validate({
    rules: {
        email: { required: true },
        password: { required: true },
    },
    errorElement: 'div',
    errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.next().after(error);
    },
    highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
    },
});

$(document).ready(function () {
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
                        case 21002:
                            formLogin.showErrors({ "email": error.response.data.message });
                            $('#formLogin input[name=email]').focus();
                            break;
                        case 21003:
                            formLogin.showErrors({ "email": error.response.data.message });
                            $('#formLogin input[name=email]').focus();
                            break;
                        case 21000:
                            formLogin.showErrors({ "password": error.response.data.message });
                            $('#formLogin input[name=password]').focus();
                            break;
                        default:
                            Swal.fire({
                                position: "top-end",
                                icon: "error",
                                title: error.response.data.error_code + " : " + error.response.data.message,
                            }).then((result) => {
                                if (error.response.data.error_code in [10000, 10001, 10002])
                                    window.location.reload(true);
                                if (error.response.data.error_code == 422)
                                    window.location.href = "/auth/login/clear/client_id";
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