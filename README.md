# u

[![Rust](https://github.com/ryanwebber/u/actions/workflows/rust.yml/badge.svg)](https://github.com/ryanwebber/u/actions/workflows/rust.yml)

A simple script manager and runner.

## Features

- Create, manage, and run scripts
- Customizable templates
- Entirely source control compatible
- Hackable and extendable 

## Dependencies

- Python 3.11+

## Getting Started

```bash
u scripts/new --template bash examples/hello-world
u scripts/list
u examples/hello-world
u scripts/delete hello-world
```

## Design

The compiled binary embeds a tarball containing some basic scripts to create and manage user scripts, along with some basic templates. At first launch, this tarball is extracted to a config folder in the users home directory. Subsequently, the binary simply passes the arguments to a python-based script runner that lives in this config directory.

This allows for the entire script configuration directory to be source controlled, including the script runner, templates, and the user scripts themselves.

A manifest file is used to track all scripts and templates and can easily be modified by hand.
