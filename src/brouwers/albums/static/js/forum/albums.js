(function($, Q, hbs, undefined) {

    var conf = {
        selectors: {
            root: 'body.forum'
        }
    };

    var renderSidebar = function() {

        Album.objects.all().then(function(albums) {
            var ctx = {
                albums: albums
            };
            hbs.render('albums::forum-sidebar', ctx).done(function(html) {
                $('body').append(html);
            });
        });


    };


    $(function() {
        // check if we're in posting mode
        if ($('textarea[name="message"]').length == 1) {
            renderSidebar();
        }

        $(conf.selectors.root).on('click', '[data-open], [data-close]', function() {
            var selector = $(this).data('open') || $(this).data('close');
            $(selector).toggleClass('open closed');
        });
    });





    $.fn.extend({
      insertAtCaret: function(myValue){
      var obj;
      if( typeof this[0].name !='undefined' ) obj = this[0];
      else obj = this;

      if ($.browser.msie) {
        obj.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
        obj.focus();
        }
      else if ($.browser.mozilla || $.browser.webkit) {
        var startPos = obj.selectionStart;
        var endPos = obj.selectionEnd;
        var scrollTop = obj.scrollTop;
        obj.value = obj.value.substring(0, startPos)+myValue+obj.value.substring(endPos,obj.value.length);
        obj.focus();
        obj.selectionStart = startPos + myValue.length;
        obj.selectionEnd = startPos + myValue.length;
        obj.scrollTop = scrollTop;
      } else {
        obj.value += myValue;
        obj.focus();
       }
     }
    });

}) (window.jQuery, Q, Handlebars);
