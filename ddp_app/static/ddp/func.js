$(document).ready(function() {
    $('.col-md-9 ul').addClass('hidden');
    $('li').click(function() {
        $(this).children('ul').toggleClass('hidden');
    });

    // radio buttons in tables
    $.each($('tr'), function(tr_idx, tr_val) {
        $.each($(tr_val).find('td:empty'), function(td_idx, td_val) {
            $(td_val).html('<input type="radio" name="group' + tr_idx + '">');
        });
    });
});
