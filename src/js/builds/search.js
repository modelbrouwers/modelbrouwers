import 'jquery';
import 'typeahead.js';

const search = 'input[name="q"]';

export default function initSearch() {
  let $search = $(search);
  if (!$search.length) {
    return;
  }

  $search.typeahead(
    {
      minLength: 2,
      highlight: true,
    },
    {
      async: true,
      source: (query, sync, async) => {
        $.getJSON($search.data('url'), {q: $search.val()}, data => async(data));
      },
      limit: 100,
      display: 'display',
    },
  );

  $search.on('typeahead:select', (event, suggestion) => (window.location = suggestion.url));
}
