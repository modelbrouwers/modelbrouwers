var urlconf = urlconf || {};

(function(win, $, Q, hbs) {
	var _urlconf = {
		groupbuilds: {
			groupbuild: {
				detail: 'groupbuilds/groupbuild/{0}/'
			},
			participant_check: 'groupbuilds/participant/check/'
		}
	};
	win.urlconf = $.extend(true, win.urlconf || {}, _urlconf);


	function GroupBuild(id) {
		this.id = id;
	}

	GroupBuild.prototype.render = function($container) {
		var endpoint = urlconf.groupbuilds.groupbuild.detail.format(this.id);
		Api.request(endpoint)
			.get()
			.then(function(data) {
				hbs.render('groupbuilds::inset', data, $container);
			});
	};

	/**
	 * Check if a topic was created
	**/
	function checkParticipantTopicCreated() {
		// check the referrer - did we come from create topic?
		var $referrer = $.url(document.referrer);
		var thisHost = $referrer.attr('host') == $.url().attr('host');
		var postCreated = thisHost
						 && $referrer.attr('file') == 'posting.php'
						 && $referrer.param('mode') == 'post';

		// we're coming from the posting page, so check if the topic was created
		if ( postCreated ) {
			var endpoint = urlconf.groupbuilds.participant_check;
			var requestData = {
				'forum_id': $referrer.param('f'),
				'topic_id': $.url().param('t') || null
			}
			Api.request(endpoint, requestData).get().done(function(data) {
				console.log(data);
			});
		}
	}

	// jQuery initialization
	$(function() {
		var gb;
		// get the page insets and render
		$('div.gb-inset').each(function() {
			gb = new GroupBuild($(this).data('id'));
			gb.render($(this));
		});

		checkParticipantTopicCreated();
	});

}(window, jQuery, Q, Handlebars));
