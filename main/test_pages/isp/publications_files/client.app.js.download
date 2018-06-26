define([
	// define global dependencies
	"jquery",
	"client.navigation",
	"client.userInterface",
	"client.carousel"
], function ($) {
	"use strict";

	// list global scripts to execute on DOM ready
	$(function() {
		// bind a click event to the 'skip-nav' link and give focus
		$(".skip-nav").click(function(event){
			var skipTo="#"+this.href.split('#')[1];
			$(skipTo).attr('tabindex', -1).on('blur focusout', function () {
				$(this).removeAttr('tabindex');
			}).focus();
		});

	});

	function initApp(){
		log('init app');
	}

	return{
		init:initApp
	};

});





