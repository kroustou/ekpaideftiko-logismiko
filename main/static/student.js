jQuery(function ($) {
	"use strict";
	

	$('.rename').on('click', function(e) {
		e.preventDefault();
		var current = $(this).parent();
		var name = current.find('.name').val();
		var lastName = current.find('.last_name').val();
		var id = current.attr('class');
		var that = this;
		$.ajax({ 
			type: "POST",
			url: "/student/",
			enctype: 'multipart/form-data',
			data: {
				name: name,
				last_name : lastName,
				id : id
			},
			success: function(data){
				$(that).html('άλλαξε!');
			}
		});     
	});
});
