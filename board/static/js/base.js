// base.js
// 141211
// - initial version

$(function() {

	$window = $(window);
	$document = $(document);
	$body = $('body');
	$overlay = $('#overlay');
	$tooltip = $('#tooltip');
	$menu = $('.menu');

	$('.hoverable').hover(function() {
		$(this).addClass('hover');
		$body.addClass('hovered');
	}, function() {
		$(this).removeClass('hover');
		$body.removeClass('hovered');
	});

	$menu
		.on('click', '.handle[href="#"]', function(e) {
			e.preventDefault();
			$(this).closest('.menu').mouseenter();
		})
		.on('click', '.close', function(e) {
			e.preventDefault();
			$menu.mouseleave();
		});

	$document
		.on('mouseenter', '.th', showTooltip)
		.on('mouseleave scroll', '.th', hideTooltip)
		.on('mouseenter', '*[title]', function() {
			if($(this).closest('.note-editor').length) return false;
			$(this)
				.data('title', $(this).attr('title'))
				.removeAttr('title')
				.addClass('th')
				.trigger('mouseenter');
		});

	if(!browser.can.placeholder()) {
		$('#form_login .field input').each(function() {
			$('<label>')
				.attr('for', $(this).attr('id'))
				.append('<span>'+$(this).attr('placeholder')+'</span>')
				.insertAfter($(this).addClass('noplaceholder'));
		});
	}

	$('#form_login')
		.on('load focusin focusout', '.field input.noplaceholder', function() {
			if(this.value == '') { $(this).next('label').show();
			} else { $(this).next('label').hide(); }
		})
		.on('keypress', '.field input.noplaceholder', function() {
			$(this).next('label').hide();
		});

	$('.vote a').on('click', function(e) {
		e.preventDefault();

		var $sibling_voted = $(this).siblings('.voted');

		var vote;
		var avote;
		var work;
		var button;
		var callback;

		var databox = {
			type: null,
			target: null,
			vote: null
		}

		if($(this).hasClass('vote-post')) databox.type = 'p';
		if($(this).hasClass('vote-comment')) databox.type = 'c';

		databox.target = $(this).parent('.vote').data('target-id');

		if($(this).hasClass('voted')) { work = '-';
		} else { work = '+'; }

		if($(this).hasClass('upvote')) { 
			vote = '+';
			avote = '-';
		}
		if($(this).hasClass('downvote')) {
			vote = '-';
			avote = '+';
		}

		button = $(this);

		if(work == '+' && $sibling_voted.length) {
			$ajax_vote(databox, '-' + avote, $sibling_voted)
				.done(function() { $ajax_vote(databox, work + vote, button); });
		} else { $ajax_vote(databox, work + vote, button); }
	});

});

var $overlay;
var $tooltip;
var $menu;

var csrftoken = $.cookie('csrftoken');

var funct = function() {};

var browser = {
	can : {
		placeholder: function() { return 'placeholder' in document.createElement('input'); }
	}
}

function csrfSafeMethod(method) { return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)); }

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});

function showTooltip(e) {
	var $target = $(e.target).closest('.th');
	var position = $target.offset();

	var targetHeight = $target.outerHeight();
	var targetWidth = $target.outerWidth();

	var offsetY = 0;
	var offsetX = 0;

	var top;
	var left;

	var height;
	var width;

	var margin = 10;

	$tooltip.find('.container p').html($target.data('title').replace('\\n', '<br>'));
	$tooltip.find('.tip').removeAttr('style');

	top = position.top + targetHeight;
	left = position.left + targetWidth/2;

	height = $tooltip.height();
	width = $tooltip.width();

	if(top + height + margin > $window.height() + $window.scrollTop()) offsetY = -1*(targetHeight + height);

	offsetX = $window.width() + $window.scrollLeft() - left;

	if(offsetX - (width/2 + margin) < 0) {
		offsetX = offsetX - (width/2 + margin);
		if(width/2 + offsetX < 0 ) return false;
	} else if(offsetX + (width/2 + margin) > 0) {
		offsetX = offsetX + width/2 + margin - $window.width();
		if(offsetX < 0) offsetX = 0;
		if(width/2 - offsetX < 0 ) return false;
	} else { offsetX = 0; }

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
			.filter((offsetY >= 0) ? '.top' : '.bottom').show();
}

function hideTooltip() {
	$tooltip
		.stop()
		.animate({'opacity': 0}, 100, function() { $tooltip.hide(); });
}

function $ajax_vote(databox, vote, button) {
	databox.vote = vote;
	return $.ajax({
			type: 'POST',
			url: '/x/v',
			data: databox
		})
			.done(function(data, status, xhr) {
				if(databox.vote.charAt(0) == '+') { button.addClass('voted');
				} else { button.removeClass('voted'); }

				var $score = button.closest('.item').find('.meta.score');

				$score
					.attr('title', '+'+data.current.upvote+' / -'+data.current.downvote)
					.find('.text span').text(data.current.total);
			})
			.fail(function(xhr, status, error) {
				switch(error) {
					case 'UNAUTHORIZED':
						alert('로그인한 사용자만 사용 가능한 기능입니다.');
						break;
					default:
						alert('알 수 없는 문제가 발생하였습니다.');
						console.log(status);
						console.log(error);
				}
			});
}
