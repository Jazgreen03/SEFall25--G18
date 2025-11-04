const fs = require('fs');
const { createBadge } = require('badgen');
const lcovParse = require('lcov-parse');

lcovParse('coverage/lcov.info', (err, data) => {
  if (err) throw err;

  let lines = { total: 0, covered: 0 };
  data.forEach(file => {
    lines.total += file.lines.found;
    lines.covered += file.lines.hit;
  });

  const pct = ((lines.covered / lines.total) * 100).toFixed(0);
  const badge = createBadge({
    label: 'coverage',
    status: `${pct}%`,
    color: pct >= 90 ? 'green' : pct >= 75 ? 'yellow' : 'red'
  });

  fs.writeFileSync('src/assets/coverage-badge.svg', badge)
  console.log('Coverage badge has been generated!')
});
