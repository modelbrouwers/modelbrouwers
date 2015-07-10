jQuery(function($) {
	var chat_opened = false;
	var chat_moved = false;

	// chat in een popup window
	$('#chat-window').dialog({
		autoOpen: false,
		draggable: true,
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
			init_popup();
		},
		resizeStop: function(event, ui){
			// reset de positie
			$(event.target).parent().css('position', 'fixed');
			if(!chat_moved){
				$(event.target).parent().css('top', 'auto');
				$(event.target).parent().css('left', 'auto');
				$(event.target).parent().css('bottom', '0');
				$(event.target).parent().css('right', '0');
			}
		},
		dragStart: function(event, ui){
			// fixen van position
			$(event.target).parent().css('position', 'fixed');
			$(event.target).parent().css('top', 'auto');
			$(event.target).parent().css('left', 'auto');
			$(event.target).parent().css('bottom', 'auto');
			$(event.target).parent().css('right', 'auto');
			chat_moved = true;
		}
	});

	$('#open-chat').click(function(e){
		e.preventDefault();
		if (!chat_opened){
			$.get('/forum_tools/get_chat/', function(json){
				$('#chat-window').html(json.html);
				title = json.title;
				title += "&nbsp;&bull; <a href=\""+$('#open-chat').attr('href')+"\" target=\"_blank\">FAQ</a>";
				applyHtmlToDialog($('#chat-window').dialog(), title);
				$('#chat-window').dialog('open');
			});
		}
		else{
			$('#chat-window').toggle();
		}
		return false;
	});

	// als de chat geopend is, zal die popup weg zijn als je op een link klikt
	// forceer dus het openen vna links in een nieuw venster/tab
	$('body').on('click', '#boardcontent a', function(){
		if(chat_opened){
			// get the content through an ajax call and replace the original content
			var url = $(this).attr('href');
			$.get(url, function(response){
				c = $(response);
				$('#boardcontent').html(c.find('#boardcontent').html());

				var title = c.find('#page-title').text();
				document.title = title;
				$(document).scrollTop(0);

				if(history.pushState){
					history.pushState({"id": history.length+1}, title, url);
				}
			});
			return false;
		}
	});

	$('a').not('#boardcontent a').click(function(){
		if(chat_opened){
			html = '<p>De chat staat nog open. Indien je de pagina niet in een niew tabblad/venster opent, zal je chatsessie niet meer actief zijn.</p>';
			html += '<br /><p>Je kan de pagina in een nieuw venster of tabblad openen, of de chat sluiten en de pagina in dit venster openen.</p>';
			$('#popup').data('href', $(this).attr('href'));
			$('#popup').html(html);
			$('#popup').dialog('open');
			return false;
		}
	});

	$('body').on('click', '.ui-dialog-titlebar', function(){
		$(this).siblings('#chat-window').toggle();
	});

	function applyHtmlToDialog(dialog, htmlTitle) {
		dialog.data("uiDialog")._title = function (title) {
		title.html(this.options.title); };
		dialog.dialog('option', 'title', htmlTitle);
	}

	function init_popup() {
		$('#popup').dialog({
			autoOpen: false,
			draggable: false,
			height: 'auto',
			width: '400px',
			modal: true,
			resizable: false,
			title: 'Opgepast!',
			buttons: {
				'Nieuw venster/tabblad': function(){
					window.open($(this).data('href'));
					$(this).dialog('close');
				},
				'Chat sluiten': function(){
					$(this).dialog('close');
					window.location = $(this).data('href');
				},
				'Annuleren': function(){
					$(this).dialog('close');
				}
			}
		});
	}
});
