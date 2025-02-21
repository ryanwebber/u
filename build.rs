use std::io::Write;

fn main() {
    // Archive and gzip the static directory and write it to a file to be included in the binary
    let mut archive = tar::Builder::new(Vec::new());
    archive.follow_symlinks(false);

    archive
        .append_dir_all(".", "static")
        .expect("Failed to archive static directory");

    let mut gz = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::default());
    gz.write_all(&archive.into_inner().expect("Failed to get archive data"))
        .expect("Failed to write archive data");

    let gz_data = gz.finish().expect("Failed to finish gz encoding");

    // Write the gzipped data to a file in the cargo out dir
    let tarball_output_path =
        std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap()).join("static.tar.gz");

    std::fs::write(&tarball_output_path, gz_data).expect("Failed to write gzipped data");

    // Print out the path to the gzipped file
    println!(
        "cargo:rustc-env=STATIC_TARBALL={}",
        tarball_output_path.display()
    );

    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-changed=static");

    // Also, track the files in the tarball for changes
    for entry in glob::glob("static/**/*").expect("Failed to read glob pattern") {
        match entry {
            Ok(path) => {
                println!("cargo:rerun-if-changed={}", path.display());
            }
            Err(e) => {
                eprintln!("{:?}", e);
                panic!("Failed to get entry path from glob pattern");
            }
        }
    }
}
