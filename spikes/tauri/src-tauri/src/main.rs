use serde::Serialize;
use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct ToolResult {
    exit_code: i32,
    stdout: String,
    stderr: String,
}

#[derive(Serialize)]
struct ReadyEvidence {
    candidate: &'static str,
    pid: u32,
    ready_epoch_ms: u128,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct AutomationContext {
    result_path: String,
    canonical_fixture_path: String,
    vsdx_fixture_path: String,
    vssx_fixture_path: String,
    round_trip_path: String,
    pdf_path: String,
    generated_vsdx_path: String,
}

fn packaged_root() -> Option<PathBuf> {
    std::env::current_exe().ok()?.parent().map(Path::to_path_buf)
}

fn development_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..")
}

fn runtime_root() -> PathBuf {
    packaged_root().filter(|root| root.join("tools").exists()).unwrap_or_else(development_root)
}

fn fixture_root() -> PathBuf {
    packaged_root()
        .filter(|root| root.join("fixtures").exists())
        .map(|root| root.join("fixtures"))
        .unwrap_or_else(|| development_root().join("shared/fixtures"))
}

#[tauri::command]
fn platform() -> String { std::env::consts::OS.to_string() }

#[tauri::command]
fn automation_context() -> Option<AutomationContext> {
    let result_path = PathBuf::from(std::env::var("SPIKE_SCENARIO_RESULT").ok()?);
    let workspace = result_path.parent().unwrap_or_else(|| Path::new("."));
    let fixtures = fixture_root();
    Some(AutomationContext {
        result_path: result_path.to_string_lossy().into_owned(),
        canonical_fixture_path: fixtures.join("canonical-project.json").to_string_lossy().into_owned(),
        vsdx_fixture_path: fixtures.join("visio/controlled-minimal.vsdx").to_string_lossy().into_owned(),
        vssx_fixture_path: fixtures.join("visio/controlled-master.vssx").to_string_lossy().into_owned(),
        round_trip_path: workspace.join("tauri-canonical-roundtrip.json").to_string_lossy().into_owned(),
        pdf_path: workspace.join("tauri-deterministic-output.pdf").to_string_lossy().into_owned(),
        generated_vsdx_path: workspace.join("tauri-generated-minimal.vsdx").to_string_lossy().into_owned(),
    })
}

#[tauri::command]
fn mark_ready(app: tauri::AppHandle) -> Result<(), String> {
    if let Ok(path) = std::env::var("SPIKE_READY_FILE") {
        let ready = ReadyEvidence {
            candidate: "tauri",
            pid: std::process::id(),
            ready_epoch_ms: SystemTime::now().duration_since(UNIX_EPOCH).map_err(|error| error.to_string())?.as_millis(),
        };
        fs::write(path, serde_json::to_vec(&ready).map_err(|error| error.to_string())?).map_err(|error| error.to_string())?;
    }
    if std::env::var("SPIKE_MEASURE").ok().as_deref() == Some("1") {
        thread::spawn(move || { thread::sleep(Duration::from_millis(1500)); app.exit(0); });
    } else if std::env::var("SPIKE_SMOKE").ok().as_deref() == Some("1") {
        thread::spawn(move || { thread::sleep(Duration::from_millis(100)); app.exit(0); });
    }
    Ok(())
}

#[tauri::command]
fn read_path(path: String) -> Result<String, String> { fs::read_to_string(path).map_err(|error| error.to_string()) }

#[tauri::command]
fn write_path(path: String, content: String) -> Result<(), String> { fs::write(path, content).map_err(|error| error.to_string()) }

#[tauri::command]
fn write_bytes_path(path: String, bytes: Vec<u8>) -> Result<(), String> { fs::write(path, bytes).map_err(|error| error.to_string()) }

#[tauri::command]
fn open_project() -> Result<Option<String>, String> {
    match rfd::FileDialog::new().add_filter("ElectroScheme spike", &["json"]).pick_file() {
        Some(path) => fs::read_to_string(path).map(Some).map_err(|error| error.to_string()),
        None => Ok(None),
    }
}

#[tauri::command]
fn save_project(default_name: String, content: String) -> Result<bool, String> {
    match rfd::FileDialog::new().set_file_name(&default_name).add_filter("ElectroScheme spike", &["json"]).save_file() {
        Some(path) => { fs::write(path, content).map_err(|error| error.to_string())?; Ok(true) }
        None => Ok(false),
    }
}

#[tauri::command]
fn export_pdf(default_name: String, bytes: Vec<u8>) -> Result<bool, String> {
    match rfd::FileDialog::new().set_file_name(&default_name).add_filter("PDF", &["pdf"]).save_file() {
        Some(path) => { fs::write(path, bytes).map_err(|error| error.to_string())?; Ok(true) }
        None => Ok(false),
    }
}

#[tauri::command]
fn clipboard_write(text: String) -> Result<(), String> {
    arboard::Clipboard::new().map_err(|error| error.to_string())?.set_text(text).map_err(|error| error.to_string())
}

#[tauri::command]
fn clipboard_read() -> Result<String, String> {
    arboard::Clipboard::new().map_err(|error| error.to_string())?.get_text().map_err(|error| error.to_string())
}

#[tauri::command]
fn run_visio_tool(args: Vec<String>) -> Result<ToolResult, String> {
    let executable = if cfg!(windows) { "python" } else { "python3" };
    let tool = runtime_root().join("tools/visio_spike_tool.py");
    let mut child = Command::new(executable).arg(tool).args(args).stdin(Stdio::null()).stdout(Stdio::piped()).stderr(Stdio::piped()).spawn().map_err(|error| error.to_string())?;
    let started = Instant::now();
    loop {
        if child.try_wait().map_err(|error| error.to_string())?.is_some() {
            let output = child.wait_with_output().map_err(|error| error.to_string())?;
            return Ok(ToolResult { exit_code: output.status.code().unwrap_or(-1), stdout: String::from_utf8_lossy(&output.stdout).into_owned(), stderr: String::from_utf8_lossy(&output.stderr).into_owned() });
        }
        if started.elapsed() >= Duration::from_secs(15) {
            child.kill().map_err(|error| error.to_string())?;
            let output = child.wait_with_output().map_err(|error| error.to_string())?;
            return Ok(ToolResult { exit_code: -2, stdout: String::from_utf8_lossy(&output.stdout).into_owned(), stderr: format!("{}timeout", String::from_utf8_lossy(&output.stderr)) });
        }
        thread::sleep(Duration::from_millis(50));
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            platform,
            automation_context,
            mark_ready,
            read_path,
            write_path,
            write_bytes_path,
            open_project,
            save_project,
            export_pdf,
            clipboard_write,
            clipboard_read,
            run_visio_tool
        ])
        .run(tauri::generate_context!())
        .expect("tauri spike runtime");
}
