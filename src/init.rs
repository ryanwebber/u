use crate::settings::Settings;

const STATIC_TARBALL: &[u8] = include_bytes!(env!("STATIC_TARBALL"));

pub fn init_if_required(settings: &Settings) -> anyhow::Result<()> {
    if matches!(settings.config_path.try_exists(), Ok(false)) {
        unimplemented!("Unpacking static files is not implemented yet");
    }

    Ok(())
}
