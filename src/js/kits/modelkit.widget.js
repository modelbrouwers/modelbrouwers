let conf = {
    add_modal: "#add-kit-modal",
};

const initModal = node => {
    // bring up modal when button is clicked
    const selector = `[data-target="${conf.add_modal}"]`;
    $(node).on("click", selector, event => {
        event.preventDefault();
        $(conf.add_modal).modal("toggle");
        return false;
    });
};

export { initModal };
