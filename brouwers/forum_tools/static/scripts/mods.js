$(document).ready(function(){
    $('#popup').dialog({
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
		        $(this).dialog("close");
		    }
		}
    });
    
    $.get('/ou/ous/', function(response){
        if (response != '0'){
            $('#popup').html(response);
            $('#popup').dialog('open');
        }
    });
    
    $.get('/forum_tools/mods/get_data/', function(json){
        if (json.open_reports > 0){
            html = '&nbsp;<span id=\"open_reports\">('+json.text_reports+')</span>';
            $('#pageheader p.linkmcp a').after(html);
        }
    });

    // retrieve sharing settings
    var user_ids = [];
    $('span.sharing').each(function(i, e){
        user_id = $(e).data('posterid');
        user_ids.push(user_id);
    });
    var ids = user_ids.join(",");
    $.get(
        '/forum_tools/mods/get_sharing_perms/',
        {'poster_ids': ids},
        function(json_response){
            $.each(json_response, function(poster_id, html){
                $('span#sharing_' + poster_id).html(html);
            });
        });
});
