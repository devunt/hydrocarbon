var user = {
	id: {{ user.id | default:'null' }},
	nick: "{{ user.nickname }}",
	c3RhZmY: {{ user.is_staff | lower }},
	authenticated: {{ user.is_authenticated.value | lower }}
}


var BOARD_CATEGORIES = { {% for cat in BOARD_CATEGORIES %}{{ cat.id }}: "{{ cat.slug }}"{% if not forloop.last %}, {% endif %}{% endfor %} }


var COMMENT_BLIND_VOTES = {{ BOARD_COMMENT_BLIND_VOTES }}
var COMMENT_MAX_DEPTH = {{ BOARD_COMMENT_MAX_DEPTH }}


var VOTE_AJAX_ENDPOINT = "{% url 'ajax_vote' %}"

function get_comment_ajax_url(id) {
	return "{% url 'ajax_comment' 0 %}".replace(/0/, id);
}


var COMMENT_FROALA_EDITOR_OPTIONS = {{ COMMENT_FROALA_EDITOR_OPTIONS | safe }}
