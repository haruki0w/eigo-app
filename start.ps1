# 英語学習アプリ - ローカル起動スクリプト

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "英語学習アプリ - ローカル起動スクリプト" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# バックエンドの起動
Write-Host "[1/2] バックエンドを起動中..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python -m uvicorn main:app --reload"
Start-Sleep -Seconds 3

# フロントエンドの起動
Write-Host "[2/2] フロントエンドを起動中..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "起動完了！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "バックエンド: http://localhost:8000" -ForegroundColor Cyan
Write-Host "フロントエンド: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "各ウィンドウを閉じるとサーバーが停止します" -ForegroundColor Yellow

