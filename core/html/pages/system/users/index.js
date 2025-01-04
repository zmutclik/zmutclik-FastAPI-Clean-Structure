
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        ajax: {
            "url": '{{prefix_url}}/{{clientId}}/{{sessionId}}/datatables', "contentType": "application/json", "type": "POST",
            "data": function (d) {
                return JSON.stringify(d);
            }, 'beforeSend': function (request) { request.setRequestHeader("Authorization", api.defaults.headers['Authorization']); }
        },
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        columns: [
            { "data": "username", "title": "USERNAME", },
            { "data": "email", "title": "EMAIL", },
            { "data": "full_name", "title": "NAMA", },
            {
                "data": function (source, type, val) {
                    if (source.disabled)
                        return "Tidak aktif";
                    else
                        return "aktif";
                }, "title": "STATUS",
            },

            { "data": "id", "title": "" },
        ],
        columnDefs: [{
            sClass: "right", searchable: false, orderable: false, bSortable: false, targets: -1, sWidth: "0px",
            render: function (data, type, row, meta) {
                btnhtml = "<div class=\"btn-group\" role=\"group\">";
                btnhtml += "<button type=\"button\" class=\"btn btn-success btnEdit\"><i class=\"fas fa-pencil-alt\"></i></button>";
                btnhtml += "<button type=\"button\" class=\"btn btn-danger btnDelete\"><i class=\"fas fa-trash-alt\"></i></button>";
                btnhtml += "</div>"
                return btnhtml;
            }
        }],
    });

    $("#btnTambah").on("click", function () {
        window.location.href = '{{prefix_url}}/{{clientId}}/{{sessionId}}/add';
    });

    $("#table_").on("click", '.btnEdit', function () {
        window.location.href = '{{prefix_url}}/{{clientId}}/{{sessionId}}/' + $(this).parents('tr').attr('id');
    });

    $("#table_").on("click", '.btnDelete', function () {
        var fullname = $(this).parents('tr').find("td:nth-child(3)").html();
        var idUser = $(this).parents('tr').attr('id');
        Swal.fire({
            title: 'Apakah anda YAKIN ingin menghapus User ini "' + fullname + '"?',
            showCancelButton: true,
            confirmButtonText: "Ya HAPUS",
        }).then((result) => {
            if (result.isConfirmed) {
                api.delete(idUser)
                    .then(function () {
                        Swal.fire("Terhapus!", "", "success")
                            .then(() => {
                                oTable.ajax.reload();
                            });
                    })
            }
        });
    });
});