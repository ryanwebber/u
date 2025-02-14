use std::process::Command;

use crate::settings::Settings;

pub fn run(settings: &Settings, args: impl Iterator<Item = String>) -> anyhow::Result<()> {
    let mut cmd = Command::new(settings.executable.clone());

    cmd.current_dir(&settings.config_path);
    cmd.env("PYTHONDONTWRITEBYTECODE", "1");

    cmd.arg("main.py");

    for arg in args {
        cmd.arg(arg);
    }

    cmd.spawn()?.wait()?;

    Ok(())
}
