var form_ = $("#form_").validate({ rules: { email: { required: !0 }, password: { required: !0 } }, errorElement: "div", errorPlacement: function (i, e) { i.addClass("invalid-feedback"), e.next().after(i) }, highlight: function (i, e, r) { $(i).addClass("is-invalid") }, unhighlight: function (i, e, r) { $(i).removeClass("is-invalid") } });

$(document).ready(function () {
    $('#form_ input[name=email]').focus();
    $("#form_").on("submit", function () {
        if (form_.valid()) {
            $('#form_ input,#form_ button').blur();
            $("#form_").LoadingOverlay("show");
            var datapost = {};
            datapost["email"] = $('#form_ input[name=email]').val();
            datapost["client_id"] = "{{client_id}}";
            axios.post('{{prefix_url_post}}', datapost, { withCredentials: true })
                .then(function (response) {
                    Swal.fire({
                        icon: "success",
                        title: "Permintaan reset Password sudah diterima.!",
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
        return false;
    });

});