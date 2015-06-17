(function($, Q, hbs, undefined) {

    var conf = {
        selectors: {
            root: 'body.forum',
            photo_list: '#photo-list',
            albums_select: 'select[name="album"]',
        }
    };

    var renderSidebar = function(albums) {
        return hbs.render('albums::forum-sidebar', {albums:albums}).then(function(html) {
            $('body').append(html);
            if (albums.length === 0) {
                return null;
            }
            return albums[0];
        });
    };

    var renderAlbumPhotos = function(album) {
        if (album === null) {
            return;
        }
        var target = $(conf.selectors.photo_list);
        return album.renderPhotos('albums::forum-sidebar-photos', target);
    };

    var showSidebar = function() {
        Album.objects.all()
            .then(renderSidebar)
            .done(renderAlbumPhotos);
    };

    var onAlbumSelectChange = function(event) {
        var id = parseInt($(this).val(), 10);
        Album.objects.get({id: id}).done(renderAlbumPhotos);
    };


    $(function() {
        // check if we're in posting mode
        if ($('textarea[name="message"]').length == 1) {
            showSidebar();
        }

        $(conf.selectors.root)
            .on('click', '[data-open], [data-close]', function() {
                var selector = $(this).data('open') || $(this).data('close');
                $(selector).toggleClass('open closed');
            })
            .on('change', conf.selectors.albums_select, onAlbumSelectChange)
        ;
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
