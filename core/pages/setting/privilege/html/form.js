var form_ = $("#form_").validate({
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
    $("#form_ input[name='privilege']").focus();

    $('#jstree_').jstree({
        'core': {
            'data': {
                'url': function (node) {
                    return 'menu/' + $('#menutype_id').val() + '/{{privilege_id}}';
                }
            }
        }, "plugins": ["checkbox"]
    });

    $('#menutype_id').on('change', function () {
        $('#jstree_').jstree(true).destroy();

        $('#jstree_').jstree({
            'core': {
                'data': {
                    'url': function (node) {
                        return 'menu/' + $('#menutype_id').val() + '/{{privilege_id}}';
                    }
                }
            }, "plugins": ["checkbox"]
        });


    });

    $(".btnBack").on("click", function () {
        window.location.href = '{{prefix_url}}';
    });

    $("#form_").on("submit", function () {
        if (form_.valid()) {
            $("form input, form button").blur();
            $("#form_").LoadingOverlay("show");

            api.post('', {
                "privilege": $("#form_ input[name='privilege']").val(),
                "desc": $("#form_ input[name='desc']").val(),
                "menutype_id": $("#menutype_id").val(),
                "menus": $('#jstree_').jstree('get_selected'),
            })
                .then(function (response) {
                    idU = response.data.id;
                    Swal.fire("Tersimpan!", "", "success")
                        .then(() => {
                            window.location.href = '{{prefix_url_post}}/' + idU;
                        });
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
                    $("#form_").LoadingOverlay("hide");
                });
        }
        return false;
    });
});