/** Name of the sources directory */
var sourcesRoot = 'src/';

/** Name of the static (source) directory */
var staticRoot = sourcesRoot + 'static/';

var jsRoot = sourcesRoot + 'js/';


/**
 * Application path configuration for use in frontend scripts
 */
module.exports = {
    // Path to the sass (sources) directory
    sassSrc: sourcesRoot + 'sass/**/*.scss',

    // Path to the (transpiled) css directory
    cssDir: staticRoot + 'css/',

    jsSrc: jsRoot + '**/*.js',
    jsEntry: jsRoot + 'index.js',
    jsDir: staticRoot + 'js/'
};
