module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    paths: {
      bower: 'bower_components/',
      dest: '../emission_events/static/js/'
    },
    concat: {
      options: {
        separator: ';',
      },
      dist: {
        src: [
          '<%= paths.bower %>jquery/dist/jquery.js',
          '<%= paths.bower %>foundation/js/foundation.js',
          '<%= paths.bower %>chartjs/Chart.js'
        ],
        dest: '<%= paths.dest %>vendor.js',
      },
    },
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');

  // Default task(s).
  grunt.registerTask('default', ['concat']);

};
