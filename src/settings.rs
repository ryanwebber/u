use std::path::PathBuf;

pub const SCRIPT_DIR_ENV_VAR: &str = "U_SCRIPTS_DIR";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Settings {
    pub config_path: PathBuf,
}

impl Settings {
    pub fn try_load() -> anyhow::Result<Self> {
        let config_path = {
            if let Ok(path) = std::env::var(SCRIPT_DIR_ENV_VAR) {
                PathBuf::from(path)
            } else {
                let home_dir = homedir::my_home()?
                    .ok_or_else(|| anyhow::anyhow!("Could not find home directory"))?;

                home_dir.join(".uscripts")
            }
        };

        Ok(Settings { config_path })
    }
}
