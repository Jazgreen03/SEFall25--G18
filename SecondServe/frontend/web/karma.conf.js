// karma.conf.js
module.exports = function(config) {
  config.set({
    basePath: '',
    frameworks: ['jasmine', '@angular-devkit/build-angular'],
    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-coverage'),
      require('karma-jasmine-html-reporter'),
      //require('@angular-devkit/build-angular/plugins/karma')
    ],
    client: {
      clearContext: false
    },
    coverageReporter: {
      dir: require('path').join(__dirname, 'coverage'),
      reporters: [
        { type: 'html', subdir: 'web' },          // HTML report in coverage/web
        { type: 'lcovonly', subdir: '.', file: 'lcov.info' } // lcov at coverage/lcov.info
      ],
      fixWebpackSourcePaths: true
    },
    reporters: ['progress', 'kjhtml', 'coverage'],
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    browsers: ['ChromeHeadlessNoSandbox'],
    customLaunchers: {
      ChromeHeadlessNoSandbox: {
        base: 'ChromeHeadless',
        flags: ['--no-sandbox', '--disable-gpu']
      }
    },
    singleRun: true,               // ensures coverage files are written
    restartOnFileChange: false
  });
};
