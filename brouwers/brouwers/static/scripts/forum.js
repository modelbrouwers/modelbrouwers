var rotation = 0;
var chat_opened = false;
$(document).ready(function(){
    $.get('/ou/so/');
    
    // dead topics
    $('a#close_message').click(function(){
		$('div#blanket').hide();
		$('div#dead_topic').hide();
		$('body').css('overflow-y','auto');
		return false;
	});
	
	// oranje briefjes syncen
	$.get('/forum_tools/get_sync_data/', function(response){
	    $.each(response, function(key, value){
	        var source = $('#'+key);
	        var cls = source.attr('class');
	        var title = source.attr('title');
	        $.each(value, function(key, value){
	            $('#'+value).attr('class', cls).attr('title', title);
	        });
	    });
	});
	
	// chat in een popup window
	$('#chat-window').dialog({
		autoOpen: false,
		//draggable: true,
		dialogClass: "chat-dialog",
		height: $(window).height()*0.75,
		width: $(window).width()/2,
		modal: false,
		resizable: true,
		// fixed position css
		create: function(event){
		    $(event.target).parent().css('position', 'fixed');
		},
		close: function(event, ui){
		    $(this).html('');
		    chat_opened=false;
		},
		open: function(event, ui){
		    $(event.target).parent().css('top', 'auto');
		    $(event.target).parent().css('left', 'auto');
		    $(event.target).parent().css('bottom', '0');
		    $(event.target).parent().css('right', '0');
		    chat_opened=true;
		}
    });
    
    $('#open-chat').click(function(e){
        e.preventDefault();
        if (!chat_opened){
            $.get('/forum_tools/get_chat/', function(json){
                $('#chat-window').html(json.html);
                // title zetten met extra gegevens
                $('#chat-window').dialog("option", "title", json.title);
                $('#chat-window').dialog('open');
            });
        }
        return false;
    });
    
    // als de chat geopend is, zal die popup weg zijn als je op een link klikt
    // forceer dus het openen vna links in een nieuw venster/tab
    $('a').click(function(){
        if(chat_opened){
            window.open($(this).attr('href'));
            return false;
        }
    });
});

function rotate(){
    if (rotation < 180){
        rotation += 1;
        rotateScreen(rotation);
    }
}

function rotateScreen(degrees){
    $('body').css('-webkit-transform', 'rotate('+degrees+'deg)');
    $('body').css('-moz-transform', 'rotate('+degrees+'deg)');
    $('body').css('-ms-transform', 'rotate('+degrees+'deg)');
    $('body').css('-o-transform', 'rotate('+degrees+'deg)');
    $('body').css('transform', 'rotate('+degrees+'deg)');
}

// dead topics
function test_url(topic_id, a){
	$.get('./ajax/topic_dead.php', {t: topic_id}, function(data){
		if (data == ""){
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
