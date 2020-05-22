import { initModal } from "../modelkit.widget";

const initAddKitModals = nodes => {
    for (const node of nodes) {
        initModal(node);
    }
};

export { initAddKitModals };
