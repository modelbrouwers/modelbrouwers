// TODO: find a way to fetch/register/render partials
(function (doc, win, $) {
	'use strict';

	var _urlconf = {
		templates: '/templates/{0}/{1}/'
	};
	win.urlconf = $.extend(true, win.urlconf || {}, _urlconf);


	function _loadTemplate(app, name){
		// keep the templates in an object
		win.Handlebars.templates = win.Handlebars.templates || {};

		var deferred = Q.defer();
		var tplName = '{0}::{1}'.format(app, name);

		// check the local cache first
		if (Handlebars.templates[tplName] !== undefined) {
			deferred.resolve(Handlebars.templates[tplName]);
		} else { // fetch from the server
			var tplUrl = win.urlconf.templates.format(app, name);
			$.get(tplUrl, function(tpl) {
				Handlebars.templates[tplName] = Handlebars.compile(tpl);
				deferred.resolve(Handlebars.templates[tplName]);
			});
		}
		return deferred.promise;
	}

	/**
	 * @param name: name of the template, in the format app::name
	 */
	function renderTemplate(name, context, $dest) {
		var bits = name.split('::');
		var _app = bits[0],
			_name = bits[1];

		return _loadTemplate(_app, _name).then(function(tpl) {
			var rendered = tpl(context || {});
			if($dest) {
				$dest.html(rendered);
			}
			return rendered;
		});
	}


	if(win.Handlebars.renderTemplate) {
		console.warn('Warning: overwriting renderTemplate');
	}
	win.Handlebars.renderTemplate = renderTemplate;

	// shorter
	win.hbs = win.Handlebars;
} (document, window, jQuery));
