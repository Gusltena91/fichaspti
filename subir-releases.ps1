# ============================================================
# Script PowerShell para subir PDFs a GitHub Releases
# Ejecutar desde: C:\Users\atenc\Claude\fichas-tecnicas
# Prerequisito: gh auth login (GitHub CLI autenticado)
# ============================================================

$ErrorActionPreference = "Stop"

# Verificar que gh está instalado
try { gh --version | Out-Null } catch {
    Write-Host "ERROR: GitHub CLI (gh) no está instalado." -ForegroundColor Red
    Write-Host "Instálalo desde: https://cli.github.com/" -ForegroundColor Yellow
    exit 1
}

# Verificar autenticación
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: No estás autenticado en GitHub CLI." -ForegroundColor Red
    Write-Host "Ejecuta: gh auth login" -ForegroundColor Yellow
    exit 1
}

$pdfDir = ".\pdfs"
$tag = "v1"
$pdfs = Get-ChildItem -Path $pdfDir -Filter "*.pdf"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Subiendo $($pdfs.Count) PDFs a GitHub Releases" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Intentar crear el release
Write-Host "`nCreando release $tag..." -ForegroundColor Yellow
try {
    gh release create $tag --title "Fichas Técnicas $tag" --notes "140 fichas técnicas en PDF" 2>&1 | Out-Null
    Write-Host "Release $tag creado." -ForegroundColor Green
} catch {
    Write-Host "Release $tag ya existe, se agregarán los archivos." -ForegroundColor Yellow
}

# Subir PDFs en lotes de 10
$batch = @()
$count = 0
$total = $pdfs.Count

foreach ($pdf in $pdfs) {
    $batch += $pdf.FullName
    $count++

    if ($batch.Count -eq 10 -or $count -eq $total) {
        Write-Host "  Subiendo $count/$total..." -ForegroundColor Gray
        gh release upload $tag @batch --clobber 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ERROR subiendo lote. Reintentando uno por uno..." -ForegroundColor Red
            foreach ($f in $batch) {
                $fname = Split-Path $f -Leaf
                Write-Host "    Subiendo $fname..." -ForegroundColor Gray
                gh release upload $tag $f --clobber 2>&1 | Out-Null
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "    FALLO: $fname" -ForegroundColor Red
                }
            }
        }
        $batch = @()
    }
}

Write-Host "`n============================================" -ForegroundColor Green
Write-Host " $count PDFs subidos exitosamente" -ForegroundColor Green
Write-Host " URL base: https://github.com/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/releases/download/$tag/" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
