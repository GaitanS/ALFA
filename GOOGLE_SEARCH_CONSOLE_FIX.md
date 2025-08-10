# Google Search Console Redirect Error Fix

## Problem
Google Search Console reports that `http://alfarecovery.co.uk/` has a redirect error and is not being indexed.

## Solution Implemented

### 1. Server-Level Redirects (.htaccess)
- Created `.htaccess` file with proper HTTP to HTTPS redirects
- Added www to non-www canonical redirects
- Implemented security headers and caching rules

### 2. Django Configuration Updates
- Added `CanonicalDomainMiddleware` to enforce canonical domain
- Added `SecurityHeadersMiddleware` for better SEO
- Updated security settings in `settings.py`
- Fixed `robots.txt` to use correct canonical domain

### 3. Files Modified/Created
- `.htaccess` (new)
- `robots.txt` (updated)
- `core/middleware.py` (updated)
- `alfa_recovery/settings.py` (updated)
- `core/management/commands/check_site_health.py` (new)

## Deployment Steps

1. **Upload files to server:**
   ```bash
   # Upload .htaccess to web root directory
   # Upload updated Python files
   ```

2. **Restart Django application:**
   ```bash
   # In PythonAnywhere console or your server
   python manage.py collectstatic --noinput
   # Restart web app
   ```

3. **Test redirects:**
   ```bash
   python manage.py check_site_health
   ```

## Expected Results

### HTTP to HTTPS Redirects
- `http://alfarecovery.co.uk/` → `https://alfarecovery.co.uk/` (301)
- `http://www.alfarecovery.co.uk/` → `https://alfarecovery.co.uk/` (301)

### WWW to Non-WWW Redirects
- `https://www.alfarecovery.co.uk/` → `https://alfarecovery.co.uk/` (301)

### Google Search Console Actions

1. **Submit sitemap again:**
   - Go to Google Search Console
   - Navigate to Sitemaps
   - Submit: `https://alfarecovery.co.uk/sitemap.xml`

2. **Request indexing:**
   - Go to URL Inspection
   - Enter: `https://alfarecovery.co.uk/`
   - Click "Request Indexing"

3. **Mark as fixed:**
   - Go to Coverage report
   - Find the redirect error
   - Click "Mark as Fixed"

## Verification

### Manual Testing
Test these URLs in browser:
- `http://alfarecovery.co.uk/` should redirect to `https://alfarecovery.co.uk/`
- `https://www.alfarecovery.co.uk/` should redirect to `https://alfarecovery.co.uk/`

### Tools
- Use online redirect checkers
- Check with curl: `curl -I http://alfarecovery.co.uk/`
- Use Django management command: `python manage.py check_site_health`

## Timeline
- Changes should take effect immediately after deployment
- Google may take 1-7 days to re-crawl and update index
- Monitor Google Search Console for improvements

## Notes
- The redirect error is actually expected behavior - we WANT HTTP URLs to redirect to HTTPS
- The issue was that Google couldn't properly follow the redirects
- These changes ensure proper canonical URL structure for SEO