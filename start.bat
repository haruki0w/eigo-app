@echo off
echo ========================================
echo 英語学習アプリ - ローカル起動スクリプト
echo ========================================
echo.

echo [1/2] バックエンドを起動中...
start "Backend Server" cmd /k "cd backend && python -m uvicorn main:app --reload"
timeout /t 3 /nobreak >nul

echo [2/2] フロントエンドを起動中...
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo 起動完了！
echo ========================================
echo バックエンド: http://localhost:8000
echo フロントエンド: http://localhost:3000
echo.
echo 各ウィンドウを閉じるとサーバーが停止します
pause

