var vents= {
    items: {
        'cli': '',
        'pay_method': '',
        'date_joined': '',
        'subtotal': 0.00,
        'iva': 0.00,
        'money': '',
        'total': 0.00,
        'replacements': []
    },

    /*add: function(item) {
        //this.items.replacements.push(item);
        //this.list()
    },*/

    list: function() {
        tblReplacements = $('#tblReplacements').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,


            data: this.items.replacements,


            columns: [
                { "data": "id" },
                { "data": "name" },
                { "data": "code_replacement" },
                { "data": "pvp" },
                { "data": "stock" },
                { "data": "subtotal" }
            ],

            columns: [
                { "data": "id" },
                { "data": "name" },
                { "data": "code_replacement" },
                { "data": "pvp" },
                { "data": "stock" },
                { "data": "subtotal" }
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    }
                },

                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);

                    }
                },

                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text", name="stock" class="form-control form-control-md" autocomplete="off" value="' + row.stock + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);

                    }
                }
            ],

            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="stock"]').TouchSpin({
                    min: 1,
                    max: 100000,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        })
    },

    add: function() {

    }
}


$(function() {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        maxDate: moment().format("YYYY-MM-DD"),
        minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='iva']").TouchSpin({
        min: 0.19,
        max: 0.19,
        step: 0.19,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function () {
        vents.calculate_invoice();
    }).
        val(0.19);

        //search replacements
        $('input[name="search"]').autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_replacements',
                        'term': request.term
                    },
                    dataType: 'json',
                }).done(function (data) {
                    response(data);
                }).fail(function (jqXHR, textStatus, errorThrown) {
                    //alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {
    
                });
            },
            delay: 500,
            minLength: 1,
            select: function (event, ui) {
                event.preventDefault();
                console.log(ui.item);
                vents.items.replacements.push(ui.item);
                console.log(vents.items)
                ui.item.stock = 1;
                ui.item.subtotal = 0.00;


                vents.list();
                //ui.item.stock = 1;
                //ui.item.subtotal = 0.00;
                //vents.items.replacements.push(ui.item);
                //vents.add(ui.item);
                //vents.list();
                //console.log(vents.items);
                $(this).val('');
    
            }
        });
})