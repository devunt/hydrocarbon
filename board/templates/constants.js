var user = {
	id: {{ user.id | default:'null' }},
	nick: "{{ user.nickname }}",
	c3RhZmY = {{ user.is_staff | lower }},
	authenticated: {{ user.is_authenticated | lower }}
}


var VOTE_AJAX_ENDPOINT = "{% url 'ajax_vote' %}"

function get_comment_ajax_url(id) {
	return "{% url 'ajax_comment' 0 %}".replace(/0/, id);
}
