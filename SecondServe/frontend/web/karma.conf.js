// karma.conf.js
module.exports = function (config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-coverage'),
      require('karma-jasmine-html-reporter'),
    ],
    client: {
      clearContext: false, // Leave Jasmine Spec Runner output visible in browser
    },

    // ✅ Coverage output configuration
    coverageReporter: {
      dir: require('path').join(__dirname, 'coverage'),
      reporters: [
        { type: 'html', subdir: 'web' },                     // Full HTML report
        { type: 'lcovonly', subdir: '.', file: 'lcov.info' }, // LCOV for external tools
        { type: 'json', subdir: 'web', file: 'coverage-final.json' }, // ✅ For badge generator
        { type: 'text-summary' },                            // Summary in console
      ],
      fixWebpackSourcePaths: true,
    },

    reporters: ['progress', 'kjhtml', 'coverage'],

    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,

    // ✅ Headless browser setup
    browsers: ['ChromeHeadlessNoSandbox'],
    customLaunchers: {
      ChromeHeadlessNoSandbox: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox', '--disable-gpu'],
      },
    },

    singleRun: true, // Ensures tests run once and exit (useful in CI)
    restartOnFileChange: false,
  });
};
