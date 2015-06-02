var urlconf = urlconf || {};

(function(win, $, Q, hbs) {
	var _urlconf = {
		groupbuilds: {
			groupbuild: {
				detail: 'groupbuilds/groupbuild/{0}/'
			},
			participant: {
				check: 'groupbuilds/participant/check/',
				add: 'groupbuilds/groupbuild/{0}/participant/',
			}
		}
	};
	win.urlconf = $.extend(true, win.urlconf || {}, _urlconf);


	function GroupBuild(id, fields) {
		this.id = id;
		for ( var key in fields||{} ) {
			this[key] = fields[key];
		}
	}

	GroupBuild.prototype.render = function($container) {
		var endpoint = urlconf.groupbuilds.groupbuild.detail.format(this.id);
		Api.request(endpoint)
			.get()
			.done(function(data) {
				hbs.render('groupbuilds::inset', data, $container);
			});
	};

	GroupBuild.prototype.showParticipantPopup = function(topic, errors) {
		var self = this;
		self.topic = topic;
		var context = {build: self, topic: topic, errors: errors}
		hbs.render('groupbuilds::participant', context).done(function(html) {
			var _dialog = $('<div id="add-participant"></div>').html(html);
			_dialog.dialog({
				autoOpen: true,
				modal: true,
				draggable: false,
				resizable: false,
				width: 400
			});
			// set the translation dependent options
			_dialog.dialog('option', {
				title: dialogTranslations.title,
				buttons: [
				{
					text: dialogTranslations.btnSubmit,
					class: 'ui-priority-primary',
					click: function() {
						var data = $(this).find('form').serializeObject();
						self.submitParticipant(data);
					}
				}, {
					text: dialogTranslations.btnCancel,
					class: 'ui-priority-secondary',
					click: function() {$(this).dialog("destroy");}
				}]
			});
		});
	};

	GroupBuild.prototype.submitParticipant = function(data) {
		var self = this;
		var endpoint = urlconf.groupbuilds.participant.add.format(self.id);
		Api.request(endpoint, data)
			.post()
			.done(function(response) {
				$('#add-participant').dialog('destroy');
			}, function(response) {
				// error handler
				if (response.status === 400) {
					// render errors
					var context = {
						build: self,
						topic_id: self.topic,
						errors: JSON.parse(response.responseText)
					};
					hbs.render('groupbuilds::participant', context, $('#add-participant'));
				}
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
			// check if we're on the meta refresh page, if so, set a cookie with the topic id
			var cookieName = 'createdtopicid';
			var refresh = $('meta[http-equiv="refresh"]');
			if (refresh.length) {
				var url = $.url(refresh.attr('content').split('; ')[1]);
				setCookie(cookieName, url.param('t'), 1 / 24); // expires after 1 hour
			} else {
				var endpoint = urlconf.groupbuilds.participant.check;
				var requestData = {
					'forum_id': $referrer.param('f'),
					'topic_id': $.url().param('t') || getCookie(cookieName)
				}
				Api.request(endpoint, requestData).get().done(function(response) {
					// groupbuild and topic keys are only present if it's just created
					if (response.topic_created) {
						build = new GroupBuild(response.groupbuild.id, response.groupbuild);
						build.showParticipantPopup(response.topic);
						deleteCookie(cookieName);
					}
				});
			}
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
