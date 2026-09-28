# ADR-0002: Tauri Shell with a Rust Core

- Status: Accepted (implementation deferred)
- Date: 2026-09-27

## Context

The application needs a desktop UI plus strong ownership of processes, files, local storage, cryptography, updates, and OS facilities. The UI must not receive ambient system authority.

## Decision

Use Tauri as the planned desktop shell, Rust for the trusted system/core layer, and React + TypeScript + Vite for the planned renderer. SQLite access, process control, secret handling, filesystem mutation, and application policy reside behind Rust-side commands and ports.

## Consequences

This creates a clear WebView/core trust boundary and keeps system behavior out of the UI. Tauri-specific types must stay in adapters/composition. No scaffold or dependency is added during Phase 1.

