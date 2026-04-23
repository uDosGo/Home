/**
 * Main entry point for Sonic-Home-Express CLI
 */

import { SonicHomeCLI } from './sonic-home-cli.js';

async function main() {
  try {
    const cli = new SonicHomeCLI();
    await cli.run();
  } catch (error) {
    console.error('❌ Sonic-Home-Express CLI error:', error);
    process.exit(1);
  }
}

main();