use serde::Serialize;
use std::{
    fs,
    path::{Path, PathBuf},
    process::{Command, Stdio},
    sync::Mutex,
    thread,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};
use tauri::Manager;

#[derive(Default)]
struct ClipboardState(Mutex<Option<arboard::Clipboard>>);

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

fn main_webview_window(app: &tauri::AppHandle, operation: &str) -> Result<tauri::WebviewWindow, String> {
    app.get_webview_window("main")
        .ok_or_else(|| format!("{operation}: main webview window not found"))
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
    let exit_delay_ms = if std::env::var("SPIKE_MEASURE").ok().as_deref() == Some("1") {
        Some(10_000)
    } else if std::env::var("SPIKE_SMOKE").ok().as_deref() == Some("1") {
        Some(100)
    } else {
        None
    };
    if let Some(delay_ms) = exit_delay_ms {
        thread::spawn(move || {
            thread::sleep(Duration::from_millis(delay_ms));
            app.exit(0);
        });
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
fn open_project(app: tauri::AppHandle) -> Result<Option<String>, String> {
    let window = main_webview_window(&app, "open failed")?;
    match rfd::FileDialog::new()
        .set_parent(&window)
        .add_filter("ElectroScheme spike", &["json"])
        .pick_file()
    {
        Some(path) => fs::read_to_string(path)
            .map(Some)
            .map_err(|error| format!("open failed: {error}")),
        None => Ok(None),
    }
}

fn native_save_bytes(
    app: &tauri::AppHandle,
    default_name: &str,
    filter_name: &str,
    extensions: &[&str],
    bytes: &[u8],
) -> Result<bool, String> {
    let window = main_webview_window(app, "save failed")?;

    match rfd::FileDialog::new()
        .set_parent(&window)
        .set_file_name(default_name)
        .add_filter(filter_name, extensions)
        .save_file()
    {
        Some(path) => {
            fs::write(&path, bytes).map_err(|error| format!("save failed: {error}"))?;
            Ok(true)
        }
        None => Ok(false),
    }
}

#[tauri::command]
fn save_project(app: tauri::AppHandle, default_name: String, content: String) -> Result<bool, String> {
    native_save_bytes(&app, &default_name, "ElectroScheme spike", &["json"], content.as_bytes())
}

#[tauri::command]
fn export_pdf(app: tauri::AppHandle, default_name: String, bytes: Vec<u8>) -> Result<bool, String> {
    native_save_bytes(&app, &default_name, "PDF", &["pdf"], &bytes)
}

fn with_clipboard<T>(state: &ClipboardState, operation: impl FnOnce(&mut arboard::Clipboard) -> Result<T, arboard::Error>) -> Result<T, String> {
    let mut guard = state.0.lock().map_err(|_| "clipboard state lock was poisoned".to_string())?;
    if guard.is_none() {
        *guard = Some(arboard::Clipboard::new().map_err(|error| error.to_string())?);
    }
    operation(guard.as_mut().expect("clipboard initialized")).map_err(|error| error.to_string())
}

#[tauri::command]
fn clipboard_write(state: tauri::State<'_, ClipboardState>, text: String) -> Result<(), String> {
    with_clipboard(&state, |clipboard| clipboard.set_text(text))
}

#[tauri::command]
fn clipboard_read(state: tauri::State<'_, ClipboardState>) -> Result<String, String> {
    with_clipboard(&state, arboard::Clipboard::get_text)
}

#[tauri::command]
fn run_visio_tool(args: Vec<String>) -> Result<ToolResult, String> {
    let executable = if cfg!(windows) { "python" } else { "python3" };
    let tool = runtime_root().join("tools/visio_spike_tool.py");
    let mut child = Command::new(executable)
        .arg(tool)
        .args(args)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|error| error.to_string())?;
    let started = Instant::now();
    loop {
        if child.try_wait().map_err(|error| error.to_string())?.is_some() {
            let output = child.wait_with_output().map_err(|error| error.to_string())?;
            return Ok(ToolResult {
                exit_code: output.status.code().unwrap_or(-1),
                stdout: String::from_utf8_lossy(&output.stdout).into_owned(),
                stderr: String::from_utf8_lossy(&output.stderr).into_owned(),
            });
        }
        if started.elapsed() >= Duration::from_secs(15) {
            child.kill().map_err(|error| error.to_string())?;
            let output = child.wait_with_output().map_err(|error| error.to_string())?;
            return Ok(ToolResult {
                exit_code: -2,
                stdout: String::from_utf8_lossy(&output.stdout).into_owned(),
                stderr: format!("{}timeout", String::from_utf8_lossy(&output.stderr)),
            });
        }
        thread::sleep(Duration::from_millis(50));
    }
}

fn main() {
    tauri::Builder::default()
        .manage(ClipboardState::default())
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
