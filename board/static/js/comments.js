var options;

function getComments(id) {
	return $.ajax({
		type: 'GET',
		url: get_comment_ajax_url(id) + '?t=' + new Date().getTime()
	})
		.done(function(data, status, xhr) {
			var $article = $('.section.article'), $container = $('.comments-list > div'), count = data.comments.count;
			$container.find('.list.item, .clone').remove();

			$.each(data.comments.list, function(i, v) { renderComment($container, v); });

			$article
				.find('.item.article .header .label.meta.comments .text, .item.article .footer .label.meta.comments .text span')
				.add('.post-id-'+id+' .label.meta.comments .text')
					.text(count);
		})
		.fail(function(xhr, status, error) {
			console.log(xhr);
			console.log(status);	
			console.log(error);

			alert('댓글을 불러오는 과정에서 오류가 발생했습니다.');
		});
}

function renderComment($container, v, depth, hidden) {
	depth = typeof depth !== 'undefined' ? depth : 0;

	var $c = $container.find('.list.template').clone(),
		date = new Date(v.created_time), contents,
		hash = window.location.hash;

	if(v.iphash) {
		$c
			.addClass('guest')
			.find('.meta.author')
				.removeClass('user')
				.addClass('guest')
				.attr('title', v.iphash);
	} else {
		 if(v.author == user.nick && user.authenticated) $c.addClass('owned');
		 $c.find('a.meta.author')
			.attr('href', v.author_url)
		 	.attr('title', '+' + v.author_total_score);
	}

	if(user.c3RhZmY) $c.find('.manipulate').show();

	if(depth > 0) {
		$c.find('.bubble.item').addClass('indent');

		if(depth <= 4) {
			$c.css('margin-left', 3*depth+'%');
		} else {
			$c.css('margin-left', 12+'%');
			for(i = 4; i < depth; i++) {
				$c.find('.depth')
					.append('<i class="fa fa-angle-right"></i>');
			}
		}
	}

	if(depth >= COMMENT_MAX_DEPTH) $c.find('div.reply').remove();

	if(!hidden && v.votes.total <= COMMENT_BLIND_VOTES) $c.addClass('hidden');

	$c.find('a.anchor').attr('id', 'c'+v.id);

	$c.find('.meta.author .text').text(v.author);
	$c.find('.meta.timestamp')
		.attr('title', date.toLocaleString('ko-kr', { hour12: false }))
		.text($.timeago(v.created_time));

	if(v.votes.total >= 0 ) v.votes.total = '+' + v.votes.total;
	
	$c.find('.meta.score')
		.attr('title', '+'+v.votes.upvote+' / -'+v.votes.downvote)
		.find('.text span').text(v.votes.total);

	contents = v.contents;
	$c.find('.article .editor').html(contents);

	$c.find('.article .editor img').each(function() {
		if(!$(this).parents('a').length > 0) {
			var a = $('<a>');

			a
				.addClass('imagecontainer')
				.attr('href', $(this).attr('src'))
				.attr('target', '_blank');

			$(this).wrap(a);
		}
	});

	if(v.voted.upvoted) $c.find('.dropdown .upvote').addClass('voted');
	if(v.voted.downvoted) $c.find('.dropdown .downvote').addClass('voted');

	$c
		.data('id', v.id)
		.data('depth', depth)
		.addClass('item')
		.removeClass('template')
		.insertBefore($container.find('.write.template'))
	
	if(!hidden) $c.show();

	if(v.subcomments) {
		if(v.votes.total <= COMMENT_BLIND_VOTES || hidden) {
			$.each(v.subcomments, function(i, v) {
				renderComment($container, v, depth + 1, true);
			});
		} else {
			$.each(v.subcomments, function(i, v) {
				renderComment($container, v, depth + 1);
			});
		}
	}

	if(hash.match(/^#c[0-9]+/) && v.id == hash.replace('#c', '')) {
		$window.scrollTop($(hash).offset().top);
	}

	return $c;
}

function postComments(id, databox) {
	return $.ajax({
		type: 'POST',
		url: get_comment_ajax_url(id),
		data: databox
	})
		.fail(function(xhr, status, error) {
			var response = xhr.responseJSON.status;
			switch(response) {
				case 'badrequest':
					var errorstr = '';

					jQuery.each(xhr.responseJSON.error_fields, function(i, v) {
						if(v == 'contents') errorstr = errorstr +'내용을 입력해 주세요.\n';
						if(v == 'nick') errorstr = errorstr +'닉네임을 입력해 주세요.\n';
					});

					alert(errorstr);

					break;

				default:
					alert('댓글을 등록하는 과정에서 오류가 발생했습니다.');
					console.log(databox);
					console.log(xhr);
					console.log(status);
					console.log(error);
			}
		});
}

function putComments(id, contents, password) {
	return $.ajax({
		type: 'PUT',
		url: get_comment_ajax_url(id),
		data: { contents: contents },
		headers: { 'X-HC-PASSWORD': password }
	})
		.fail(function(xhr, status, error) {
			switch(error) {
				case 'FORBIDDEN':
					alert('이 댓글을 수정할 권한이 없습니다. 비밀번호를 잘못 입력하셨나요?');
					break;

				case 'BAD REQUEST':
					var errorstr = '';

					jQuery.each(xhr.responseJSON.error_fields, function(i, v) {
						if(v == 'contents') errorstr = errorstr +'내용을 입력해 주세요.\n';
						if(v == 'nick') errorstr = errorstr +'닉네임을 입력해 주세요.\n';
					});

					alert(errorstr);

					break;

				default:
					console.log(xhr);
					console.log(status);
					console.log(error);
					alert('댓글을 수정하는 과정에서 오류가 발생했습니다.');
			}
		});
}

function deleteComments(id, password) {
	return $.ajax({
		type: 'DELETE',
		url: get_comment_ajax_url(id),
		headers: { 'X-HC-PASSWORD': password }
	})
		.fail(function(xhr, status, error) {
			switch(error) {
				case 'FORBIDDEN':
					alert('이 댓글을 삭제할 권한이 없습니다. 비밀번호를 잘못 입력하셨나요?');
					break;

				default:
					console.log(xhr);
					console.log(status);
					console.log(error);
					alert('댓글을 삭제하는 과정에서 오류가 발생했습니다.');
			}
		});
}

function toggleComments(action, target) {
	var $container = $(target).closest('.comments-list > div'),
		$item = $(target).closest('div.list.item'),
		item_depth = $item.data('depth'),
		item_index = $item.index();

	if(action == 'toggle') $item.toggleClass('hidden');
	if(action == 'hide') $item.addClass('hidden');
	if(action == 'show') $item.removeClass('hidden');

	$.each($container.find('div.list.item'), function(index, it) {
		var depth = $(it).data('depth');

		if(index <= item_index - 1) return true;
		if(depth <= item_depth) return false;
		
		if(action == 'toggle') {
			if($item.hasClass('hidden')) { $(it).hide();
			} else { $(it).removeClass('hidden').show(); }
		}
		if(action == 'hide') $(it).hide();
		if(action == 'show') $(it).removeClass('hidden').show();
	});
}

$(function() {
	$('.section.article .item.article .footer')
		.on('click', 'a', function(e) {
			var action = $(this).attr('href').replace('#', '');

			switch(action) {
				case 'toggle':
					e.preventDefault();
					$('.comments-list').toggle();
					break;

				case 'refresh':
					e.preventDefault();
					getComments($('.section.article').data('id'));
					break;
			}
		});

	$('.comments-list')
		.on('keypress', '.modify, .write', function(e) {
			if(e.ctrlKey && (e.which == 10 || e.which == 13)) {
				$(this).find('.submit.button').trigger('click');
				e.preventDefault();
				return false;
			}
		})
		.on('click', ':not(.prerender) .header', function(e) {
			if(!$(e.target).closest('a').length) {
				e.preventDefault();
				toggleComments('toggle', this);
			}
		})
		.on('click', '.write .submit', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.write'),
				editor = $container.find('textarea'),
				text = editor.editable("getHTML"),
				nick = $container.find('.footer label.nick input').val(),
				password = $container.find('.footer label.password input').val(),
				id = $container.data('id'),
				type = $container.data('type'),
				databox = {
					contents: text,
					type: $container.data('type'),
					ot_nick: nick,
					ot_password: password
				};

			if(text == '') {
				alert('내용을 입력해 주세요.');
				return false;
			}

			if(type == 'c') id = $container.prev('div.list.item').data('id');

			postComments(id, databox)
				.done(function() {
					editor.editable('setHTML', '');
					getComments(post_id)
						.done(function() {
							if(type == 'c') window.location.hash = '#c' + id;
						});
				});
		})
		.on('click', '.modify .submit', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.modify'),
				editor = $container.find('textarea'),
				text = editor.editable("getHTML"),
				id = $container.data('id'),
				password = $container.find('.footer label.password input').val();

			if(text == '') {
				alert('내용을 입력해 주세요.');
				return false;
			}

			putComments(id, text, password)
				.done(function() {
					getComments(post_id)
						.done(function() {
							window.location.hash = '#c' + id;
						});
				});
		})
		.on('click', '.reply .cancel', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.reply');

			$container.prev('.reply').removeClass('reply')
			$container.remove();
		})
		.on('click', '.modify .cancel', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.modify');

			$container.prev('.list.item').show();
			$container.remove();
		})
		.on('click', '.delete .submit', function(e) {
			e.preventDefault();
			var $item = $(this).closest('div.list.item'),
				password = $item.find('.footer label.password input').val();

			deleteComments($item.data('id'), password)
				.done(function() { getComments(post_id) });
		})
		.on('click', '.delete .cancel', function(e) {
			e.preventDefault();
			var $container = $(this).closest('.footer');

			$container.closest('.delete').removeClass('delete');
			$container.remove();
		})
		.on('click', '.dropdown.menu li a', function(e) {
			$(this).closest('.dropdown.container.open').removeClass('open');

			var $container = $('.comments-list > div'), action = $(this).attr('href');

			switch(action) {
				case '#upvote':
				case '#downvote':
					e.preventDefault();
					var button = $(this).closest('li.vote'),
						$item = $(this).closest('div.list.item');
					vote('c', $item.data('id'), button);

					break;

				case '#reply':
					e.preventDefault();
					var scroll,
						$c = $container.find('.write.template').clone(),
						$item = $(this).closest('div.list.item').not('.reply'),
						editor = $c.find('textarea');

					$('.reply .cancel').click();

					$item.addClass('reply');

					$c.find('textarea')
						.removeAttr('id')
						.val('')
						.appendTo($c.find('.article'))
						.show();

					$c.find('.froala-box').remove();
					$c.find('script').remove();

					$c
						.removeAttr('data-type data-id')
						.data('type', 'c')
						.data('id', $item.data('id'))
						.addClass('clone reply indent')
						.removeClass('template')
						.insertAfter($item)
						.show();

					if($item.data('depth') <= 3) {
						$c.css('margin-left', 3*($item.data('depth') + 1)+'%');
					} else {
						$c.css('margin-left', 12+'%');
					}

					$c.find('input').removeAttr('id');

					editor.editable(COMMENT_FROALA_EDITOR_OPTIONS);
					editor.editable('focus');
					$c.find('.cancel').show();

					$('body').scrollTop($c.offset().top - 60);

					break;

				case '#modify':
					e.preventDefault();
					var $c = $container.find('.write.template').clone(),
						$item = $(this).closest('div.list.item'),
						editor = $c.find('textarea');

					$item.hide();

					editor
						.removeAttr('id')
						.val('')
						.appendTo($c.find('.article'))
						.show();

					$c.find('.froala-box').remove();
					$c.find('script').remove();

					$c
						.css('margin-left', $item.css('margin-left'))
						.removeAttr('data-type')
						.data('id', $item.data('id'))
						.addClass('clone modify')
						.removeClass('template write')
						.insertAfter($item)
						.show();

					if($item.data('depth') > 0) $c.find('.bubble.item').addClass('indent');

					if(user.c3RhZmY) { $c.find('label').remove();
					} else if($item.hasClass('guest')) {
						$c.find('label.nick').remove();
						$c.find('label').show();
					}

					$c.find('input').removeAttr('id');

					editor.editable(COMMENT_FROALA_EDITOR_OPTIONS);
					editor.editable('setHTML', $item.find('.article .froala-element.editor').html());
					editor.editable('focus');
					$c.find('.cancel').show();

					$c.find('.submit').text('수정');

					break;

				case '#delete':
					e.preventDefault();
					var $c = $container.find('.write.template .footer').clone(), $item = $(this).closest('div.list.item').not('.delete');

					$item.addClass('delete');

					$c.appendTo($item.find('.bubble.item > .container'));

					if(user.c3RhZmY) { $c.find('label').remove();
					} else if($item.hasClass('guest')) {
						$c.find('label.nick').remove();
						$c.find('label').show();
					}

					$c.find('input').removeAttr('id');

					$c.find('.cancel')
						.show();

					$c.find('.submit')
						.text('삭제')
						.removeClass('blue')
						.addClass('red');

					$('body').scrollTop($c.offset().top - 100);

					break;

				default:
					console.log(action);
			}
		});
});
