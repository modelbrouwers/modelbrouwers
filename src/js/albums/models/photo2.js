/**
 * This uses the proper PonyJS models. photo.js is legacy.
 */
"use strict";

import { Model } from "../../ponyjs/models.js";

class Photo extends Model("Photo", {
    Meta: {
        app_label: "albums"
    }
}) {
    toString() {
        return `Photo by ${this.user.username}`;
    }
}

export default Photo;
