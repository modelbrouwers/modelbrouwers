const get = async url => {
  return window.fetch(url, {credentials: 'include'}).then(response => response.json());
};

const injectModInformation = () => {
  get('/forum_tools/mods/get_data/').then(json => {
    if (json.open_reports <= 0) return;
    const sibling = document.querySelector('#pageheader p.linkmcp a');
    const html = `&nbsp;<span id="open_reports">${json.text_reports}</span>`;
    sibling.insertAdjacentHTML('beforeend', html);
  });
};

document.addEventListener('DOMContentLoaded', () => {
  injectModInformation();
});
