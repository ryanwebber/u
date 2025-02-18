use std::path::PathBuf;

pub const SCRIPT_DIR_ENV_VAR: &str = "U_SCRIPTS_DIR";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Settings {
    pub config_path: PathBuf,
    pub executable: String,
}

impl Settings {
    pub fn try_load() -> anyhow::Result<Self> {
        Ok(Settings {
            config_path: {
                if let Ok(path) = std::env::var(SCRIPT_DIR_ENV_VAR) {
                    PathBuf::from(path)
                } else {
                    let home_dir = homedir::my_home()?
                        .ok_or_else(|| anyhow::anyhow!("Could not find home directory"))?;

                    home_dir.join(".uscripts")
                }
            },
            executable: {
                if let Ok(path) = std::env::var("U_EXECUTABLE") {
                    path
                } else {
                    String::from("python3.11")
                }
            },
        })
    }
}
