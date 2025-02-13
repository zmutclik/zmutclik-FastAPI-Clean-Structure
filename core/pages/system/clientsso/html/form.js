var form_ = $("#form_").validate({ rules: { scope: { required: !0 }, desc: { required: !0 } }, errorElement: "div", errorPlacement: function (e, i) { e.addClass("invalid-feedback"), i.after(e) }, highlight: function (e, i, r) { $(e).addClass("is-invalid") }, unhighlight: function (e, i, r) { $(e).removeClass("is-invalid") } });
$(document).ready(function () {
    $("#form_ input[name='scope']").focus();

    $(".btnBack").on("click", function () {
        window.location.href = '{{prefix_url}}';
    });

    $("#form_").on("submit", function () {
        if (form_.valid()) {
            $("form input, form button").blur();
            $("#form_").LoadingOverlay("show");

            api.post('', {
                "nama": $("#form_ input[name='nama']").val(),
                "ipaddress": $("#form_ input[name='ipaddress']").val(),
                "callback_uri": $("#form_ input[name='callback_uri']").val(),
                "disabled": $("#form_ select[name='disabled']").val(),
            })
                .then(function (response) {
                    idU = response.data.clientsso_id;
                    Swal.fire("Tersimpan!", "", "success")
                        .then(() => {
                            window.location.href = '{{prefix_url_post}}/form/' + idU;
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
                                title: error.response.data.error_code + " : " + error.response.data.message,
                            }).then((result) => {
                                if (error.response.data.error_code in [10000, 10001, 10002])
                                    window.location.reload(true);
                            });
                    }
                })
                .finally(() => {
                    $("#form_").LoadingOverlay("hide");
                });
        }
        return false;
    });

    $("#form_").on("click", '#btn-reset', function () {
        var idU = $("#clientsso_id").val();
        Swal.fire({
            title: 'Apakah anda YAKIN ingin Reset Secret Key Client SSO "' + idU + '"?',
            showCancelButton: true,
            confirmButtonText: "Ya HAPUS",
        }).then((result) => {
            if (result.isConfirmed) {
                api.post("/generate_clientsso_secret")
                    .then(function () {
                        Swal.fire("Ter Generate Ulang!", "", "success")
                            .then(() => {
                                window.location.reload(true);
                            });
                    })
            }
        });
    });
});