var urlconf = urlconf || {};

+(function($) {
    $(function() {
        urlconf = $.extend(true, urlconf, {
            ou: {
                so: "/ou/so/",
                ous: "/ou/ous/"
            },

            forum_tools: {
                mods: {
                    get_sharing_perms: "/forum_tools/mods/get_sharing_perms/"
                }
            }
        });

        $.get("/forum_tools/mods/get_data/", function(json) {
            if (json.open_reports > 0) {
                html =
                    '&nbsp;<span id="open_reports">(' +
                    json.text_reports +
                    ")</span>";
                $("#pageheader p.linkmcp a").after(html);
            }
        });

        // retrieve sharing settings
        var user_ids = [];
        $("span.sharing").each(function(i, e) {
            user_id = $(e).data("posterid");
            user_ids.push(user_id);
        });
        var ids = user_ids.join(",");
        if (ids) {
            $.get(
                urlconf.forum_tools.mods.get_sharing_perms,
                { poster_ids: ids },
                function(json_response) {
                    $.each(json_response, function(poster_id, html) {
                        $("span#sharing_" + poster_id).html(html);
                    });
                }
            );
        }
    });
})(window.jQuery);
