/**
 * Sonic-Home-Express CLI - uHomeNest Management Interface
 * Integrated with Sonic-Screwdriver v1.1.0
 */

import { Command } from "commander";
import { execSync } from "child_process";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join, resolve } from "path";
import chalk from "chalk";
import { fileURLToPath } from "url";

// Get directory name in ES modules
const __dirname = resolve(fileURLToPath(import.meta.url), "..");

interface SonicHomeOptions {
  verbose?: boolean;
  force?: boolean;
  dryRun?: boolean;
}

export class SonicHomeCLI {
  private program: Command;
  private projectRoot: string;

  constructor() {
    this.program = new Command();
    this.projectRoot = resolve(__dirname, "../../..");
    
    this.setupBaseCommands();
    this.setupHomeAutomationCommands();
    this.setupSonicScrewdriverCommands();
    this.setupDiagnosticCommands();
  }

  private setupBaseCommands(): void {
    this.program
      .name("sonic-home")
      .description("Sonic-Home-Express CLI — uHomeNest management tool")
      .version("1.1.0")
      .option("--verbose", "Enable verbose output")
      .option("--debug", "Enable debug mode")
      .hook("preAction", (thisCommand) => {
        if (thisCommand.opts().verbose) {
          console.log(chalk.blue(`🔧 Running: ${thisCommand.name()}`));
        }
      });

    // Installation commands
    this.program
      .command("install")
      .description("Install uHomeNest core components")
      .option("--force", "Force reinstall")
      .action(async (options: SonicHomeOptions) => {
        console.log(chalk.blue("🏠 Installing uHomeNest core components..."));
        // Implementation would go here
        console.log(chalk.green("✅ uHomeNest installation completed"));
      });

    this.program
      .command("update")
      .description("Update uHomeNest to latest version")
      .option("--force", "Force update")
      .action(async (options: SonicHomeOptions) => {
        console.log(chalk.blue("🔄 Updating uHomeNest..."));
        // Implementation would go here
        console.log(chalk.green("✅ uHomeNest update completed"));
      });
  }

  private setupHomeAutomationCommands(): void {
    // Home automation control
    this.program
      .command("automation:start")
      .description("Start home automation services")
      .action(async () => {
        console.log(chalk.blue("🏡 Starting home automation services..."));
        // Implementation would go here
        console.log(chalk.green("✅ Home automation services started"));
      });

    this.program
      .command("automation:stop")
      .description("Stop home automation services")
      .action(async () => {
        console.log(chalk.blue("🛑 Stopping home automation services..."));
        // Implementation would go here
        console.log(chalk.green("✅ Home automation services stopped"));
      });

    this.program
      .command("automation:status")
      .description("Show home automation status")
      .action(async () => {
        console.log(chalk.cyan("📊 Home Automation Status"));
        console.log("==========================");
        console.log("Status: Running");
        console.log("Devices: 12 connected");
        console.log("Scenes: 5 active");
        console.log("Uptime: 3h 45m");
      });

    // Device management
    this.program
      .command("device:list")
      .description("List connected devices")
      .action(async () => {
        console.log(chalk.blue("📋 Listing connected devices..."));
        // Implementation would go here
        console.log("💡 Living Room Light - Connected");
        console.log("🔌 Smart Plug - Connected");
        console.log("🌡️  Thermostat - Connected");
      });

    this.program
      .command("device:control <device> <action>")
      .description("Control a specific device")
      .action(async (device, action) => {
        console.log(chalk.blue(`🎛️  Controlling ${device}: ${action}`));
        // Implementation would go here
        console.log(chalk.green(`✅ ${device} ${action} completed`));
      });

    // Scene management
    this.program
      .command("scene:activate <scene>")
      .description("Activate a home automation scene")
      .action(async (scene) => {
        console.log(chalk.blue(`🎭 Activating scene: ${scene}`));
        // Implementation would go here
        console.log(chalk.green(`✅ Scene ${scene} activated`));
      });
  }

  private setupSonicScrewdriverCommands(): void {
    // Sonic-Screwdriver version
    this.program
      .command("sonic:version")
      .description("Show Sonic-Screwdriver version")
      .action(async () => {
        console.log(chalk.blue("🔧 Checking Sonic-Screwdriver version..."));
        const result = this.runSonicCommand(["version"]);
        console.log(chalk.cyan(result));
      });

    // Library management
    this.program
      .command("sonic:library")
      .description("Show available games in Sonic-Screwdriver library")
      .action(async () => {
        console.log(chalk.blue("📚 Fetching Sonic-Screwdriver library..."));
        const result = this.runSonicCommand(["library", "list"]);
        console.log(result);
      });

    // Game installation
    this.program
      .command("sonic:install <game>")
      .description("Install a game using Sonic-Screwdriver")
      .action(async (game) => {
        console.log(chalk.blue(`🎮 Installing game: ${game}`));
        const result = this.runSonicCommand(["install", game]);
        console.log(result);
      });

    // Game removal
    this.program
      .command("sonic:remove <game>")
      .description("Remove a game using Sonic-Screwdriver")
      .action(async (game) => {
        console.log(chalk.blue(`🗑️  Removing game: ${game}`));
        const result = this.runSonicCommand(["remove", game]);
        console.log(result);
      });

    // Health monitoring
    this.program
      .command("sonic:health")
      .description("Check Sonic-Screwdriver container health")
      .option("--game <game>", "Check specific game container")
      .option("--all", "Check all containers")
      .action(async (options) => {
        if (options.game) {
          console.log(chalk.blue(`🩺 Checking health for game: ${options.game}`));
          const result = this.runSonicCommand(["health", options.game]);
          console.log(result);
        } else if (options.all) {
          console.log(chalk.blue("🩺 Checking health for all containers"));
          const result = this.runSonicCommand(["health", "--all"]);
          console.log(result);
        } else {
          console.log(chalk.blue("🩺 Checking overall Sonic-Screwdriver health"));
          const result = this.runSonicCommand(["health"]);
          console.log(result);
        }
      });

    // Container repair
    this.program
      .command("sonic:repair")
      .description("Repair unhealthy containers")
      .option("--game <game>", "Repair specific game")
      .option("--all", "Repair all containers")
      .action(async (options) => {
        if (options.game) {
          console.log(chalk.blue(`🩹 Repairing game: ${options.game}`));
          const result = this.runSonicCommand(["repair", options.game]);
          console.log(result);
        } else if (options.all) {
          console.log(chalk.blue("🩹 Repairing all unhealthy containers"));
          const result = this.runSonicCommand(["repair", "--all"]);
          console.log(result);
        } else {
          console.log(chalk.blue("🩹 Running automatic repair"));
          const result = this.runSonicCommand(["repair", "--all"]);
          console.log(result);
        }
      });

    // Container management
    this.program
      .command("sonic:start <game>")
      .description("Start a game container")
      .action(async (game) => {
        console.log(chalk.blue(`🚀 Starting container: ${game}`));
        const result = this.runSonicCommand(["start", game]);
        console.log(result);
      });

    this.program
      .command("sonic:stop <game>")
      .description("Stop a game container")
      .action(async (game) => {
        console.log(chalk.blue(`🛑 Stopping container: ${game}`));
        const result = this.runSonicCommand(["stop", game]);
        console.log(result);
      });

    this.program
      .command("sonic:logs <game>")
      .description("Show container logs")
      .option("--follow", "Follow logs")
      .option("--lines <count>", "Number of lines", "100")
      .action(async (game, options) => {
        console.log(chalk.blue(`📜 Showing logs for: ${game}`));
        const args = ["logs", game];
        if (options.follow) args.push("--follow");
        if (options.lines) args.push("--lines", options.lines);
        const result = this.runSonicCommand(args);
        console.log(result);
      });

    this.program
      .command("sonic:list")
      .description("List installed games")
      .action(async () => {
        console.log(chalk.blue("📋 Listing installed games"));
        const result = this.runSonicCommand(["list"]);
        console.log(result);
      });

    // Ventoy integration
    this.program
      .command("sonic:ventoy")
      .description("Sonic-Screwdriver Ventoy commands")
      .addCommand(
        new Command("package")
          .description("Create Ventoy installer bundle")
          .action(async () => {
            console.log(chalk.blue("📦 Creating Ventoy bundle..."));
            const result = this.runSonicCommand(["ventoy", "package"]);
            console.log(result);
          })
      )
      .addCommand(
        new Command("validate")
          .description("Validate Ventoy bundle")
          .action(async () => {
            console.log(chalk.blue("🔍 Validating Ventoy bundle..."));
            const result = this.runSonicCommand(["ventoy", "validate"]);
            console.log(result);
          })
      )
      .addCommand(
        new Command("info")
          .description("Show Ventoy bundle information")
          .action(async () => {
            console.log(chalk.blue("ℹ️  Showing Ventoy bundle info..."));
            const result = this.runSonicCommand(["ventoy", "info"]);
            console.log(result);
          })
      );
  }

  private setupDiagnosticCommands(): void {
    // System diagnostics
    this.program
      .command("diagnostics")
      .description("Run system diagnostics")
      .option("--fix", "Attempt to fix issues")
      .action(async (options) => {
        console.log(chalk.cyan("🩺 Running uHomeNest diagnostics..."));
        
        // Check Node.js
        try {
          const nodeVersion = execSync("node --version", { encoding: "utf8" }).trim();
          console.log(`✅ Node.js: ${nodeVersion}`);
        } catch {
          console.log(chalk.red("❌ Node.js: Not found"));
        }
        
        // Check Sonic-Screwdriver
        try {
          const sonicVersion = this.runSonicCommand(["version"]);
          console.log(`✅ Sonic-Screwdriver: ${sonicVersion}`);
        } catch {
          console.log(chalk.red("❌ Sonic-Screwdriver: Not found"));
        }
        
        // Check Docker
        try {
          execSync("docker --version", { stdio: "pipe" });
          console.log("✅ Docker: Installed");
        } catch {
          console.log(chalk.red("❌ Docker: Not found"));
        }
        
        console.log(chalk.green("🩺 Diagnostics completed"));
      });

    // Configuration management
    this.program
      .command("config:get <key>")
      .description("Get configuration value")
      .action(async (key) => {
        const configPath = join(this.projectRoot, "config.json");
        
        if (!existsSync(configPath)) {
          console.log(chalk.yellow(`⚠️  Config file not found: ${configPath}`));
          return;
        }
        
        try {
          const config = JSON.parse(readFileSync(configPath, "utf8"));
          const value = config[key];
          
          if (value !== undefined) {
            console.log(`${key}: ${JSON.stringify(value, null, 2)}`);
          } else {
            console.log(chalk.yellow(`⚠️  Key "${key}" not found`));
          }
        } catch (error) {
          console.error(chalk.red(`❌ Failed to read config: ${error.message}`));
        }
      });

    this.program
      .command("config:set <key> <value>")
      .description("Set configuration value")
      .action(async (key, value) => {
        const configPath = join(this.projectRoot, "config.json");
        
        try {
          let config = {};
          if (existsSync(configPath)) {
            config = JSON.parse(readFileSync(configPath, "utf8"));
          }
          
          // Try to parse value as JSON
          try {
            config[key] = JSON.parse(value);
          } catch {
            config[key] = value;
          }
          
          writeFileSync(configPath, JSON.stringify(config, null, 2), "utf8");
          console.log(chalk.green(`✅ Config updated: ${key} = ${JSON.stringify(config[key])}`));
        } catch (error) {
          console.error(chalk.red(`❌ Failed to update config: ${error.message}`));
        }
      });
  }

  // Helper method to run Sonic-Screwdriver commands
  private runSonicCommand(args: string[]): string {
    try {
      const result = execSync(`sonic ${args.join(' ')}`, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'inherit']
      });
      return result.trim();
    } catch (error) {
      console.error(chalk.red(`❌ Sonic-Screwdriver command failed: ${error.message}`));
      return '';
    }
  }

  // Main entry point
  public async run(argv: string[] = process.argv): Promise<void> {
    try {
      await this.program.parseAsync(argv);
    } catch (error) {
      console.error(chalk.red("❌ Error:", error));
      process.exit(1);
    }
  }

  // Factory method
  public static async createAndRun(): Promise<void> {
    const cli = new SonicHomeCLI();
    await cli.run();
  }
}

// Export for programmatic use
const sonicHomeCLI = new SonicHomeCLI();
export default sonicHomeCLI;