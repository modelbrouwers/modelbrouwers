"use strict";

import $ from "jquery";
import URI from "urijs";
import urlconf from "./urlconf";

import { TopicConsumer } from "../data/topic";

const conf = {
    forum_id_key: "f",
    topic_id_key: "t",
    selectors: {
        new_post: "a.new-post"
    }
};

export default class App {
    static init() {
        this.pingServer();
        this.initDeadTopics();
        this.syncUnreadPosts();
        this.initPostPermissions();
    }

    static pingServer() {
        // ping the Django server, ignore exceptions
        $.get(urlconf.ou.so);
    }

    static initDeadTopics() {
        const consumer = new TopicConsumer();

        const test_url = function(e) {
            e.preventDefault();
            var a = $(this);
            var topic_id = a.data("topic-id");

            consumer
                .retrieve(topic_id)
                .then(data => {
                    if (!data.is_dead) {
                        window.location = a.attr("href");
                    } else {
                        $("body").css("overflow-y", "hidden");
                        $("#blanket, #dead_topic").show();
                        $("#message_topic_dead").text(data.text_dead);
                    }
                })
                .catch(console.error);

            return false;
        };

        const hideOverlayDeadTopics = () => {
            $("div#blanket").hide();
            $("div#dead_topic").hide();
            $("body").css("overflow-y", "auto");
            return false;
        };

        // dead-topics - bind clicks on reply buttons
        $(conf.selectors.new_post).click(test_url);
        $("a#close_message").click(hideOverlayDeadTopics);
    }

    static syncUnreadPosts() {
        const syncNewPostsIndicators = response => {
            $.each(response, function(key, value) {
                var source = $("#" + key);
                var cls = source.attr("class");
                var title = source.attr("title");
                $.each(value, function(key, value) {
                    $("#" + value)
                        .attr("class", cls)
                        .attr("title", title);
                });
            });
        };

        // sync 'oranje briefjes'
        $.get(urlconf.forum_tools.sync_data, syncNewPostsIndicators);
    }

    static initPostPermissions() {
        // new-topic, new-reply buttons hiding
        // parse the current page URL for the forum_id
        var forum = URI().search(true)[conf.forum_id_key];
        if (forum !== undefined) {
            $.get(urlconf.forum_tools.get_post_perm, { forum: forum }, function(
                json
            ) {
                let restrictions = json.restrictions;
                if ($.inArray("T", restrictions) > -1) {
                    $("a.new-topic").remove();
                }
                if ($.inArray("T", restrictions) > -1) {
                    $("a.new-reply").remove();
                }
            });
        }

        // if we're on a viewtopic page, check if the buttons should be visible
        var url = URI();
        if (url.filename() === "viewtopic.php") {
            var forum_id = parseInt(url.search(true)[conf.forum_id_key], 10);
            $.getJSON(urlconf.forum_tools.get_build_report_forums, function(
                json
            ) {
                if (json.forum_ids.indexOf(forum_id) > -1) {
                    // good to go!
                    $("#add-build-report button").text(json.text_build_report);
                    $("#nominate-build button").text(json.text_nominate);
                    $("#add-build-report, #nominate-build").show();
                }
            });
        }
    }
}
