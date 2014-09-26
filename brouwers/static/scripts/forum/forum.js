// global vars

var forum_id_key = 'f';
var urlconf = urlconf || {};
var _urlconf = {
	ou: {
		so: '/ou/so/'
	},

	forum_tools: {
		sync_data: '/forum_tools/get_sync_data/',
		get_build_report_forums: '/forum_tools/get_build_report_forums/',
		get_post_perm: '/forum_tools/get_post_perm/',
		check_topic_dead: './ajax/topic_dead.php', // FIXME

		mods: {
			get_sharing_perms: '/forum_tools/mods/get_sharing_perms/',
		}
	}
};


$(document).ready(function() {
	// include the full urlconf from other javascript files
	urlconf = $.extend(true, urlconf, _urlconf);

	$.get(urlconf.ou.so);

	// dead topics
	$('a#close_message').click(function(){
		$('div#blanket').hide();
		$('div#dead_topic').hide();
		$('body').css('overflow-y','auto');
		return false;
	});

	// oranje briefjes syncen
	$.get(urlconf.forum_tools.sync_data, function(response){
		$.each(response, function(key, value){
			var source = $('#'+key);
			var cls = source.attr('class');
			var title = source.attr('title');
			$.each(value, function(key, value){
				$('#'+value).attr('class', cls).attr('title', title);
			});
		});
	});


	// new-topic, new-reply buttons hiding
	// parse the current page URL for the forum_id
	var forum = $.url().param(forum_id_key);
	if (forum !== undefined){
		$.get(
			urlconf.forum_tools.get_post_perm,
			{'forum': forum},
			function(json){
				restrictions = json.restrictions;
				if ($.inArray('T', restrictions) > -1){
					$('a.new-topic').remove();
				}
				if ($.inArray('T', restrictions) > -1){
					$('a.new-reply').remove();
				}
			}
		);
	}

	// if we're on a viewtopic page, check if the buttons should be visible
	var url = $.url();
	if(url.segment(-1) == 'viewtopic.php'){
		var forum_id = parseInt(url.param('f'), 10);
		$.getJSON(urlconf.forum_tools.get_build_report_forums, function(json){
			if(json.forum_ids.indexOf(forum_id) > -1){ // good to go!
				$('#add-build-report button').text(json.text_build_report);
				$('#nominate-build button').text(json.text_nominate);
				$('#add-build-report, #nominate-build').show();
			}
		});
	}

	// dead topics
	function test_url(topic_id, a){
		$.get(urlconf.forum_tools.check_topic_dead, {t: topic_id}, function(data){
			if (data === "") {
				var url = "" + a.attr('href');
				window.location=url;
			} else {
				$('body').css('overflow-y','hidden');
				$('div#blanket').show();
				$('div#dead_topic').show();
				$('div#message_topic_dead').html(data);
			}
		});
	}
});
