// scripts/generate-badge.js
import fs from "fs";
import { badgen } from "badgen";

const coverageFile = "coverage/web/coverage-final.json";
const outputBadge = "src/assets/coverage-badge.svg";

if (!fs.existsSync(coverageFile)) {
  console.error(`❌ Coverage file not found: ${coverageFile}`);
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(coverageFile, "utf8"));

// Accumulators
let totalStatements = 0, coveredStatements = 0;
let totalFunctions = 0, coveredFunctions = 0;
let totalBranches = 0, coveredBranches = 0;
let totalLines = 0, coveredLines = 0;

for (const file of Object.values(data)) {
  // Statements
  if (file.s) {
    const counts = Object.values(file.s);
    coveredStatements += counts.filter(c => c > 0).length;
    totalStatements += counts.length;
  }
  // Functions
  if (file.f) {
    const counts = Object.values(file.f);
    coveredFunctions += counts.filter(c => c > 0).length;
    totalFunctions += counts.length;
  }
  // Branches
  if (file.b) {
    const counts = Object.values(file.b).flat();
    coveredBranches += counts.filter(c => c > 0).length;
    totalBranches += counts.length;
  }
  // Lines — fallback: same as statements
  if (file.s) {
    const counts = Object.values(file.s);
    coveredLines += counts.filter(c => c > 0).length;
    totalLines += counts.length;
  }
}

// Compute percentages
const pctStatements = totalStatements ? (coveredStatements / totalStatements) * 100 : 0;
const pctFunctions = totalFunctions ? (coveredFunctions / totalFunctions) * 100 : 0;
const pctBranches = totalBranches ? (coveredBranches / totalBranches) * 100 : 0;
const pctLines = totalLines ? (coveredLines / totalLines) * 100 : 0;

const avgCoverage = (pctStatements + pctFunctions + pctBranches + pctLines) / 4;

// Pick a color
let color = "red";
if (avgCoverage >= 90) color = "green";
else if (avgCoverage >= 75) color = "yellow";
else if (avgCoverage >= 50) color = "orange";

// Generate badge
const svg = badgen({
  label: "angular coverage",
  status: `${avgCoverage.toFixed(1)}%`,
  color,
});

fs.mkdirSync(outputBadge.substring(0, outputBadge.lastIndexOf("/")), { recursive: true });
fs.writeFileSync(outputBadge, svg);

console.log(`✅ Coverage badge generated: ${outputBadge} (${avgCoverage.toFixed(1)}%)`);
