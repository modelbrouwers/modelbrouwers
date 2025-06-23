'use strict';

import $ from 'jquery';
import URI from 'urijs';

import {getTopic} from '@/data/topic';

import urlconf from './urlconf';

const conf = {
  forum_id_key: 'f',
  topic_id_key: 't',
  selectors: {
    new_post: 'a.new-post',
  },
};

export default class App {
  static init() {
    this.pingServer();
    this.initDeadTopics();
    this.initPostPermissions();
  }

  static pingServer() {
    // ping the Django server, ignore exceptions
    $.get(urlconf.ou.so);
  }

  static initDeadTopics() {
    const test_url = async function (e) {
      e.preventDefault();
      var a = $(this);
      var topic_id = a.data('topic-id');

      const {is_dead, text_dead} = await getTopic(parseInt(topic_id));
      if (!is_dead) {
        window.location = a.attr('href');
      } else {
        $('body').css('overflow-y', 'hidden');
        $('#blanket, #dead_topic').show();
        $('#message_topic_dead').text(text_dead);
      }

      return false;
    };

    const hideOverlayDeadTopics = () => {
      $('div#blanket').hide();
      $('div#dead_topic').hide();
      $('body').css('overflow-y', 'auto');
      return false;
    };

    // dead-topics - bind clicks on reply buttons
    $(conf.selectors.new_post).click(test_url);
    $('a#close_message').click(hideOverlayDeadTopics);
  }

  static initPostPermissions() {
    // new-topic, new-reply buttons hiding
    // parse the current page URL for the forum_id
    var forum = URI().search(true)[conf.forum_id_key];
    if (forum !== undefined) {
      $.get(urlconf.forum_tools.get_post_perm, {forum: forum}, function (json) {
        let restrictions = json.restrictions;
        if ($.inArray('T', restrictions) > -1) {
          $('a.new-topic').remove();
        }
        if ($.inArray('T', restrictions) > -1) {
          $('a.new-reply').remove();
        }
      });
    }

    // if we're on a viewtopic page, check if the buttons should be visible
    var url = URI();
    if (url.filename() === 'viewtopic.php') {
      var forum_id = parseInt(url.search(true)[conf.forum_id_key], 10);
      $.getJSON(urlconf.forum_tools.get_build_report_forums, function (json) {
        if (json.forum_ids.indexOf(forum_id) > -1) {
          // good to go!
          $('#add-build-report button').text(json.text_build_report);
          $('#nominate-build button').text(json.text_nominate);
          $('#add-build-report, #nominate-build').show();
        }
      });
    }
  }
}
