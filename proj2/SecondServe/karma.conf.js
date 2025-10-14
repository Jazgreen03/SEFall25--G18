module.exports = function (config) {
  config.set({
    // ... existing config ...
    browsers: ['Chrome', 'ChromeHeadless'],
    customLaunchers: {
      ChromeHeadless: {
        base: 'Chrome',
        flags: ['--headless', '--disable-gpu', '--no-sandbox', '--remote-debugging-port=9222'],
      },
    },
    singleRun: false,
    restartOnFileChange: true,
  });
};
