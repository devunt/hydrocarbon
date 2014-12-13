// base.js
// 141211
// - initial version

$(function() {

	$window = $(window);
	$document = $(document);
	$overlay = $('#overlay');
	$tooltip = $('#tooltip');

	$('.hoverable').hover(function() { $(this).addClass('hover'); },
			function() { $(this).removeClass('hover'); });

	$document
		.on('mouseenter', '.th', showTooltip)
		.on('mouseleave scroll', '.th', hideTooltip)
		.on('mouseenter', '*[title]', function() {
			$(this)
				.data('title', $(this).attr('title'))
				.removeAttr('title')
				.addClass('th')
				.trigger('mouseenter');
		});		

	$('#form_login')
		.on('load focusin focusout', '.field input', function() {
			if(this.value == '') { $(this).next('label').show();
			} else { $(this).next('label').hide(); }
		})
		.on('keypress', '.field input', function() {
			$(this).next('label').hide();
		});

});

var $overlay;
var $tooltip;

function showTooltip(e) {
	var $target = $(e.target).closest('.th');
	var position = $target.offset();

	var targetHeight = $target.outerHeight();
	var targetWidth = $target.outerWidth();

	var offsetY;
	var offsetX;

	var top;
	var left;

	var height;
	var width;

	$tooltip.find('.container p').text($target.data('title'));
	$tooltip.find('.tip').removeAttr('style');

	top = position.top + targetHeight;
	left = position.left + targetWidth/2;

	height = $tooltip.height();
	width = $tooltip.width();

	offsetX = $window.width() - (left + width/2);
	offsetY = $window.height() - (top + height);

	offsetX = (offsetX < 0) ? offsetX - 10 : 0;
	offsetY = (offsetY < 0) ? -1*(height + targetHeight) - 2 : 2;

	$tooltip
		.css({
			'top': top + offsetY,
			'left': left - width/2 + offsetX
		})
		.show()
		.stop()
		.animate({'opacity': 1}, 100)
		.find('.tip')
			.hide()
			.css('margin-left', -2*offsetX)
			.filter((offsetY > 0) ? '.top' : '.bottom').show();
}

function hideTooltip() {
	$tooltip
		.stop()
		.animate({'opacity': 0}, 100, function() { $tooltip.hide(); });
}
