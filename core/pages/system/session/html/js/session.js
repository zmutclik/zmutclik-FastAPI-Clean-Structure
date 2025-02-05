
var oTable_session;
$(document).ready(function () {
    oTable_session = $('#table_session').DataTable({
        serverSide: true,
        "ajax": function (data, callback, settings) {
            api.post('/datatables/session', data).then(response => { callback(response.data); })
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
            { "data": "session_id", "title": "SESSION", },
            { "data": "user", "title": "USER", },
            {
                "data": function (source, type, val) {
                    return "start: " + moment.utc(source.session_start).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm") + "<br/>"
                        + " end : " + moment.utc(source.session_end).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm");
                }, "title": "WAKTU",
            },
            {
                "data": function (source, type, val) {
                    if (source.session_update == null)
                        return "-";
                    return moment.utc(source.session_update).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm");
                }, "title": "REFRESH",
            },
            {
                "data": "Lastipaddress", "title": "IPADDRESS",
            },
            {
                "data": "LastPage", "title": "LASTPAGE",
            },
            {
                "data": "id", "title": "-", "orderable": false, "searchable": false,
            },
        ],
        columnDefs: [{
            sClass: "right", searchable: false, orderable: false, bSortable: false, targets: -1, sWidth: "0px",
            render: function (data, type, row, meta) {
                btndis = ""
                if (!row.active_status) btndis = " disabled"

                btnhtml = "<div class=\"btn-group\" role=\"group\">";
                if (!row.active_status)
                    btnhtml += "<button type=\"button\" class=\"btn btn-secondary btnDelete\" " + btndis + "><i class=\"fas fas fa-skull\"></i></button>";
                else
                    btnhtml += "<button type=\"button\" class=\"btn btn-danger btnDelete\" " + btndis + "><i class=\"fas fas fa-skull\"></i></button>";
                btnhtml += "</div>"
                return btnhtml;
            }
        }],
    });


    $("#table_session").on("click", '.btnDelete', function () {
        var nm = $(this).parents('tr').find("td:nth-child(2)").html();
        var idU = $(this).parents('tr').attr('id');
        Swal.fire({
            title: 'Apakah anda YAKIN ingin Membunuh Session punya "' + nm + '" ?',
            showCancelButton: true,
            confirmButtonText: "Ya KILL",
        }).then((result) => {
            if (result.isConfirmed) {
                api.delete("session/" + idU)
                    .then(function () {
                        Swal.fire("Terhapus!", "", "success")
                            .then(() => {
                                oTable_session.ajax.reload();
                            });
                    })
            }
        });
    });
});