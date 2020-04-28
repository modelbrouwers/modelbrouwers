"use strict";

var gulp = require("gulp");
var sass = require("gulp-sass");
var sourcemaps = require("gulp-sourcemaps");
var autoprefixer = require("autoprefixer");
var paths = require("./build/paths");
var postcss = require('gulp-postcss');
var bourbon = require("bourbon");
var neat = require("bourbon-neat");
var compass = require("compass-importer");

const sassOptions = {
    outputStyle: "minified",
    importer: compass,
    // Includes bourbon neat
    includePaths: bourbon.includePaths.concat(neat.includePaths),
};

var plugins = [
    autoprefixer(),
];

/**
 * Sass task
 * Run using "gulp sass"
 * Searches for sass files in paths.sassSrc
 * Compiles sass to css
 * Includes bourbon neat
 * Auto prefixes css
 * Writes css to paths.cssDir
 */
function scss() {
    return gulp.src(paths.sassSrc)
        .pipe(sourcemaps.init())
        .pipe(sass(sassOptions).on("error", sass.logError))
        .pipe(postcss(plugins))
        .pipe(sourcemaps.write("./maps"))
        .pipe(gulp.dest(paths.cssDir));
};

function watchSCSS() {
    scss()
    gulp.watch(paths.sassWatchSrc, scss);
};

gulp.task('sass', scss);
gulp.task('scss', scss);
gulp.task("watch-scss", watchSCSS);

gulp.task("default", watchSCSS);
