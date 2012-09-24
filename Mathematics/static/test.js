jQuery(function ($) {
	"use strict";
	
	var exercise_level = $('#exercise-level #id_level');


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
});