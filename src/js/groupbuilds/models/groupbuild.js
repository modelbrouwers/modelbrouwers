'use strict';

import URI from 'URIjs';

import Api from 'scripts/api';
import Model from 'scripts/model';
import Handlebars from 'general/js/hbs-pony';
import urlconf from '../forum/urlconf';

import 'jquery-ui';
import 'scripts/jquery.serializeObject';


class GroupBuild extends Model {
	static Meta() {
		return {
			app_label: 'groupbuilds',
			// ordering: ['id'],
			endpoints: {
				list: 'groupbuilds/groupbuild/',
				detail: 'groupbuilds/groupbuild/:id/'
			}
		}
	}

	toString() {
		return 'Groupbuild {0}'.format(this.theme);
	}

	render(container) {
		Handlebars.render('groupbuilds::inset', this, container).done();
	}

	showParticipantPopup(topic, errors) {
		var self = this;
		self.topic = topic;
		let context = {
			build: this,
			topic: topic,
			errors: errors
		};

		Handlebars
			.render('groupbuilds::participant', context)
			.done(html => {
				let _dialog = $('<div id="add-participant"></div>').html(html);
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
							let data = $(this).find('form').serializeObject();
							self.submitParticipant(data);
						}
					}, {
						text: dialogTranslations.btnCancel,
						class: 'ui-priority-secondary',
						click: function() {
							$(this).dialog("destroy");
						}
					}]
				});
			});
	}

	submitParticipant(data) {
		let self = this;
		let endpoint = urlconf.groupbuilds.participant.add.format(self.id);
		let $dialog = $('#add-participant');
		Api.request(endpoint, data)
			.post()
			.done(
				response => $dialog.dialog('destroy'),
				response => {
					// error handler
					if (response.status === 400) {
						// render errors
						let context = {
							build: self,
							topic_id: self.topic,
							errors: JSON.parse(response.responseText)
						};
						Handlebars.render('groupbuilds::participant', context, $dialog);
					}
			});
	}
}

export { GroupBuild };