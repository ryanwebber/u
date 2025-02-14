use settings::Settings;

mod init;
mod runner;
mod settings;

fn main() {
    if let Err(e) = try_main() {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}

fn try_main() -> anyhow::Result<()> {
    let Ok(settings) = Settings::try_load() else {
        anyhow::bail!(
            "Failed determine a valid script directory. Retry with {} set",
            settings::SCRIPT_DIR_ENV_VAR
        );
    };

    init::init_if_required(&settings)?;
    runner::run(&settings, std::env::args().skip(1))?;

    Ok(())
}
