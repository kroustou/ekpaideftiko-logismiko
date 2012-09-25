jQuery(function ($) {
	"use strict";
	
	var exerciseSwitcher = $('#exercise-level select');
  var exercise_level = $('#exercise-level #id_level');
  var exercise_chapter = $('#exercise-level #id_chapter');


    exerciseSwitcher.on('change', function () {
        $.ajax({
              type: "POST",
              url: "/get-exercise/",
              data: { exercise_level: exercise_level.val() , chapter: exercise_chapter.val() }
        }).done(function( msg ) {
            $('.container').html(msg);
        }); 
    });

  var testSwitcher = $('#test-level select');
	var test_level = $('#test-level #id_level');
  var test_chapter = $('#test-level #id_chapter');
  
  testSwitcher.on('change', function(){
    $.ajax({
            type: "POST",
            url: "/get-test/",
            data: { test_level: test_level.val() , chapter: test_chapter.val() }
        }).done(function( msg ) {
            $('.container').html(msg);
        }); 
  });
  

  // var exam_level = $('#exam-level #id_level');
});
