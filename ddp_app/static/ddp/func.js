$(document).ready(function() {
    $('.col-md-9 ul').addClass('hidden');
    $('li').click(function() {
        $(this).children('ul').toggleClass('hidden');
    });
});
