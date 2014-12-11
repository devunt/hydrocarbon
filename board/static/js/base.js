// base.js
// 141211
// - initial version

$(function() {

	$window = $(window);
	$document = $(document);
	$overlay = $('#overlay');
	$tooltip = $('#tooltip');

	$('*[title]').on('mouseenter',function() {
		var title = $(this).attr('title');
		$(this)
			.removeAttr('title')
			.addClass('th')
			.data('title', title);
	});

	$document.on('mouseenter', '.th', function(e) { showTooltip(e) });
	$document.on('mouseleave', '.th', function() { hideTooltip() });
	$document.on('scroll', function() { hideTooltip() });

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

	top = position.top + targetHeight;
	left = position.left + targetWidth/2;

	height = $tooltip.height();
	width = $tooltip.width();

	offsetX = $document.width() - (left + width/2);
	offsetY = $document.height() - (top + height);

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
