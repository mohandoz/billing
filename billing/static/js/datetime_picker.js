$(function () {
    console.log("Ready!....")


    $('body').on('focus', "input.date.dateinput.form-control", function () {
        $(this).datepicker({format: 'yyyy-mm-dd'});
    });

     //  $("#datetimepicker1").datetimepicker({
     //    format: 'DD/MM/YYYY HH:mm',
     //  });
     //
     // $('#datetimepicker1').datetimepicker();
})

