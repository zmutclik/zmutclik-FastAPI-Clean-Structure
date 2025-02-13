var formLogin = $("#formLoggedin").validate({ errorElement: "div", errorPlacement: function (i, e) { i.addClass("invalid-feedback"), e.next().after(i) }, highlight: function (i, e, r) { $(i).addClass("is-invalid") }, unhighlight: function (i, e, r) { $(i).removeClass("is-invalid") } });

$(document).ready(function () {
    $("#list_users .list-group-item").on("click", function () {
        let idUser = $(this).attr('iduser');
        let idUser_ = $(this).attr('id');
        $("#card_login").LoadingOverlay("show");
        axios.post('{{prefix_url_post}}/check', { "email": idUser }, { withCredentials: true })
            .then(function (response) {
                $("#card_otp").show();
                $("#list_users .list-group-item").hide();
                $("#list_users #" + idUser_).show();
                $("#otp1").focus();
                $("#email").val(idUser);
            })
            .catch(function (error) {
                Swal.fire({
                    position: "top-end",
                    icon: "error",
                    title: error.response.status + " : " + error.response.data.message,
                });
            })
            .finally(() => {
                $("#card_login").LoadingOverlay("hide");
            });
    });


    $("#formLoggedin").on("submit", function () {
        let idUser = $(this).attr('iduser');
        let optcode = $("#otp1").val() + $("#otp2").val() + $("#otp3").val() + $("#otp4").val();

        if (isValidNumberString(optcode) == false) {
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: "Invalid OTP Code",
            });
        } else {
            $("#card_login").LoadingOverlay("show");
            axios.post('{{prefix_url_post}}/login', { "email": $("#email").val(), "code": optcode }, { withCredentials: true })
                .then(function (response) {
                    window.location.href = "{{redirect_uri}}";
                })
                .catch(function (error) {
                    switch (error.response.data.error_code) {
                        case 422:
                            $.each(error.response.data.detail, function (i, v) {
                                $("#otp-error").html(v["message"]);

                            });
                            $("#otp-error").show();
                            break;
                        case 404:
                            Swal.fire({
                                position: "top-end",
                                icon: "error",
                                title: error.response.status + " : " + error.response.data.message,
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
                    $("#card_login").LoadingOverlay("hide");
                });
        }
        return false;
    });
});

function moveToNext(current, nextFieldID) {
    if (current.value.length >= 1) {
        if (nextFieldID) {
            document.getElementById(nextFieldID).focus();
            document.getElementById(nextFieldID).select();
        }
    }
}

function isValidNumberString(str) {
    return /^[0-9]{4}$/.test(str);
}