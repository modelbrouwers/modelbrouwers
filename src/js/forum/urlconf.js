const urlconf = {
    ou: {
        so: "/ou/so/"
    },

    forum_tools: {
        sync_data: "/forum_tools/get_sync_data/",
        get_build_report_forums: "/forum_tools/get_build_report_forums/",
        get_post_perm: "/forum_tools/get_post_perm/",
        check_topic_dead: "forum_tools/topic/{0}/",

        mods: {
            get_sharing_perms: "/forum_tools/mods/get_sharing_perms/"
        }
    },

    groupbuilds: {
        participant: {
            check: "groupbuilds/participant/check/",
            add: "groupbuilds/groupbuild/{0}/participant/",
            setFinished: "groupbuilds/participant/{0}/"
        }
    }
};

export default urlconf;
