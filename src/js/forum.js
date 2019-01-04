/**
 * Main entry point for the JS 'app' integrated in the phpBB3 board.
 *
 * Essentially, all 'apps' are globals that need to run on every page. Each
 * 'app' can detect if it needs to run or not.
 */
import ForumToolsApp from './forum/forum-tools';
import GroupBuildsApp from './forum/group-builds';


ForumToolsApp.init();
GroupBuildsApp.init();
