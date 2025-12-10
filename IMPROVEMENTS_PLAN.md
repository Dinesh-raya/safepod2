# Improvements Plan for SecureText Vault

## Issue 1: Dark Mode Toggle Not Working Properly

### Current Problem
The dark mode toggle is not consistently applying styles throughout the application, resulting in a mixed appearance with some elements in dark mode and others in light mode.

### Solution
1. Add `!important` to all CSS rules to ensure they override default Streamlit styles
2. Expand CSS selectors to cover all text elements
3. Ensure consistent styling for all interactive elements

### Implementation
Modify the theme CSS in `site_management_page()` function to include:
- `!important` declarations for all CSS rules
- Comprehensive selectors for all text elements (h1-h6, p, div, span, label)
- Consistent styling for buttons, inputs, and other UI elements

## Issue 2: Auto-Save Functionality Clarity

### Current Behavior
- Content auto-saves every 30 seconds if changes are detected
- Manual save is also available via the Save button
- Users may not be aware when content is auto-saved

### Enhancement
1. Add visual indicators for auto-save status
2. Show "Last auto-saved" timestamp
3. Provide clear feedback when manual save occurs

### Implementation
- Keep existing auto-save logic but improve UI indicators
- Add a warning when there are unsaved changes
- Show timestamps for last auto-save and manual save

## Issue 3: Missing Unsaved Changes Warning

### Current Problem
No warning is shown when users try to leave the page with unsaved changes.

### Solution
Implement unsaved changes tracking and warnings:
1. Track when content is modified
2. Show warning when navigating away with unsaved changes
3. Show warning when logging out with unsaved changes

### Implementation
1. Add `unsaved_changes` flag to session state
2. Compare current content with saved content to detect changes
3. Show warnings before logout when unsaved changes exist
4. Add visual indicator for unsaved changes

## Implementation Steps

### Step 1: Fix Dark Mode Theming
- Modify CSS in both theme blocks to use `!important`
- Expand selectors to cover all text elements
- Ensure consistent styling across all components

### Step 2: Improve Auto-Save Indicators
- Keep existing auto-save functionality
- Add visual indicators for save status
- Show timestamps for last save actions

### Step 3: Add Unsaved Changes Tracking
- Add `unsaved_changes` to session state
- Implement content comparison logic
- Add warnings for navigation with unsaved changes

## Expected Results

1. **Consistent Dark/Light Mode**: All elements will consistently use either dark or light theme without mixing
2. **Clear Auto-Save Feedback**: Users will clearly see when content is saved and when it's not
3. **Unsaved Changes Protection**: Users will be warned before losing unsaved work

## Technical Approach

Instead of editing the large main.py file directly, we recommend implementing these changes through targeted search and replace operations focusing on:

1. The theme CSS blocks (lines ~357-419)
2. The session state initialization (around line 332)
3. The save functionality (around lines 810-890)
4. The logout functionality (around line 728)