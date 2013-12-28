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

			setVote(ui.draggable.data('id'), $(this));
		},
		out: function(event, ui){
	        $(this).droppable('option', 'accept', 'li.project');
        }
		// TODO: scope
	});
});

function setVote(projectId, droppable){
	var destClass;
	if(droppable.hasClass('first')){
		destClass = 'project1';
	} else if(droppable.hasClass('second')) {
		destClass = 'project2';
	} else if(droppable.hasClass('third')) {
		destClass = 'project3';
	}

	// set the value
	droppable.closest('div.vote-blocks').siblings('input.'+destClass).val(projectId);
}