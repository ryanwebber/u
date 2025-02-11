use std::process::Command;

use crate::settings::Settings;

pub fn run(settings: &Settings, args: Vec<String>) -> anyhow::Result<()> {
    let mut cmd = Command::new("python3");

    cmd.current_dir(settings.config_path.clone());
    cmd.arg("main.py");

    for arg in args.iter() {
        cmd.arg(arg);
    }

    cmd.spawn()?.wait()?;

    Ok(())
}
