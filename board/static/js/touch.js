// mobile.js
// 141211
// - initial version

$(function() {

	$menu = $('.menu');

	$('.hovermenu .handle').on('click', function(e) {
		e.preventDefault();
		$(this).parent('.menu').addClass('hover');
	});

	$menu.on('click', '.close' function(e) {
		e.preventDefault();
		$menu.removeClass('hover');
	});

	$('.hoverable').each(function() {
		$(this).removeClass('hoverable');
	});
});

var $menu;
