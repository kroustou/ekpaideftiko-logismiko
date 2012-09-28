jQuery(function ($) {
    "use strict";

   // tabs
    var exercise = $('#exercise-level #id_level');
    var test = $('#test-level #id_level');
    var exam = $('#exam-level #id_level');
    var new_exercise = $('#id_exercise_type');


    new_exercise.on('change', function () {
        console.log('fetch');
        $.ajax({
              type: "POST",
              url: "/fetch/",
              data: { exercise_type: new_exercise.val() }
        }).done(function( msg ) {
            $('.ajax-result').html(msg);
            $('#add').show();
        }); 
    });

    exercise.on('change', function () {
        console.log('Will generate a test');
    }); 


    test.on('change', function() {
        console.log('Will bring you a single exercise');
    });

    exam.on('change', function() {
        console.log('Will bring you a single exercise');
    });

});
