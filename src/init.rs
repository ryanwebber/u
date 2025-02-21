use crate::settings::Settings;

const STATIC_TARBALL: &[u8] = include_bytes!(env!("STATIC_TARBALL"));

pub fn init_if_required(settings: &Settings) -> anyhow::Result<()> {
    match settings.config_path.try_exists() {
        Err(err) => anyhow::bail!(err),
        Ok(true) => Ok(()),
        Ok(false) => {
            let confirmation = inquire::Confirm::new(
                "Script directory does not exist. Would you like to create it?",
            )
            .with_help_message(&format!(
                "Script directory: {}",
                settings.config_path.display()
            ))
            .with_default(false)
            .prompt()?;

            if !confirmation {
                std::process::exit(0);
            }

            let reader = flate2::read::GzDecoder::new(STATIC_TARBALL);
            let mut archive = tar::Archive::new(reader);
            archive.unpack(&settings.config_path)?;

            println!(
                "Script directory created at: {}",
                settings.config_path.display()
            );

            println!();

            Ok(())
        }
    }
}
