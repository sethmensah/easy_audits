$(document).ready(function () {

    //Prevent right-click on entire window
    $(window).on("contextmenu", function () {
        return false;
    });
    //Prevent browser back and forward buttons.
    if (window.history && window.history.pushState) {
        window.history.pushState('forward', '', window.location.href);
        $(window).on('popstate', function (e) {
            window.history.pushState('forward', '', window.location.href);
            e.preventDefault();
        });
    }

    $('#id_review_date').daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }

    });
    $('#id_period_covered').daterangepicker({
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });

    $("#id_banklodgment-0-lodgment_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });

    $("#id_fundsutilized-0-expense_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });

    $("#id_commodityreceived-0-commodity_receipt_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });


    $("#id_commodityutilized-0-commodity_issued_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });

    $("#id_unpresentedpaymentvouchers-0-payment_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });

    $("#id_fundsreceived-0-receipt_date").daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        drops: 'down',
        locale: {
            cancelLabel: 'Clear'
        }
    });
    //for maintaing and using single dates
    $('#id_period_covered').on('apply.daterangepicker', function (ev, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
    });

    $('#id_review_date').on('apply.daterangepicker', function (env, review_picker) {
        $(this).val(review_picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_fundsreceived-0-receipt_date').on('apply.daterangepicker', function (env, funds_rec_picker) {
        $(this).val(funds_rec_picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_unpresentedpaymentvouchers-0-payment_date').on('apply.daterangepicker', function (env, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_commodityutilized-0-commodity_issued_date').on('apply.daterangepicker', function (env, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_commodityreceived-0-commodity_receipt_date').on('apply.daterangepicker', function (env, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_fundsutilized-0-expense_date').on('apply.daterangepicker', function (env, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY'));
    });

    $('#id_banklodgment-0-lodgment_date').on('apply.daterangepicker', function (env, picker) {
        $(this).val(picker.startDate.format('MM/DD/YYYY'));
    });
})
