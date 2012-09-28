jQuery(function ($) {

    var minutes = parseInt($('.timer .min').html(), 10);
    var seconds = parseInt($('.timer .sec').html(), 10);
    var form = $('.exam');

    setInterval(function() {

        if (seconds != 0 ){
            seconds -= 1;
        }else {
            seconds = 59;
            minutes -= 1;            
        }

        // change style if timer is on its last minute
        if ( minutes == 0 ) {
            $('.timer').css('font-weight', '800');
            $('.timer').css('color', 'red');
        }

        // always have double digits in secs
        if (seconds < 10 ){
            seconds_html = '0' + seconds;
        } else {
            seconds_html = seconds; 
        }
        //if time has passed submit the form
        if (( minutes == 0 ) && ( seconds == 0 )){
            form.submit();
        }

        $('.timer .sec').html(seconds_html);
        $('.timer .min').html(minutes);
    },1000);
});
