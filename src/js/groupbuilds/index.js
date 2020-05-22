"use strict";

import "jquery";

import { GroupBuildParticipantConsumer } from "../data/group-build-participant";

const participantConsumer = new GroupBuildParticipantConsumer();

export default class Page {
    static init() {
        this.initDetails();

        $('[data-toggle="popover"]').popover();
    }

    static initDetails() {
        $('[data-toggle="finished"]').click(function(e) {
            e.preventDefault();

            const id = Number($(this).data("id"));
            const isFinished = $(this).children(".fa-ellipsis-h").length > 0;

            const indicator = $(this).find(".fa");

            participantConsumer
                .setFinished(id, !isFinished)
                .then(participant => {
                    indicator.toggleClass("fa-check fa-ellipsis-h");
                })
                .catch(console.error);
            return false;
        });
    }
}
