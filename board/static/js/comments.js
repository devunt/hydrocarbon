function getComments(id) {
	return $.ajax({
		type: 'GET',
		url: '/x/c/' + id
	})
		.done(function(data, status, xhr) {
			var $article = $('.section.article'), $container = $('.comments-list ul'), count = data.comments.length;
			$container.find('.list.item').remove();

			$.each(data.comments, function(i, v) {
				var $c = $container.find('.list.template').clone(), date = new Date(v.created_time);

				$c.find('.meta.author .text').text(v.author);
				$c.find('.meta.timestamp')
					.attr('title', date.toLocaleString('ko-kr', { hour12: false }))
					.text($.timeago(v.created_time));
				$c.find('.article').html(v.contents);

				$c
					.data('id', v.id)
					.addClass('item')
					.removeClass('template')
					.insertBefore($container.find('.write'))
					.show();
			});

			$article
				.find('.item.article .header .label.meta.comments .text, .item.article .footer .label.meta.comments .text span')
				.add('.post-id-'+id+' .label.meta.comments .text')
					.text(count);

			$('.comments-list .write textarea').val('');
		})
		.fail(function(xhr, status, error) {
			console.log(xhr);
			console.log(status);	
			console.log(error);

			alert('댓글을 불러오는 과정에서 오류가 발생했습니다.');
		});
}

function postComments(id, contents, type) {
	return $.ajax({
		type: 'POST',
		url: '/x/c/' + id,
		data: {
			contents: contents,
			type: type
		}
	})
		.fail(function(xhr, status, error) {
			console.log(xhr);
			console.log(status);
			console.log(error);

			alert('댓글을 등록하는 과정에서 오류가 발생했습니다.');
		});
}
