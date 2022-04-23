var urlconf = urlconf || {};

const get = url => {
    return window
        .fetch(url, { credentials: "include" })
        .then(response => response.json());
};

const injectModInformation = () => {
    get("/forum_tools/mods/get_data/").then(json => {
        if (json.open_reports <= 0) return;
        const sibling = document.querySelector("#pageheader p.linkmcp a");
        const html = `&nbsp;<span id="open_reports">${
            json.text_reports
        }</span>`;
        sibling.insertAdjacentHTML("beforeend", html);
    });
};

const injectUserSharingSettings = () => {
    const userIds = [];
    const sharingNodes = document.querySelectorAll("span.sharing");
    sharingNodes.forEach(node => {
        const userId = node.dataset.posterid;
        userIds.push(userId);
    });
    if (!userIds.length) return;

    const query = new URLSearchParams({
        poster_ids: userIds.join(",")
    });
    const url = `/forum_tools/mods/get_sharing_perms/?${query}`;
    get(url).then(json => {
        Object.entries(json).map(([user_id, html]) => {
            const node = document.querySelector(`span#sharing_${user_id}`);
            node.innerHTML = html;
        });
    });
};

document.addEventListener("DOMContentLoaded", () => {
    urlconf = Object.assign(urlconf, {
        ou: {
            so: "/ou/so/",
            ous: "/ou/ous/"
        }
    });
    injectModInformation();
    injectUserSharingSettings();
});
