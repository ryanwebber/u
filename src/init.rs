use crate::settings::Settings;

const STATIC_TARBALL: &[u8] = include_bytes!(env!("STATIC_TARBALL"));

pub fn init_if_required(settings: &Settings) -> anyhow::Result<()> {
    println!("Tarball size: {} bytes", STATIC_TARBALL.len());

    // write the tarball to "/Users/rwebber/dev/hobby/u/hackyfile.tar.gz"
    std::fs::write(
        "/Users/rwebber/dev/hobby/u/hackyfile.tar.gz",
        STATIC_TARBALL,
    )
    .unwrap();

    Ok(())
}
