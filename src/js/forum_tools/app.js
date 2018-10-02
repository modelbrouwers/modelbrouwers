'use strict';

import $ from 'jquery';
import URI from 'urijs';
import Api from '../scripts/api';


let conf = {
    forum_id_key: 'f',
    topic_id_key: 't',
    selectors: {
        new_post: 'a.new-post'
    }
};

let urlconf = {
    ou: {
        so: '/ou/so/'
    },

    forum_tools: {
        sync_data: '/forum_tools/get_sync_data/',
        get_build_report_forums: '/forum_tools/get_build_report_forums/',
        get_post_perm: '/forum_tools/get_post_perm/',
        check_topic_dead: 'forum_tools/topic/{0}/',

        mods: {
            get_sharing_perms: '/forum_tools/mods/get_sharing_perms/'
        }
    }
};


$(function() {
    // ping the Django server, ignore exceptions
    $.get(urlconf.ou.so);

    // dead-topics - bind clicks on reply buttons
    $(conf.selectors.new_post).click(test_url);
    $('a#close_message').click(hideOverlayDeadTopics);

    // sync 'oranje briefjes'
    // oranje briefjes syncen
    $.get(urlconf.forum_tools.sync_data, syncNewPostsIndicators);

    // new-topic, new-reply buttons hiding
    // parse the current page URL for the forum_id
    var forum = URI().search(true)[conf.forum_id_key];
    if (forum !== undefined) {
        $.get(
            urlconf.forum_tools.get_post_perm,
            {'forum': forum},
            function(json) {
                let restrictions = json.restrictions;
                if ($.inArray('T', restrictions) > -1) {
                    $('a.new-topic').remove();
                }
                if ($.inArray('T', restrictions) > -1) {
                    $('a.new-reply').remove();
                }
            }
        );
    }

    // if we're on a viewtopic page, check if the buttons should be visible
    var url = URI();
    if (url.filename() === 'viewtopic.php') {
        var forum_id = parseInt(url.search(true)[conf.forum_id_key], 10);
        $.getJSON(urlconf.forum_tools.get_build_report_forums, function(json) {
            if (json.forum_ids.indexOf(forum_id) > -1) { // good to go!
                $('#add-build-report button').text(json.text_build_report);
                $('#nominate-build button').text(json.text_nominate);
                $('#add-build-report, #nominate-build').show();
            }
        });
    }
});


// dead topics
function test_url(e) {
    e.preventDefault();
    var a = $(this);
    var topic_id = a.data('topic-id');

    var endpoint = urlconf.forum_tools.check_topic_dead.format(topic_id);
    Api.request(endpoint)
        .get()
        .done(function(data) {
            if (!data.is_dead) {
                window.location = a.attr('href');
            } else {
                $('body').css('overflow-y', 'hidden');
                $('#blanket, #dead_topic').show();
                $('#message_topic_dead').text(data.text_dead);
            }
        });
    return false;
}

function hideOverlayDeadTopics() {
    $('div#blanket').hide();
    $('div#dead_topic').hide();
    $('body').css('overflow-y', 'auto');
    return false;
}

function syncNewPostsIndicators(response) {
    $.each(response, function(key, value) {
        var source = $('#' + key);
        var cls = source.attr('class');
        var title = source.attr('title');
        $.each(value, function(key, value) {
            $('#' + value).attr('class', cls).attr('title', title);
        });
    });
}
