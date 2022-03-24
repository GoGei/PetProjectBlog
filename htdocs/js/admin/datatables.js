$('.datatable-form').on('change', function () {
    $(this).submit();
});


// $('.filter-form-button').on('click', function (e) {
//     console.log('there');
//     let $filterForm = $('.filter-form');
//     // e.preventDefault();
//     $.ajax({
//         method: $filterForm.attr('method'),
//         url: $filterForm.attr('action'),
//         data: $filterForm.serialize(),
//         success: function (response) {
//             console.log('ok');
//             closeModal();
//         },
//         error: function () {
//             console.log('error');
//             // closeModal();
//         }
//     });
//
//     function closeModal(){
//         $('#filterForm').modal('hide');
//     }
//
//     return false;
// });