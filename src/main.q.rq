use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "q")]
#[command(version)]
#[command(about = "Q Programming Language")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    New { name: String },
    Build,
    Run { file: String },
    Check { file: String },
    Fmt,
    Lint,
    Test,
    Repl,
    Version,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::New { name } => {
            println!("Creating project {name}");
        }
        Commands::Build => {
            println!("Building...");
        }
        Commands::Run { file } => {
            println!("Running {file}");
        }
        Commands::Check { file } => {
            println!("Checking {file}");
        }
        Commands::Fmt => {
            println!("Formatting...");
        }
        Commands::Lint => {
            println!("Linting...");
        }
        Commands::Test => {
            println!("Running tests...");
        }
        Commands::Repl => {
            println!("Starting Q REPL...");
        }
        Commands::Version => {
            println!("Q Language v0.1.0");
        }
    }
}
