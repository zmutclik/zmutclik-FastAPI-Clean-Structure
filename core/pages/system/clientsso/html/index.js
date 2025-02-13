
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        "ajax": function (data, callback, settings) {
            api.post('/datatables', data).then(response => { callback(response.data); })
        },
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        columns: [
            { "data": "clientsso_id", "title": "ClientID", "width": "10%", },
            { "data": "nama", "title": "NAMA", },
            { "data": "ipaddress", "title": "IPADDRESS", },
            {
                "data": function (source, type, val) {
                    return source.created_user + "<br/> " + moment.utc(source.created_at).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm") + "";
                }
                , "title": "CREATED", "width": "15%",
            },
            { "data": "disabled", "title": "DISABLED", "width": "10%", },
            { "data": "clientsso_id", "title": "" },
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
        window.location.href = '{{prefix_url_post}}/form/add';
    });

    $("#table_").on("click", '.btnEdit', function () {
        window.location.href = '{{prefix_url_post}}/form/' + $(this).parents('tr').attr('id');
    });

    $("#table_").on("click", '.btnDelete', function () {
        var nm = $(this).parents('tr').find("td:nth-child(1)").html();
        var idU = $(this).parents('tr').attr('id');
        Swal.fire({
            title: 'Apakah anda YAKIN ingin menghapus Client SSO "' + nm + '"?',
            showCancelButton: true,
            confirmButtonText: "Ya HAPUS",
        }).then((result) => {
            if (result.isConfirmed) {
                api.delete(idU)
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