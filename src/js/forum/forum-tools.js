import $ from 'jquery';
import {createRoot} from 'react-dom/client';
import {IntlProvider} from 'react-intl';
import URI from 'urijs';

import {getTopic} from '@/data/topic';
import {getIntlProviderProps} from '@/i18n.js';

import DeadTopicModal from './DeadTopicModal';
import urlconf from './urlconf';

const conf = {
  forum_id_key: 'f',
  topic_id_key: 't',
};

export default class App {
  static init() {
    this.initDeadTopics();
    this.initPostPermissions();
  }

  static async initDeadTopics() {
    // dead-topics - bind clicks on reply buttons
    const rootNode = document.getElementById('dead_topic');
    if (!rootNode) return;
    const inltPropsPromise = getIntlProviderProps();

    const {postReplyUrl} = rootNode.dataset;

    let reactRoot = createRoot(rootNode);
    const resetRoot = () => {
      reactRoot.unmount();
      reactRoot = createRoot(rootNode);
    };

    const addNewPostLinks = document.querySelectorAll('a.new-post');
    for (const link of addNewPostLinks) {
      link.addEventListener('click', async event => {
        event.preventDefault();
        const anchor = event.currentTarget;
        const {topicId} = anchor.dataset;

        // check if it's okay or not
        const {is_dead, text_dead} = await getTopic(parseInt(topicId));
        if (!is_dead) {
          window.location = anchor.href;
          return;
        }

        const intlProps = await inltPropsPromise;
        reactRoot.render(
          <IntlProvider {...intlProps}>
            <DeadTopicModal
              message={text_dead}
              replyTopicUrl={postReplyUrl}
              onRequestClose={resetRoot}
            />
          </IntlProvider>,
        );
      });
    }
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
