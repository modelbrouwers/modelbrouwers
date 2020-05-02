$(document).ready(function(){
    $('#password-change-dialog').dialog({
		autoOpen: false,
		draggable: false,
		width: 600,
		modal: true,
		title: trans_change_password,
		buttons: [{
		    text: trans_confirm,
		    click: function(){
		        $.post(
		            $('#form-password').attr("action"),
		            $('#form-password').serialize(),
		            function (response){
		                obj = JSON.parse(response);
		                if(obj.success){
		                    add_message(obj.msg);
		                    $('#password-change-dialog').dialog("close");
		                } else {
		                    $('#password-change-dialog').html(obj.html);
		                }
		            }
		        );
		    }}, {
		    text: trans_cancel,
		    click: function() {
		        $(this).dialog("close");
		    }
		}]
	});
	$('#change-password-link').click(function(){
	    $('#password-change-dialog').dialog("open");
	    return false;
	});
});

function add_message(msg){
    m = '<li class=\"{{ class }}\">{{ text }}</li>';
    m = m.replace("{{ class }}", msg.tag);
    m = m.replace("{{ text }}", msg.text);
    $('div#messages ul.messages').append(m);
    $('div#messages').show();
}
