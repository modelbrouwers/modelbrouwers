var urlconf = urlconf || {};

(function(win, $, Q, hbs) {
	var _urlconf = {
		groupbuilds: {
			groupbuild: {
				detail: 'groupbuilds/groupbuild/{0}/'
			}
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

	// get the page insets and render
	$(function() {
		var gb;
		$('div.gb-inset').each(function() {
			gb = new GroupBuild($(this).data('id'));
			gb.render($(this));
		});
	});

}(window, jQuery, Q, Handlebars));
