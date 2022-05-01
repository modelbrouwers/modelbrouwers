const fetchAndDisplayAnnouncements = () => {
    window
        .fetch("/utils/get-announcement/", { credentials: "include" })
        .then(response => response.json())
        .then(response => {
            if (!response.html) return;
            const node = document.getElementById("announcement");
            if (!node) return;
            node.innerHTML = response.html;
        });
};

document.addEventListener("DOMContentLoaded", () => {
    fetchAndDisplayAnnouncements();
});
