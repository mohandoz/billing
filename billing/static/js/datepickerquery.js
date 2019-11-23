// $(function () {
    console.log("Ready!....")


    $('body').on('focus', "input.date.dateinput.form-control", function () {
        $(this).datepicker({format: 'yyyy-mm-dd'});
    });


// });

