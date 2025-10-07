@echo off
REM Script to configure Supabase Cloud integration for QuantumTrade

echo 🔄 Configuring Supabase Cloud for QuantumTrade...
echo Project URL: https://jstuvjquxrciaazrsedx.supabase.co

REM Check if .env file exists
if not exist ".env" (
    echo 📝 Creating .env file from .env.example...
    copy .env.example .env
)

echo.
echo Please update the following values in your .env file:
echo ==================================================
echo 1. DATABASE_URL - Replace ^<USER^> and ^<PASSWORD^> with your Supabase database credentials
echo 2. SUPABASE_ANON_KEY - Get from your Supabase project dashboard
echo 3. SUPABASE_SERVICE_ROLE_KEY - Get from your Supabase project dashboard
echo 4. SUPABASE_JWT_SECRET - Get from your Supabase project dashboard
echo.
echo You can find these values in your Supabase project dashboard under:
echo Settings ^> API
echo.
echo After updating the .env file, restart your application to use Supabase Cloud.

echo.
echo ✅ Supabase configuration guide completed!