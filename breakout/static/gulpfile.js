var postcss = require('gulp-postcss');
var gulp = require('gulp');
var autoprefixer = require('autoprefixer');
var cssnano = require('cssnano');
var sass = require('gulp-sass');
var rucksack = require('rucksack-css');
var sourcemaps = require('gulp-sourcemaps');
 
gulp.task('css', function () {
    var plugins = [
        rucksack(),
        autoprefixer(),
        cssnano(),

    ];
    // return gulp.src('./src/*.scss')
    return gulp.src('./sass/**/*.scss')
	.pipe(sourcemaps.init())
        .pipe(sass())
        .pipe(postcss(plugins))
    //     .pipe(gulp.dest('./dest'));
	.pipe(sourcemaps.write('./css'))
        .pipe(gulp.dest('./css'));
});

gulp.task('watch:css', function() {
    gulp.watch('./sass/**/*scss', gulp.series('css'));
});
