'use strict';

import $ from 'jquery';
import URI from 'URIjs';

import { getCookie, deleteCookie, setCookie } from 'scripts/csrf';
import Api from 'scripts/api';
import { GroupBuild } from '../models/groupbuild';
import urlconf from './urlconf';


/**
 * Check if a topic was created
**/
function checkParticipantTopicCreated() {
	// check the referrer - did we come from create topic?
	let referrer = URI(document.referrer);
	let thisHost = referrer.host() == URI().host();
	let postCreated = thisHost
					 && referrer.filename() == 'posting.php'
					 && referrer.search(true).mode == 'post';

	// we're coming from the posting page, so check if the topic was created
	if ( postCreated ) {
		// check if we're on the meta refresh page, if so, set a cookie with the topic id
		let cookieName = 'createdtopicid';
		let refresh = $('meta[http-equiv="refresh"]');
		if (refresh.length) {
			let url = URI(refresh.attr('content').split('; ')[1]);
			setCookie(cookieName, url.search(true).t, 1 / 24); // expires after 1 hour
		} else {
			let endpoint = urlconf.groupbuilds.participant.check;
			let requestData = {
				'forum_id': referrer.search(true).f,
				'topic_id': URI().search(true).t || getCookie(cookieName)
			}

			if (!requestData.topic_id > 0) {
				return;
			}

			Api.request(endpoint, requestData).get()
			.done(response => {
				// groupbuild and topic keys are only present if it's just created
				if (response.topic_created && response.topic) {
					let build = new GroupBuild(response.groupbuild);
					build.showParticipantPopup(response.topic);
					deleteCookie(cookieName);
				}
			});
		}
	}
}


// jQuery initialization
$(function() {

	let gb;

	// get the page insets and render
	$('div.gb-inset').each((i, div) => {
		let inset = $(div);
		gb = GroupBuild.objects.get({id: inset.data('id')})
			.done( gb => gb.render(inset) );
	});

	checkParticipantTopicCreated();
});
