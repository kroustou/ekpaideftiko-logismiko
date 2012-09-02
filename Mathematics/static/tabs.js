function () {
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

}();