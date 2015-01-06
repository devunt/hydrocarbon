// base.js
// 141211
// - initial version

// Disable enter to submit form
// http://stackoverflow.com/a/587575
function checkEnter(e){
	e = e || event;
	var txtArea = /textarea/i.test((e.target || e.srcElement).tagName);
	return txtArea || (e.keyCode || e.which || e.charCode || 0) !== 13;
}



var $overlay,
	$tooltip,
	$menu,
	csrftoken = $.cookie('csrftoken'),
	browser = {
		can : {
			placeholder: function() { return 'placeholder' in document.createElement('input'); }
		}
	},
	taggingJS_options = {
		'case-sensitive': true,
		'forbidden-chars': [','],
		'forbidden-chars-text': '이하의 문자는 사용할 수 없습니다:\n',
		'forbidden-words-text': '이하의 단어는 사용할 수 없습니다:\n',
		'no-duplicate-text': '이하의 태그는 이미 선택되어 있습니다:\n',
		'tag-char': '',
		'no-spacebar': true,
		'tag-on-blur': false
	},
	autocomplete_options = {
		'serviceUrl': '/x/t',
		'type': 'POST',
		'minChars': 2,
		'lookupLimit': 5,
		'preserveInput': true,
		'formatResult': function(suggestion, currentValue) {
			return '<span class="left">' + $.Autocomplete.formatResult(suggestion, currentValue) + '</span><span class="right">' + suggestion.data + '</span>';
		},
		'onSelect': function(suggestion) { this.focus(); },
		'zIndex': 1050
	}

$(function() {

	$window = $(window);
	$document = $(document);
	$body = $('body');
	$overlay = $('#overlay');
	$tooltip = $('#tooltip');
	$menu = $('.dropdown.container');

	$document
		.one('touchstart', function() {
			$('html').removeClass('no-touch');

			$document.off('mouseenter mouseleave', '.th');
		})

		.on('keypress', '.type-zone', checkEnter)

		.on('click', '.dropdown.container .handle', function(e) {
			var $container = $(this).closest('.container');
			if(!$container.hasClass('open')) { $container.addClass('open');
			} else { $container.removeClass('open'); }
		})
		.on('mouseleave', '.dropdown.container', function() { if($(this).hasClass('open')) $(this).removeClass('open'); })
		.on('click', '.dropdown.container .handle[href=#]', function(e) { e.preventDefault(); })
		.on('mousedown', '.dropdown.container .close', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.container');
			$container.removeClass('open');
		})

		.on('click', 'a.checkbox', function(e) {
			if($(this).attr('href') != '#') return true;

			e.preventDefault();

			var $checkbox = $(this).prev('input[type=checkbox]');

			$(this).toggleClass('checked');
			$checkbox.prop('checked', !$checkbox.prop('checked'));
		})

		.on('mouseenter', '.th', showTooltip)
		.on('mouseleave scroll', '.th', hideTooltip)
		.on('touchstart', '.th:not(.th-active)', showTooltip)
		.on('touchstart', '.th.th-active', hideTooltip)
		.on('mouseenter touchstart', '*[title]', function(e) {
			if($(this).closest('.note-editor').length) return false;
			$(this)
				.data('title', $(this).attr('title'))
				.removeAttr('title')
				.addClass('th');
			showTooltip(e);
		});

	$('.article img').each(function() {
		if($(this).parents('a').length > 0) { return false; } else {
			var a = $('<a>');

			a
				.addClass('imagecontainer')
				.attr('href', $(this).attr('src'))
				.attr('target', '_blank');

			$(this).wrap(a);
		}
	});

	$('input[type=checkbox]').each(function() {
		var $label;

		$label = $(this).closest('label').length ? $(this).closest('label') : $label;
		$label = $(this).next('label').length ? $(this).next('label') : $label;
		$label = $(this).prev('label').length ? $(this).prev('label') : $label;

		var $a = $('<a>')
			.attr('href', '#')
			.addClass('checkbox')
			.html('<span class="label"><span class="icon"></span></span>')

		if($(this).prop('checked')) $a.addClass('checked');

		$a
			.insertAfter($label)
			.find('.label').append('<span class="text">' + $.trim($label.text()) + '</span>');
		$(this).insertAfter($label);

		$(this).hide();
		$label.remove();
	});

	$('.post.item .label.meta.comments')
		.on('mouseenter', function() {
			var $item = $(this).closest('a.post.item');

			$item.attr('href', $item.attr('href') + '#comments');
		})
		.on('mouseleave', function() {
			var $item = $(this).closest('a.post.item');

			$item.attr('href', $item.attr('href').replace('#comments', ''));
		});

	$('.post.item .label.meta.author.user')
		.on('mouseenter', function() {
			var $item = $(this).closest('a.post.item');

			$item.attr('href', $(this).data('user-id-url'));
		})
		.on('mouseleave', function() {
			var $item = $(this).closest('a.post.item');

			$item.attr('href', '/' + $item.data('post-id') + '/');
		});

	$('.section.article.form form')
		.on('submit', function() {
			$('#tagbox').tagging('add');
			$tags.val($tagbox.tagging('getTags').join(','));
		})
		.find('.category')
			.on('click', 'a.option', function(e) {
				e.preventDefault();
				$('.section.article.form .category option').filter('[value='+$(this).data('value')+']').prop('selected', true).trigger('change');
				$('.section.article.form .category .text').text($(this).text());
				$(this).closest('.dropdown.container').removeClass('open');
			})
			.each(function() {
				var option, $handle = $('<a>'), $dropdown = $('<div>'), $ul = $('<ul>');

				option = $(this).find('select option');

				$('<span>')
					.html('<span>'+$(this).data('text')+'</span>')
					.addClass('text')
					.appendTo($handle);

				$('<span>')
					.addClass('icon')
					.appendTo($handle);

				$handle
					.attr('href', '#')
					.addClass('handle label meta')
					.appendTo($(this));

				$('<a>')
					.addClass('close')
					.attr('href', '#')
					.appendTo($dropdown);

				$('<div>')
					.addClass('tip top')
					.html('<span></span>')
					.appendTo($dropdown);

				option.each(function() {
					var $li = $('<li>'), $a = $('<a>'), value = $(this).attr('value');

					if(value == '') return true;

					if($(this).prop('selected')) $(this).closest('.dropdown.container').find('.handle .text span').text($(this).text());

					$('<span>')
						.text($(this).text())
						.appendTo($a);

					$a
						.attr('href', '#')
						.addClass('option')
						.data('value', value)
						.appendTo($li);

					switch($(this).text()) {
						case '번역':
							$li.addClass('scanlation');
							break;
						case '자막':
							$li.addClass('subtitles');
							break;
						case '정보':
							$li.addClass('news');
							break;
					}

					$li.appendTo($ul);
				});

				$ul.appendTo($dropdown);

				$dropdown
					.addClass('dropdown menu')
					.appendTo($(this));

				$(this).find('select').hide();
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
		vote('p', $(this).parent('.vote').data('target-id'), $(this));
	});

	$('.section.board')
		.on('click', '.search.button .label.meta.search', function(e) {
			e.preventDefault();

			var $nav = $(this).closest('.nav.bottom');

			$nav
				.addClass('open')
				.removeClass('close');

		})
		.on('click', '.search.button .label.meta.delete', function(e) {
			e.preventDefault();

			var $nav = $(this).closest('.nav.bottom');

			$nav
				.removeClass('open')
				.addClass('close');
		});

	$('.tabs')
		.on('click', '.tab.header a:not(.current)', function() {
			var $container = $(this).closest('.tabs'),
				target = $(this).attr('href').replace('#', '.');

			$container.find('.section').hide();
			$container.find(target).show();

			$container.find('.tab.header a').removeClass('current');
			$(this).addClass('current');

		})
});

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

	$tooltip.find('.container p').html($target.data('title').replace(/\\n/gi, '<br>'));
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

	$('.th-active').removeClass('th-active');
	$target.addClass('th-active');

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
	$('.th-active').removeClass('th-active');

	$tooltip
		.stop()
		.animate({'opacity': 0}, 100, function() { $tooltip.hide(); });
}

function vote(type, target, button) {
	var vote, avote, work,
		$sibling_voted = button.siblings('.voted'),
		databox = {
			type: type,
			target: target,
			vote: null
		};

	work = button.hasClass('voted') ? '-' : '+';
	vote = button.hasClass('upvote') ? '+' : '-';
	avote = (vote == '+') ? '-' : '+';

	if(work == '+' && $sibling_voted.length) {
		$ajax_vote({type: type, target: target, vote: '-' + avote}, $sibling_voted)
			.done(function(data, status, xhr) {
				$ajax_vote({type: type, target: target, vote: work + vote})
					.done(function(data) { vote_callback(data, work, button); });

				vote_callback(data, '-', $sibling_voted);
			});
	} else { $ajax_vote({type: type, target: target, vote: work + vote}).done(function(data) { vote_callback(data, work, button); }); };
}

function vote_callback(data, work, button) {
	if(work == '+') { button.addClass('voted');
	} else { button.removeClass('voted'); }

	var $score = button.closest('.item').find('.meta.score');

	$score
		.attr('title', '+'+data.current.upvote+' / -'+data.current.downvote)
		.find('.text span').text(data.current.total);
}

function $ajax_vote(databox) {
	return $.ajax({
			type: 'POST',
			url: VOTE_AJAX_ENDPOINT,
			data: databox
		})
			.fail(function(xhr, status, error) {
				var response = xhr.responseJSON.status;
				switch(response) {
					case 'notauthenticated':
						alert('로그인한 사용자만 사용 가능한 기능입니다.');
						break;

					case 'alreadyhave':
						alert('이미 추천한 게시글 또는 댓글입니다.');
						break;

					default:
						alert('알 수 없는 문제가 발생하였습니다.');
						console.log(databox);
						console.log(xhr);
						console.log(status);
						console.log(error);
				}
			});
}
