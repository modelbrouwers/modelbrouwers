// TODO: find a way to fetch/register/render partials
(function (doc, win, $, hbs) {
	'use strict';

	var hbsHelpers = [];
	var _urlconf = {
		templates: '/templates/{0}/{1}/'
	};
	win.urlconf = $.extend(true, win.urlconf || {}, _urlconf);


	function _loadTemplate(app, name){
		// keep the templates in an object
		hbs.templates = hbs.templates || {};

		var deferred = Q.defer();
		var tplName = '{0}::{1}'.format(app, name);

		// check the local cache first
		if (hbs.templates[tplName] !== undefined) {
			deferred.resolve(hbs.templates[tplName]);
		} else { // fetch from the server
			var tplUrl = win.urlconf.templates.format(app, name);
			$.get(tplUrl, function(tpl) {
				hbs.templates[tplName] = hbs.compile(tpl);
				deferred.resolve(hbs.templates[tplName]);
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
	var render = renderTemplate;
	if(hbs.renderTemplate) {
		console.warn('Warning: overwriting renderTemplate');
	}
	hbs.renderTemplate = renderTemplate;
	hbs.render = render;



	/**
	 *	Handlebars helpers
	 */
	var _yesno = function(bool, options) {
		var _defaults = {
			yes: '<span class="fa fa-check"></span>',
			no: '<span class="fa fa-times"></span>'
		};
		var hash = $.extend(_defaults, options.hash);
		var result;

		if (hbs.Utils.isFunction(bool)) {
			bool = bool.call(this);
		}

		if (!bool || hbs.Utils.isEmpty(bool)) {
			result = hash.no;
		} else {
			result = hash.yes;
		}
		if (hbs.Utils.isFunction(result)) {
			result = result.call(this);
		}
		return new hbs.SafeString(result);
	};
	hbsHelpers.push({name: 'yesno', fn: _yesno});

	var _isEven = function(number, options) {
		if((number % 2) === 0) {
			return options.fn(this);
		} else {
			return options.inverse(this);
		}
	};
	hbsHelpers.push({name: 'if_even', fn: _isEven});

	var _add = function(number, number2, options) {
		return number+number2;
	};
	hbsHelpers.push({name: 'add', fn: _add});


	/**
	 * Register the helpers
	 */
	for (var i=0; i<hbsHelpers.length; i++) {
		var helper = hbsHelpers[i];
		hbs.registerHelper(helper.name, helper.fn);
	}

	// shorter
	win.hbs = hbs;
} (document, window, jQuery, Handlebars));
