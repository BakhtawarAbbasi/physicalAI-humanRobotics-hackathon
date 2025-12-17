# Data Model: Cleanup & Landing Page UI Upgrade — ai-book

**Date**: 2025-12-17
**Feature**: 001-ui-upgrade
**Status**: Complete

## Entities

### 1. Docusaurus Theme Configuration

**Description**: Centralized configuration that controls colors, fonts, and layout properties with the new navy bluish tech theme

**Fields**:
- themeColors: Object containing primary, secondary, success, warning, danger color definitions
- typographySettings: Font family, size, and weight configurations
- layoutProperties: Spacing, breakpoints, and grid system parameters
- accessibilitySettings: Contrast ratios and accessibility compliance parameters

**Validation Rules**:
- All color values must be valid CSS color formats
- Contrast ratios must meet WCAG AA compliance (minimum 4.5:1 for normal text)
- Typography settings must be web-safe or properly loaded web fonts

### 2. Landing Page Feature Cards

**Description**: Three specific content cards that highlight Physical AI & Embodied Intelligence, Humanoid Robotics & Simulation, and AI-to-Physical World Integration

**Fields**:
- title: String with the feature card title
- description: Optional string with detailed description of the feature
- icon: Optional icon identifier or path for visual representation
- link: Optional URL for more information about the feature
- order: Integer defining the display order (1-3)

**Validation Rules**:
- Must have exactly 3 feature cards
- Titles must match exactly: "Physical AI & Embodied Intelligence", "Humanoid Robotics & Simulation", "AI-to-Physical World Integration"
- Order values must be unique integers from 1 to 3

### 3. Content Structure

**Description**: The cleaned-up documentation organization with default Docusaurus content removed

**Fields**:
- documentationDirectories: Array of directory paths that remain after cleanup
- navigationItems: Array of navigation elements displayed in sidebar/navbar
- contentLinks: Collection of internal links that must remain functional

**Validation Rules**:
- tutorial-basics directory must not exist
- tutorial-extras directory must not exist
- blog directory must not exist or be disabled
- All internal links must resolve to valid content
- Navigation structure must be logical and intuitive

### 4. Responsive Layout System

**Description**: CSS and component framework that adapts the new UI for different screen sizes and devices

**Fields**:
- breakpoints: Object defining mobile, tablet, desktop screen size thresholds
- componentBehaviors: How UI elements adapt at different screen sizes
- mediaQueries: CSS rules for responsive behavior
- deviceCompatibility: List of supported devices and browsers

**Validation Rules**:
- Must work on screen sizes from 320px to 1920px
- All interactive elements must have minimum 44px touch target size
- Content must remain readable at all zoom levels up to 200%

### 5. Accessibility Features

**Description**: Design elements and code implementations that ensure the new theme is usable by people with disabilities

**Fields**:
- colorContrastRatios: Measured contrast values for text and background combinations
- keyboardNavigation: Tab order and keyboard interaction patterns
- screenReaderSupport: ARIA labels and semantic HTML structure
- accessibilityCompliance: WCAG 2.1 AA compliance status

**Validation Rules**:
- Minimum contrast ratio of 4.5:1 for normal text, 3:1 for large text
- All interactive elements must be keyboard accessible
- Proper semantic HTML structure with headings, lists, and landmarks
- ARIA attributes where native HTML is insufficient

### 6. Theme Color Scheme

**Description**: The navy bluish tech-themed color palette applied consistently throughout the site

**Fields**:
- primaryColor: Main brand color (navy blue)
- secondaryColor: Supporting color
- accentColors: Additional colors for highlights and emphasis
- backgroundColors: Light and dark mode background options
- textColors: Text color options for different contexts

**Validation Rules**:
- Primary color must be a shade of navy blue
- All colors must maintain proper contrast ratios
- Color palette must work in both light and dark modes
- Color usage must be consistent across all components