jQuery(function ($) {
	"use strict";
	
	var exercise_level = $('#exercise-level #id_level');
	var test_level = $('#test-level #id_level');
	var exam_level = $('#exam-level #id_level');

    exercise_level.on('change', function () {
        console.log('get exercise');
        $.ajax({
              type: "POST",
              url: "/get-exercise/",
              data: { exercise_level: exercise_level.val() }
        }).done(function( msg ) {
            $('.container').html(msg);
        }); 
    });
	
	test_level.on('change', function(){
		console.log('get test');
		//TODO a lot...
	});
});