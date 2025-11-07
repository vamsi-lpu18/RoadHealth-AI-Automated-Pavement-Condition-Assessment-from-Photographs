# Testing Guide for RoadHealth AI

## 🧪 Manual Testing Checklist

### 1. User Authentication Tests

#### Registration

- [ ] Navigate to `/accounts/register/`
- [ ] Fill in all required fields
- [ ] Select role (Admin/Engineer/Viewer)
- [ ] Submit form
- [ ] Verify successful registration
- [ ] Check if automatically logged in
- [ ] Verify redirect to dashboard

#### Login

- [ ] Log out if logged in
- [ ] Navigate to `/accounts/login/`
- [ ] Enter valid credentials
- [ ] Click "Sign In"
- [ ] Verify successful login
- [ ] Check redirect to dashboard
- [ ] Test invalid credentials (should show error)

#### Profile

- [ ] Navigate to `/accounts/profile/`
- [ ] Update phone number
- [ ] Update organization
- [ ] Update address and bio
- [ ] Save changes
- [ ] Verify changes are saved

### 2. Image Upload Tests

#### Basic Upload

- [ ] Navigate to `/core/upload/`
- [ ] Select a road/pavement image (JPEG or PNG)
- [ ] Verify image preview appears
- [ ] Add title and description
- [ ] Click "Upload & Analyze"
- [ ] Verify success message
- [ ] Check redirect to dashboard
- [ ] Verify image appears in recent analyses

#### Upload with Location

- [ ] Navigate to upload page
- [ ] Select an image
- [ ] Click "Use My Current Location"
- [ ] Allow browser location access
- [ ] Verify latitude/longitude populated
- [ ] Add location name
- [ ] Submit form
- [ ] Verify location saved

#### File Validation

- [ ] Try uploading file > 10MB (should fail)
- [ ] Try uploading non-image file (should fail)
- [ ] Try uploading without selecting file (should fail)

### 3. Dashboard Tests

#### Statistics Display

- [ ] Navigate to `/core/dashboard/`
- [ ] Verify total images count
- [ ] Verify analyzed images count
- [ ] Verify pending images count
- [ ] Verify average severity displayed

#### Charts

- [ ] Verify "Defect Distribution" chart loads
- [ ] Verify "Condition Severity" chart loads
- [ ] Check if charts show correct data
- [ ] Hover over chart elements (should show tooltips)

#### Recent Images Table

- [ ] Verify table displays recent uploads
- [ ] Check image thumbnails load
- [ ] Verify status badges show correct colors
- [ ] Check analysis results display (if available)
- [ ] Click "View" button on an image
- [ ] Click "Report" button (if analysis complete)

#### Export Functions

- [ ] Click "Export CSV" button
- [ ] Verify CSV file downloads
- [ ] Open CSV and verify data
- [ ] Click "Summary Report" button
- [ ] Verify PDF downloads
- [ ] Open PDF and verify content

### 4. Image Detail Tests

#### View Details

- [ ] Navigate to any image detail page
- [ ] Verify image displays correctly
- [ ] Check upload information displays
- [ ] Verify status is shown
- [ ] Check location info (if available)

#### Analysis Results

- [ ] Wait for analysis to complete (or upload new image)
- [ ] Verify defect type is displayed
- [ ] Check severity score
- [ ] Verify condition label with correct color
- [ ] Check AI confidence percentage
- [ ] Read maintenance recommendation
- [ ] Verify annotated image displays (if available)

#### Report Generation

- [ ] Click "Download Report" button
- [ ] Verify PDF downloads
- [ ] Open and review PDF content
- [ ] Check all sections are complete
- [ ] Verify images are included
- [ ] Click "Preview Report"
- [ ] Verify preview page displays correctly

### 5. Map View Tests

#### Map Display

- [ ] Navigate to `/core/map/`
- [ ] Verify map loads (if Google Maps API configured)
- [ ] Check if markers appear for geotagged images
- [ ] Verify markers are color-coded by severity

#### Marker Interaction

- [ ] Click on a map marker
- [ ] Verify info window appears
- [ ] Check location name displays
- [ ] Verify defect type and condition shown
- [ ] Click "View Details" link in popup
- [ ] Verify correct image detail page opens

#### Map Legend

- [ ] Verify legend displays below map
- [ ] Check all condition types are listed
- [ ] Verify correct color coding

### 6. Image List Tests

#### Grid Display

- [ ] Navigate to `/core/images/`
- [ ] Verify images display in grid layout
- [ ] Check image thumbnails load
- [ ] Verify status badges visible
- [ ] Check condition badges (if analyzed)

#### Filtering

- [ ] Select status filter (e.g., "Analyzed")
- [ ] Click "Apply Filter"
- [ ] Verify only matching images show
- [ ] Click "Clear" to reset filter
- [ ] Verify all images show again

#### Image Cards

- [ ] Verify title displays (or "Untitled")
- [ ] Check user name shows
- [ ] Verify upload date displays
- [ ] Check location (if available)
- [ ] Verify defect type (if analyzed)
- [ ] Click "View" button
- [ ] Click "Report" button (if available)

### 7. Admin Panel Tests

#### Access Admin

- [ ] Navigate to `/admin/`
- [ ] Log in with superuser credentials
- [ ] Verify admin dashboard loads

#### User Management

- [ ] Click "Users"
- [ ] Verify user list displays
- [ ] Click on a user
- [ ] Update user information
- [ ] Save changes
- [ ] Verify changes saved

#### Image Records

- [ ] Click "Image Records"
- [ ] Verify uploaded images list
- [ ] Check filters work (status, user, date)
- [ ] Click on an image record
- [ ] Review metadata
- [ ] Verify file path correct

#### Analysis Results

- [ ] Click "Analysis Results"
- [ ] Verify results list displays
- [ ] Check defect type filter
- [ ] Check condition filter
- [ ] Click on a result
- [ ] Review analysis details
- [ ] Verify maintenance suggestion

### 8. API Tests (Using Postman or curl)

#### Get JWT Token

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your-email@example.com","password":"yourpassword"}'
```

- [ ] Verify token received

#### Register User

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "username":"testuser",
    "password":"testpass123",
    "password2":"testpass123",
    "first_name":"Test",
    "last_name":"User",
    "role":"engineer"
  }'
```

- [ ] Verify user created

#### Get User Profile

```bash
curl http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

- [ ] Verify profile data returned

#### List Images

```bash
curl http://localhost:8000/api/core/images/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

- [ ] Verify images list returned

#### Get Statistics

```bash
curl http://localhost:8000/api/core/images/statistics/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

- [ ] Verify statistics returned

### 9. Email Notification Tests

#### Critical Condition Alert

- [ ] Upload image that gets "critical" condition
- [ ] Wait for analysis to complete
- [ ] Check console for email output (if using console backend)
- [ ] If using SMTP, check email inbox
- [ ] Verify email contains correct information

### 10. Performance Tests

#### Page Load Times

- [ ] Dashboard loads in < 2 seconds
- [ ] Image upload page loads quickly
- [ ] Image list page loads with many images
- [ ] Map view loads markers efficiently

#### Image Processing

- [ ] Upload image and time analysis
- [ ] Check Celery worker logs
- [ ] Verify async processing works
- [ ] Check status updates in real-time

### 11. Mobile Responsiveness Tests

#### Test on Different Devices

- [ ] Open on mobile phone
- [ ] Test on tablet
- [ ] Verify navigation menu works
- [ ] Check forms are usable
- [ ] Verify tables scroll horizontally
- [ ] Check charts resize properly
- [ ] Test image uploads on mobile

### 12. Error Handling Tests

#### Network Errors

- [ ] Disconnect internet
- [ ] Try to submit form
- [ ] Verify error message
- [ ] Reconnect and retry

#### Invalid Data

- [ ] Submit empty forms
- [ ] Enter invalid email format
- [ ] Use short password
- [ ] Verify validation errors display

#### Permission Errors

- [ ] As regular user, try to access admin panel
- [ ] Try to view another user's images (if not admin)
- [ ] Verify access denied

## 🔍 Automated Testing (Future Enhancement)

Create test files in each app:

- `accounts/tests.py`
- `core/tests.py`
- `analysis/tests.py`
- `reports/tests.py`

Run tests with:

```bash
python manage.py test
```

## 📊 Test Coverage Goals

- [ ] User authentication: 100%
- [ ] Image upload: 100%
- [ ] AI analysis: 90%
- [ ] Report generation: 90%
- [ ] API endpoints: 100%

## 🐛 Bug Reporting

If you find any issues:

1. Document the steps to reproduce
2. Note the error message
3. Check browser console
4. Review Django logs
5. Create detailed bug report

## ✅ Test Results Template

```
Date: _____________
Tester: ___________
Environment: Dev/Staging/Production

Passed: ___/___
Failed: ___/___

Critical Issues: ________
Major Issues: __________
Minor Issues: __________

Notes:
_____________________
_____________________
```

## 🎯 Success Criteria

All tests should pass before:

- Deploying to production
- Creating new releases
- Merging major features
- Conducting demos

Happy Testing! 🧪
