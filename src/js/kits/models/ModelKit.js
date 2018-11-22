"use strict";

import { Model } from "../../ponyjs/models.js";

class ModelKit extends Model("ModelKit", {
    Meta: {
        app_label: "kits",
        endpoints: {
            list: "kits/kit/",
            detail: "kits/kit/:id/"
        }
    }
}) {
    toString() {
        return "ModelKit: {0}".format(this.title);
    }
}

export default ModelKit;
