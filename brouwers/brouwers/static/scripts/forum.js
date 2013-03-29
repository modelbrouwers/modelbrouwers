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
});

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
