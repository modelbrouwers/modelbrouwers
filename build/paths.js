/** Name of the sources directory */
var sourcesRoot = 'src/';

/** Name of the static (source) directory */
var staticRoot = sourcesRoot + 'static/';


/**
 * Application path configuration for use in frontend scripts
 */
module.exports = {
    // Path to the sass (sources) directory
    sassSrc: sourcesRoot + 'sass/**/*.scss',

    // Path to the (transpiled) css directory
    cssDir: staticRoot + 'css/'
};
