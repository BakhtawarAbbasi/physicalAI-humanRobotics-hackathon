# Research: Cleanup & Landing Page UI Upgrade — ai-book

**Date**: 2025-12-17
**Feature**: 001-ui-upgrade
**Status**: Complete

## Research Tasks Completed

### 1. Docusaurus Content Cleanup Process

**Decision**: Remove tutorial-basics, tutorial-extras, and blog directories; disable blog in config

**Rationale**: Following Docusaurus best practices for removing default content while maintaining site functionality

**Approach**:
- Delete `docs/tutorial-basics/` directory and its contents
- Delete `docs/tutorial-extras/` directory and its contents
- Delete or disable `blog/` directory
- Update `docusaurus.config.js` to remove blog plugin if needed
- Update sidebar configuration to remove references to deleted content

**Alternatives considered**:
- Keep content but hide via CSS (rejected - increases bundle size unnecessarily)
- Move content to separate branch (rejected - unnecessary complexity for cleanup)

### 2. Docusaurus Theme Customization for Navy Bluish Tech Theme

**Decision**: Use Docusaurus theme customization via CSS variables and custom CSS

**Rationale**: Docusaurus provides built-in theme customization capabilities that allow for consistent color schemes across the site

**Approach**:
- Define navy bluish color palette in CSS variables
- Customize primary, secondary, success, and other color tokens
- Apply theme consistently across all site components
- Ensure WCAG AA compliance for accessibility
- Test on multiple devices and browsers

**Alternatives considered**:
- Create custom theme component (rejected - overkill for color changes)
- Use third-party Docusaurus themes (rejected - need custom branding)

### 3. Landing Page Redesign with Feature Cards

**Decision**: Redesign homepage using Docusaurus's built-in HomepageFeatures component pattern

**Rationale**: Docusaurus provides flexible homepage customization options that work well with the existing framework

**Approach**:
- Create custom homepage component in `src/pages/index.js`
- Implement three feature cards with specified titles:
  1. Physical AI & Embodied Intelligence
  2. Humanoid Robotics & Simulation
  3. AI-to-Physical World Integration
- Ensure responsive design using Docusaurus's built-in responsive utilities
- Apply navy bluish theme consistently to cards

**Alternatives considered**:
- Use external homepage templates (rejected - want to maintain Docusaurus integration)
- Complex animations/interactions (rejected - focus on content and readability)

### 4. Responsive Design and Accessibility Implementation

**Decision**: Use Docusaurus's built-in responsive utilities and follow WCAG guidelines

**Rationale**: Docusaurus is built on React and provides responsive utilities out of the box

**Approach**:
- Use Docusaurus's responsive classes for mobile/tablet/desktop
- Implement proper contrast ratios for navy bluish theme (minimum 4.5:1 for normal text)
- Add proper ARIA labels and semantic HTML
- Test with screen readers and keyboard navigation
- Optimize for performance with minimal custom CSS

**Alternatives considered**:
- Custom responsive framework (rejected - redundant with Docusaurus capabilities)
- Complex accessibility overlays (rejected - better to implement proper semantic HTML)

### 5. Build Process Validation

**Decision**: Use standard Docusaurus build process with validation steps

**Rationale**: Standard Docusaurus build process is well-tested and reliable

**Approach**:
- Run `npm run build` to generate static site
- Verify all links work correctly after content removal
- Check that custom theme is applied consistently
- Validate performance metrics (load time < 3 seconds)
- Test on multiple browsers and devices

**Alternatives considered**:
- Custom build process (rejected - unnecessary complexity)
- Multiple build configurations (rejected - single optimized build sufficient)

## Key Findings

1. **Docusaurus Configuration**: The `docusaurus.config.js` file is the central place for theme customization and plugin management.

2. **CSS Customization**: Docusaurus supports CSS variables for theming, which is ideal for implementing the navy bluish color scheme consistently.

3. **Homepage Customization**: The default Docusaurus homepage can be completely replaced by creating a custom `src/pages/index.js` file.

4. **Sidebar Management**: The `sidebars.js` file controls navigation structure and needs to be updated after removing documentation sections.

5. **Performance Considerations**: Docusaurus generates optimized static sites, but custom CSS should be kept minimal to maintain performance.

## Implementation Risks and Mitigations

1. **Risk**: Broken links after removing default content
   - **Mitigation**: Thorough testing after content removal, updating any internal links

2. **Risk**: Theme not displaying correctly across browsers
   - **Mitigation**: Cross-browser testing and using well-supported CSS features

3. **Risk**: Performance degradation from custom CSS
   - **Mitigation**: Minimal, optimized CSS and performance testing

4. **Risk**: Accessibility issues with new color scheme
   - **Mitigation**: Contrast ratio validation and accessibility testing tools