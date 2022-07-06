/**
 * Main entry point for the JS 'app' integrated in the phpBB3 board.
 *
 * Essentially, all 'apps' are globals that need to run on every page. Each
 * 'app' can detect if it needs to run or not.
 */
import "@babel/polyfill";

import AlbumsApp from "./forum/albums";
import ForumToolsApp from "./forum/forum-tools";
import GroupBuildsApp from "./forum/group-builds";
import "./forum/announcement";

AlbumsApp.init();
ForumToolsApp.init();
GroupBuildsApp.init();
