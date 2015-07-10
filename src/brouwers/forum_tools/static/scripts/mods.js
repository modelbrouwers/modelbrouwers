var urlconf = urlconf || {};

jQuery(document).ready(function() {
	urlconf = jQuery.extend(true, urlconf, {
		ou: {
			so: '/ou/so/',
			ous: '/ou/ous/'
		},

		forum_tools: {
			mods: {
				get_sharing_perms: '/forum_tools/mods/get_sharing_perms/'
			}
		}
	});

	jQuery('#popup').dialog({
		autoOpen: false,
		draggable: true,
		//dialogClass: "",
		height: 300,
		width: 400,
		modal: false,
		resizable: true,
		title: "Online gebruikers",
		buttons: {
			Sluiten: function() {
				jQuery(this).dialog("close");
			}
		}
	});

	jQuery.get(urlconf.ou.ous, function(response){
		if (response != '0'){
			jQuery('#popup').html(response);
			jQuery('#popup').dialog('open');
		}
	});

	jQuery.get('/forum_tools/mods/get_data/', function(json){
		if (json.open_reports > 0){
			html = '&nbsp;<span id=\"open_reports\">('+json.text_reports+')</span>';
			jQuery('#pageheader p.linkmcp a').after(html);
		}
	});

	// retrieve sharing settings
	var user_ids = [];
	jQuery('span.sharing').each(function(i, e){
		user_id = jQuery(e).data('posterid');
		user_ids.push(user_id);
	});
	var ids = user_ids.join(",");
	if (ids){
		jQuery.get(
			urlconf.forum_tools.mods.get_sharing_perms,
			{'poster_ids': ids},
			function(json_response){
				jQuery.each(json_response, function(poster_id, html){
					jQuery('span#sharing_' + poster_id).html(html);
				});
			});
	}
});
