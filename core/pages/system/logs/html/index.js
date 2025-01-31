
var oTable;
$(document).ready(function () {
    $('#time_end').val(moment().subtract(-10, 'minutes').format("DD MMM YYYY HH:mm"));
    $('#time_start').val(moment().subtract(6, 'hours').format("DD MMM YYYY HH:mm"));

    oTable = $('#table_').DataTable({
        serverSide: true,
        "ajax": function (data, callback, settings) {
            data.search.bulantahun = moment($('#time_start').val(), "DD MMM YYYY HH:mm").format("YYYY-MM-DD HH:mm:ss");
            data.search.time_start = moment($('#time_start').val(), "DD MMM YYYY HH:mm").unix();
            data.search.time_end = moment($('#time_end').val(), "DD MMM YYYY HH:mm").unix();
            data.search.ipaddress = $('#ipaddress').val();
            data.search.routername = $('#routername').val();
            data.search.clientid = $('#clientid').val();
            data.search.username = $('#username').val();
            data.search.channel = $('#channel').val();
            data.search.method = $('#method').val();
            data.search.status = $('#status').val();
            data.search.path = $('#querypath').val();
            data.search.referer = $('#queryreferer').val();
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
                    return moment.unix(source.startTime).format("YYYY-MM-DD HH:mm:ss");
                }
                , "title": "WAKTU",
            },
            {
                "data": function (source, type, val) {
                    return "<div class=\"row\"><div class=\"col\">" + source.platform + "</div></div><div class=\"row\"><div class=\"col\">" + source.browser + "</div></div>";
                }, "title": "PLATFORM",
            },
            {
                "data": function (source, type, val) {
                    return "<div class=\"row\"><div class=\"col\">ref : " + source.referer + "</div></div><div class=\"row\"><div class=\"col\">for : " + source.path + "</div></div>";
                }, "title": "PATH",
            },
            {
                "data": function (source, type, val) {
                    return "<div class=\"row\"><div class=\"col\">" + source.method + "</div></div><div class=\"row\"><div class=\"col\">" + source.ipaddress + "</div></div>";
                }, "title": "IP",
            },
            { "data": "user", "title": "USERS", },
            {
                "data": function (source, type, val) {
                    if (/\b50[0-9]\b/.test(source.status_code)) {
                        return '<a href="#" class="show_ErrorModal" data-bs-toggle="modal" data-bs-target="#ErrorModal" attid="' + source.id + '"><b>' + source.status_code + '</b></a>';
                    } else
                        return source.status_code;
                }, "title": "CODE",
            },
            {
                "data": function (source, type, val) {
                    return source.process_time.toFixed(3);
                }, "title": "TIME",
            },
        ],
        columnDefs: [
            {
                render: function (data, type, full, meta) {
                    return "<div class='text-wrap width-200'>" + data + "</div>";
                },
                targets: 5
            }
        ]
    });

    $("#table_").on("click", '.show_ErrorModal', function () {
        $("#ErrorModal").LoadingOverlay("show");
        api.get('/error/' + $(this).parents('tr').attr('id'))
            .then(function (response) {
                $("#error_type").val(response.data["error_type"])
                $("#error_message").val(response.data["error_message"])
                $("#error_traceback").val(response.data["error_traceback"])
            })
            .catch(function (error) {
            })
            .finally(function () {
                $("#ErrorModal").LoadingOverlay("hide");
            });
    });
    $("#time_start,#time_end").flatpickr({
        enableTime: true,
        dateFormat: "d M Y H:i",
        time_24hr: true, onChange: function (selectedDates, dateStr, instance) {
            oTable.ajax.reload();
        }
    });

    $("#method,#status,#routername,#clientid,#username,#channel").on("change", function (e) {
        oTable.ajax.reload();
    });

    var timer, delay = 500;
    $('#ipaddress,#querypath,#queryreferer').bind('keydown blur change', function (e) {
        var _this = $(this);
        clearTimeout(timer);
        timer = setTimeout(function () {
            oTable.ajax.reload();
        }, delay);
    });


    $('.card-header').on('click', '.btnreload', function () {
        oTable.ajax.reload();
    });

    $('.card-body').on('click', '.btntimenow', function () {
        $('#time_end').val(moment().subtract(-10, 'minutes').format("DD MMM YYYY HH:mm"));
        $('#time_start').val(moment().subtract(6, 'hours').format("DD MMM YYYY HH:mm"));
        setTimeout(function () {
            oTable.ajax.reload();
        }, 200);
    });
});