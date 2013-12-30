
$(function(){
	$('.voteable').closest('li.project').each(function(){
		var scope = $(this).closest('div.category').find('input.category').attr('name');
		$(this).draggable({
			containment: $(this).closest('div.category'),
			revert: 'invalid',
			revertDuration: 100,
			cursorAt: {
				bottom: 0,
				right: 0
			},
			scope: scope,
			scrollSensitivity: 100,
			drag: checkScrollTop,
			stop: function(event, ui) {
				$('body').stop(true);
			}
		});
	});

	$('div.vote').each(function(){
		var scope = $(this).closest('div.category').find('input.category').attr('name');
		var accept = 'li.project';
		var votes = $(this).find('ul.vote-accept li.project.dropped');
		if(votes.length) {
			accept = votes;
		}

		$(this).droppable({
			accept: accept,
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
			},
			scope: scope
		});
	});

	$('a.reset').click(function(event){
		event.preventDefault();
		var container = $(this).closest('div.category');
		var voteDiv = $(this).closest('.vote');
		var destClass = voteDiv.data('input-class');
		var projectList = container.find('ul.projects-list');

		container.find('input.'+destClass).val('');
		voteDiv.find('ul.vote-accept li').appendTo(projectList);
		projectList.find('.dropped').removeClass('dropped');
		// let it accept all projects
		voteDiv.droppable('option', 'accept', 'li.project');
		return false;
	})
});

function setVote(projectId, droppable){
	var destClass = droppable.data('inputClass');
	// set the value
	var destination = droppable.closest('div.vote-blocks').siblings('input.'+destClass);
	destination.val(projectId);

	// remove old votes with same value
	destination.siblings('input[value="'+projectId+'"].project').val('');
}

function checkScrollTop(event, ui) {
	var voteBlocks = $(this).closest('div.category');
	var offsetVoteBlocks = voteBlocks.offset().top;
	var bodyScrollTop = $('body').scrollTop();

	if(bodyScrollTop - offsetVoteBlocks > 100) {
		$('body').animate({scrollTop: offsetVoteBlocks}, 200);
	}
}