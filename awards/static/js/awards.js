$(function(){
	$('.voteable').closest('li.project').draggable({
		// helper: 'clone',
		revert: 'invalid'
	});

	$('div.vote').droppable({
		accept: 'li.project',
		hoverClass: 'highlight-border',
		drop: function(event, ui){
			ui.draggable.addClass('dropped');
			ui.draggable.appendTo($(this).find('.vote-accept'));
			ui.draggable.css('top', '0').css('left', '0');
			// prevent other elements to be dropped
			$(this).droppable('option', 'accept', ui.draggable);
		},
		out: function(event, ui){
	        $(this).droppable('option', 'accept', 'li.project');
        }
		// TODO: scope
	});
});