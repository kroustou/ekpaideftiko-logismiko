jQuery(function ($) {
    "use strict";

   // tabs
    var tabs = $('.tabs > li');
    var panes = $('.panes > li');

    tabs.on('click', function () {
        var index = tabs.index(this);

        tabs.removeClass('active')
            .eq(index).addClass('active');

        panes.removeClass('active')
            .eq(index).addClass('active');

    }); 

     $('.show-sos').on('click', function() {
        $('.sos').css('background', 'tomato');
        $(this).slideUp();
    });
    
    $(document).ready(function() {
        $('.panes').prepend('<div class="print"><a href="#print"><img width="16" height="16" src="/static/images/print.png">Εκτύπωση.</a></div>');
        $('.panes .print a').click(function() {
            window.print();
            return false;
        });
    }); 
});