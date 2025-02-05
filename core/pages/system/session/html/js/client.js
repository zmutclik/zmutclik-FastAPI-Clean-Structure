
var oTable_client;
$(document).ready(function () {
    oTable_client = $('#table_client').DataTable({
        serverSide: true,
        "ajax": function (data, callback, settings) {
            api.post('/datatables/client', data).then(response => { callback(response.data); })
        },
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": true,
        "responsive": true,
        columns: [
            { "data": "client_id", "title": "CLIENT", },
            { "data": "platform", "title": "PLATFORM", },
            { "data": "browser", "title": "BROWSER", },
            { "data": "users", "title": "USERS", },
            {
                "data": function (source, type, val) {
                    if (source.LastLogin == null)
                        return "-";
                    return moment.utc(source.LastLogin).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm");
                }, "title": "LASTACTIVITY",
            },
            { "data": "disabled", "title": "DISABLED", },
            {
                "data": "id", "title": "-", "orderable": false, "searchable": false,
            },
        ],
        columnDefs: [{
            sClass: "right", searchable: false, orderable: false, bSortable: false, targets: -1, sWidth: "0px",
            render: function (data, type, row, meta) {
                btndis = ""

                btnhtml = "<div class=\"btn-group\" role=\"group\">";
                if (row.disabled)
                    btnhtml += "<button type=\"button\" class=\"btn btn-secondary btnDelete\"><i class=\"fas fas fa-skull\"></i></button>";
                else
                    btnhtml += "<button type=\"button\" class=\"btn btn-danger btnDelete\"><i class=\"fas fas fa-skull\"></i></button>";
                btnhtml += "</div>"
                return btnhtml;
            }
        }],

    });


    $("#table_client").on("click", '.btnDelete', function () {
        var nm = $(this).parents('tr').find("td:nth-child(1)").html();
        var disablet = $(this).parents('tr').find("td:nth-child(6)").html();
        if (disablet == "true")
            disablet = "ENABLE";
        else
            disablet = "DISABLE";
        Swal.fire({
            title: 'Apakah anda YAKIN ingin ' + disablet + ' CLIENT punya "' + nm + '" ?',
            showCancelButton: true,
            confirmButtonText: "Ya KILL",
        }).then((result) => {
            if (result.isConfirmed) {
                api.delete("client/" + nm)
                    .then(function () {
                        Swal.fire("Terhapus!", "", "success")
                            .then(() => {
                                oTable_client.ajax.reload();
                            });
                    })
            }
        });
    });
});