
var oTable;
$(document).ready(function () {
    oTable = $('#table_').DataTable({
        serverSide: true,
        "ajax": function (data, callback, settings) {
            api.post('/datatables', data).then(response => { callback(response.data); })
        },
        "paging": true,
        "lengthChange": false,
        "searching": false,
        "ordering": false,
        "info": false,
        "autoWidth": true,
        "responsive": true,
        columns: [
            { "data": "id", "title": "NO", },
            {
                "data": function (source, type, val) {
                    return moment.utc(source.session_start).tz('Asia/Jakarta').format("DD-MM-YYYY HH:mm");
                }
                , "title": "TIMESTAMP",
            },
            { "data": "device", "title": "DEVICE", },
            { "data": "sender", "title": "SENDER", },
            { "data": "target", "title": "TARGET", },
            { "data": "text", "title": "TEXT", },
            { "data": "status", "title": "STATUS", },
            { "data": "state", "title": "STATE", },

        ],
        // columnDefs: [
        //     {
        //         render: function (data, type, full, meta) {
        //             return "<div class='text-wrap width-200'>" + data + "</div>";
        //         },
        //         targets: 5
        //     }
        // ]
    });
});