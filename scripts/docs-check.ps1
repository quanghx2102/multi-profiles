[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Errors = [System.Collections.Generic.List[string]]::new()
$Warnings = [System.Collections.Generic.List[string]]::new()

function Add-CheckError([string]$Message) {
    $Errors.Add($Message)
}

function Get-RelativeDisplay([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    if ($full.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $full.Substring($RepoRoot.Length).TrimStart('\', '/')
    }
    return $full
}

function Get-TextFiles {
    $roots = @('AGENTS.md', 'README.md', 'THIRD_PARTY_NOTICES.md', 'docs', 'contracts', 'research', 'audit')
    $files = @()
    foreach ($root in $roots) {
        $path = Join-Path $RepoRoot $root
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            $files += Get-Item -LiteralPath $path
        } elseif (Test-Path -LiteralPath $path -PathType Container) {
            $files += Get-ChildItem -LiteralPath $path -File -Recurse | Where-Object { $_.Extension -in @('.md', '.json', '.yaml', '.yml') }
        }
    }
    return $files | Sort-Object FullName -Unique
}

$textFiles = @(Get-TextFiles)
$markdownFiles = @($textFiles | Where-Object Extension -eq '.md')

# Local Markdown links. Anchors are intentionally ignored after validating the target file.
$linkPattern = '(?<!\!)\[[^\]]+\]\((?<target>[^)]+)\)'
foreach ($file in $markdownFiles) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    foreach ($match in [regex]::Matches($content, $linkPattern)) {
        $target = $match.Groups['target'].Value.Trim()
        if ($target.StartsWith('<') -and $target.EndsWith('>')) { $target = $target.Substring(1, $target.Length - 2) }
        if ($target -match '^(https?://|mailto:|#)') { continue }
        $pathPart = ($target -split '#', 2)[0]
        if ([string]::IsNullOrWhiteSpace($pathPart)) { continue }
        $pathPart = [Uri]::UnescapeDataString($pathPart).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
        $resolved = Join-Path $file.DirectoryName $pathPart
        if (-not (Test-Path -LiteralPath $resolved)) {
            Add-CheckError "Broken local link in $(Get-RelativeDisplay $file.FullName): $target"
        }
    }
}

# Audit register structure, enums, references, and terminal evidence rules.
$auditPath = Join-Path $RepoRoot 'docs\AUDIT_REGISTER.md'
$auditText = Get-Content -LiteralPath $auditPath -Raw
$auditHeaderMatches = [regex]::Matches($auditText, '(?m)^### (AUD-(?<number>[0-9]{3}))\s')
$auditIds = @($auditHeaderMatches | ForEach-Object { $_.Groups[1].Value })
$duplicateAuditIds = @($auditIds | Group-Object | Where-Object Count -gt 1)
foreach ($duplicate in $duplicateAuditIds) { Add-CheckError "Duplicate audit definition: $($duplicate.Name)" }
if ($auditIds.Count -eq 0) { Add-CheckError 'No audit item definitions found.' }
else {
    $numbers = @($auditIds | ForEach-Object { [int]($_.Substring(4)) } | Sort-Object -Unique)
    foreach ($number in 1..($numbers | Measure-Object -Maximum).Maximum) {
        if ($numbers -notcontains $number) { Add-CheckError ('Missing audit definition: AUD-{0:D3}' -f $number) }
    }
}

$allowedAuditStatuses = @('NOT_STARTED', 'RESEARCHING', 'TEST_READY', 'BLOCKED', 'CONFIRMED', 'PATCH_REQUIRED', 'RESOLVED', 'ACCEPTED_RISK', 'REJECTED')
$allowedEvidence = @('NONE', 'HYPOTHESIS', 'DOCUMENTED', 'SOURCE_CONFIRMED', 'TEST_CONFIRMED', 'MULTI_ENV_CONFIRMED')
$itemMatches = [regex]::Matches($auditText, '(?ms)^### (?<id>AUD-[0-9]{3}).*?(?=^### AUD-[0-9]{3}|^## Register maintenance)')
foreach ($item in $itemMatches) {
    $id = $item.Groups['id'].Value
    $body = $item.Value
    $statusMatches = [regex]::Matches($body, '(?m)^- \*\*Status:\*\* `(?<value>[A-Z_]+)`')
    $qualityMatches = [regex]::Matches($body, '(?m)^- \*\*Evidence quality:\*\* `(?<value>[A-Z_]+)`')
    if ($statusMatches.Count -ne 1) { Add-CheckError "$id must have exactly one Status field."; continue }
    if ($qualityMatches.Count -ne 1) { Add-CheckError "$id must have exactly one Evidence quality field."; continue }
    $status = $statusMatches[0].Groups['value'].Value
    $quality = $qualityMatches[0].Groups['value'].Value
    if ($allowedAuditStatuses -notcontains $status) { Add-CheckError "$id has invalid status: $status" }
    if ($allowedEvidence -notcontains $quality) { Add-CheckError "$id has invalid evidence quality: $quality" }
    if ($status -in @('CONFIRMED', 'RESOLVED')) {
        if ($body -notmatch 'EVD-AUD-[0-9]{3}-[0-9]{3}') { Add-CheckError "$id is $status without an evidence record reference." }
        if ($quality -in @('NONE', 'HYPOTHESIS', 'DOCUMENTED')) { Add-CheckError "$id is $status with insufficient evidence quality: $quality" }
    }
}

$allMarkdownText = ($markdownFiles | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw }) -join "`n"
$auditRefs = @([regex]::Matches($allMarkdownText, '\bAUD-[0-9]{3}\b') | ForEach-Object Value | Sort-Object -Unique)
foreach ($reference in $auditRefs) {
    if ($auditIds -notcontains $reference) { Add-CheckError "Reference to undefined audit ID: $reference" }
}

# Canonical requirement definitions and references.
$requirementPath = Join-Path $RepoRoot 'docs\REQUIREMENTS.md'
$requirementText = Get-Content -LiteralPath $requirementPath -Raw
$requirementIds = @([regex]::Matches($requirementText, '(?m)^\| `(REQ-[A-Z]+-[0-9]{3}|SEC-[0-9]{3}|INV-[0-9]{3})` \|') | ForEach-Object { $_.Groups[1].Value })
foreach ($duplicate in @($requirementIds | Group-Object | Where-Object Count -gt 1)) { Add-CheckError "Duplicate requirement definition: $($duplicate.Name)" }
$requirementRefs = @([regex]::Matches($allMarkdownText, '\b(?:REQ-[A-Z]+-[0-9]{3}|SEC-[0-9]{3}|INV-[0-9]{3})\b') | ForEach-Object Value | Sort-Object -Unique)
foreach ($reference in $requirementRefs) {
    if ($requirementIds -notcontains $reference) { Add-CheckError "Reference to undefined requirement ID: $reference" }
}

# ADR numbering, references, and status values.
$adrDir = Join-Path $RepoRoot 'docs\adr'
$adrFiles = @(Get-ChildItem -LiteralPath $adrDir -File -Filter '*.md')
$adrNumbers = @()
foreach ($file in $adrFiles) {
    if ($file.BaseName -notmatch '^(?<number>[0-9]{4})-') { Add-CheckError "ADR filename does not begin with four digits: $($file.Name)"; continue }
    $number = $Matches['number']
    $adrNumbers += $number
    $content = Get-Content -LiteralPath $file.FullName -Raw
    $status = [regex]::Match($content, '(?m)^- Status: (?<status>Accepted|Proposed|Superseded|Rejected)(?:[ (;,].*)?$')
    if (-not $status.Success) { Add-CheckError "ADR-$number has missing or invalid status." }
}
foreach ($duplicate in @($adrNumbers | Group-Object | Where-Object Count -gt 1)) { Add-CheckError "Duplicate ADR number: $($duplicate.Name)" }
$adrRefs = @([regex]::Matches($allMarkdownText, '\bADR-(?<number>[0-9]{4})\b') | ForEach-Object { $_.Groups['number'].Value } | Sort-Object -Unique)
foreach ($reference in $adrRefs) {
    if ($adrNumbers -notcontains $reference) { Add-CheckError "Reference to undefined ADR-$reference" }
}

# JSON and draft-schema structural validation, including local references.
$jsonFiles = @($textFiles | Where-Object Extension -eq '.json')
foreach ($file in $jsonFiles) {
    try { $json = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json }
    catch { Add-CheckError "Invalid JSON in $(Get-RelativeDisplay $file.FullName): $($_.Exception.Message)"; continue }
    if ($file.Name.EndsWith('.schema.json')) {
        if ($json.'$schema' -ne 'https://json-schema.org/draft/2020-12/schema') { Add-CheckError "Schema must declare JSON Schema 2020-12: $(Get-RelativeDisplay $file.FullName)" }
        if ([string]::IsNullOrWhiteSpace([string]$json.'$id')) { Add-CheckError "Schema missing `$id: $(Get-RelativeDisplay $file.FullName)" }
        if ($null -eq $json.type) { Add-CheckError "Schema missing top-level type: $(Get-RelativeDisplay $file.FullName)" }
        if ($null -eq $json.required) { Add-CheckError "Schema missing required fields: $(Get-RelativeDisplay $file.FullName)" }
        if ($null -eq $json.additionalProperties) { Add-CheckError "Schema missing additionalProperties policy: $(Get-RelativeDisplay $file.FullName)" }
        $schemaText = Get-Content -LiteralPath $file.FullName -Raw
        if ($schemaText -notmatch '"schemaVersion"') { Add-CheckError "Schema missing explicit schemaVersion: $(Get-RelativeDisplay $file.FullName)" }
        foreach ($refMatch in [regex]::Matches($schemaText, '"\$ref"\s*:\s*"(?<ref>[^"#]+)')) {
            $ref = $refMatch.Groups['ref'].Value
            if ($ref -match '^(https?://|urn:)') { continue }
            if (-not (Test-Path -LiteralPath (Join-Path $file.DirectoryName $ref))) { Add-CheckError "Broken schema reference in $(Get-RelativeDisplay $file.FullName): $ref" }
        }
    }
}

# Register migration must be atomic. YAML items imply generated Markdown authority.
$auditItemFiles = @(Get-ChildItem -LiteralPath (Join-Path $RepoRoot 'audit\items') -File | Where-Object Extension -in @('.yaml', '.yml'))
if ($auditItemFiles.Count -gt 0 -and $auditText -notmatch '(?m)^<!-- GENERATED; DO NOT EDIT') {
    Add-CheckError 'audit/items contains YAML records but docs/AUDIT_REGISTER.md is not marked generated; migration is partial.'
}

# Strong Camoufox capability claims require explicit qualification/evidence language.
foreach ($file in $markdownFiles) {
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $file.FullName) {
        $lineNumber++
        if ($line -match '(?i)\bCamoufox (supports|provides|implements|guarantees|can)\b' -and $line -notmatch '(?i)(does not|cannot|unverified|hypothes|candidate|AUD-[0-9]{3}|if |whether )') {
            Add-CheckError "Unqualified Camoufox capability claim in $(Get-RelativeDisplay $file.FullName):$lineNumber"
        }
    }
}

# Evidence hygiene: source records only, no binaries, raw profiles, or likely secret artifacts.
$evidenceDir = Join-Path $RepoRoot 'research\camoufox\evidence'
$allowedEvidenceExtensions = @('.md', '.json', '.yaml', '.yml', '.txt', '.csv', '.sha256')
foreach ($file in @(Get-ChildItem -LiteralPath $evidenceDir -File -Recurse)) {
    if ($allowedEvidenceExtensions -notcontains $file.Extension.ToLowerInvariant()) { Add-CheckError "Disallowed evidence artifact type: $(Get-RelativeDisplay $file.FullName)" }
    if ($file.Name -match '(?i)^(cookies\.sqlite|logins\.json|key[34]\.db|places\.sqlite|webappsstore\.sqlite)$') { Add-CheckError "Raw profile/secret-bearing file in evidence: $(Get-RelativeDisplay $file.FullName)" }
    if ($file.Length -gt 10MB) { Add-CheckError "Evidence file exceeds repository size policy: $(Get-RelativeDisplay $file.FullName)" }
}

$lockPath = Join-Path $RepoRoot 'research\camoufox\UPSTREAM_LOCK.json'
try {
    $lock = Get-Content -LiteralPath $lockPath -Raw | ConvertFrom-Json
    if ($lock.verificationStatus -eq 'UNSELECTED') {
        $forbiddenLockValues = @($lock.repository.commit, $lock.repository.tagOrRelease, $lock.firefoxBase.sha256, $lock.launcher.artifactSha256, $lock.platformArtifact.sha256) | Where-Object { $null -ne $_ -and $_ -ne 'UNSELECTED' }
        if ($forbiddenLockValues.Count -gt 0) { Add-CheckError 'UPSTREAM_LOCK is UNSELECTED but contains a selected commit/release/hash.' }
    }
} catch { Add-CheckError "Cannot validate UPSTREAM_LOCK.json: $($_.Exception.Message)" }

if ($Warnings.Count -gt 0) {
    Write-Host "Warnings ($($Warnings.Count)):" -ForegroundColor Yellow
    $Warnings | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
}
if ($Errors.Count -gt 0) {
    Write-Host "Documentation checks failed ($($Errors.Count)):" -ForegroundColor Red
    $Errors | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

Write-Host "Documentation checks passed: $($markdownFiles.Count) Markdown files, $($jsonFiles.Count) JSON files, $($auditIds.Count) audits, $($requirementIds.Count) requirements, and $($adrFiles.Count) ADRs." -ForegroundColor Green
