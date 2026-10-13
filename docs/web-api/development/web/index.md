---
overview: true
---

# EnergyAtlasWeb Development Guide

EnergyAtlasWeb is the web and cross-platform frontend for EnergyAtlas. It consists of an
ASP.NET backend serving a JavaScript-driven UI, and can run either as a standalone web app
in a browser or as a native desktop application via .NET MAUI.

This section documents the job system, real-time logging, file handling, and execution mode
differences that developers need to understand when extending the application.


## Job system

EnergyAtlasWeb supports two kinds of jobs:

- **[GUI Job](gui-job.md)** — Automatically generates a complete job page (input form,
  real-time logs, output display) from C# attribute-decorated input/output classes. Use this
  when the job requires user-provided parameters or produces downloadable artefacts.

- **[GUI-less Job](guiless-job.md)** — A single-click background task with no input form.
  Parameters are hard-coded or read from server configuration. Use this for batch processing,
  infrastructure tasks, or anything that doesn't need user input.

Both job types share the same real-time logging infrastructure built on SignalR.


## Supporting infrastructure

- **[SignalR Logging](report-logs.md)** — How jobs report progress to the frontend in real
  time. Covers `IJobReporter`, `JobSignal`, `BinaryProgress` (spinner), `TQDM` (progress bar),
  and the SignalR delivery pipeline.

- **[Working with Local Files](file-sys-access.md)** — How file picking, upload, and output
  artefacts work. Covers the MAUI file picker bridge, the artifact sink for in-memory downloads,
  and on-disk reveal-in-folder outputs.

- **[Execution Modes](exec-modes.md)** — The two modes (browser and local/MAUI) that control
  how the frontend interacts with files and the host environment. Covers configuration,
  detection, and what changes between modes.


## Quick reference

| Topic | Page | Key classes |
|-------|------|-------------|
| GUI job | [gui-job.md](gui-job.md) | `GUIJobFactoryBase<TInput,TOutput>`, `IGUIJob<TInput,TOutput>`, `[JobInput]`, `[JobOutput]` |
| GUI-less job | [guiless-job.md](guiless-job.md) | `IJobFactory`, `IControllerJob` |
| Logging | [report-logs.md](report-logs.md) | `IJobReporter`, `JobSignal`, `BinaryProgress`, `TQDM` |
| File access | [file-sys-access.md](file-sys-access.md) | `OutputFileReference`, `IArtifactSink`, `GUIJobRunContext` |
| Execution modes | [exec-modes.md](exec-modes.md) | `ExecutionMode` config key, `/api/config` |
