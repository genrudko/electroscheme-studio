use serde::Serialize;
use std::{
    fs,
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

#[tauri::command]
fn platform() -> String { std::env::consts::OS.to_string() }

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
    let packaged = std::env::current_exe().ok().and_then(|path| path.parent().map(|parent| parent.join("tools/visio_spike_tool.py")));
    let development = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../tools/visio_spike_tool.py");
    let tool = packaged.filter(|path| path.exists()).unwrap_or(development);
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
        .invoke_handler(tauri::generate_handler![platform, mark_ready, read_path, write_path, open_project, save_project, export_pdf, clipboard_write, clipboard_read, run_visio_tool])
        .run(tauri::generate_context!())
        .expect("tauri spike runtime");
}
