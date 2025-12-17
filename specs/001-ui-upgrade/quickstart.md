# Quickstart Guide: Cleanup & Landing Page UI Upgrade — ai-book

**Date**: 2025-12-17
**Feature**: 001-ui-upgrade
**Status**: Complete

## Overview

This guide provides the essential steps to implement the UI upgrade for the Physical AI & Humanoid Robotics book website. The process involves removing default Docusaurus content and implementing a professional navy bluish tech theme with redesigned landing page feature cards.

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager
- Git for version control
- A code editor of your choice

## Setup and Installation

### 1. Clone and Prepare the Repository

```bash
# Navigate to your project directory
cd your-project-directory

# Ensure you're on the correct branch
git checkout 001-ui-upgrade
```

### 2. Install Dependencies

```bash
# Install project dependencies
npm install
# OR if using yarn
yarn install
```

### 3. Verify Current Setup

```bash
# Start the development server to verify current state
npm run start
# The site should be accessible at http://localhost:3000
```

## Implementation Steps

### Step 1: Remove Default Content

1. **Delete tutorial-basics directory**:
   ```bash
   rm -rf docs/tutorial-basics/
   ```

2. **Delete tutorial-extras directory**:
   ```bash
   rm -rf docs/tutorial-extras/
   ```

3. **Remove or disable blog directory**:
   ```bash
   # Option A: Remove the blog directory completely
   rm -rf blog/

   # Option B: If you want to keep the directory but disable the blog,
   # skip the removal and update the config in the next step
   ```

### Step 2: Update Docusaurus Configuration

1. **Edit `docusaurus.config.js`** to remove blog plugin and update theme:

```javascript
// Update the plugins array to remove blog plugin if you didn't delete the directory
// plugins: [
//   // Remove ['@docusaurus/plugin-content-blog', {...}] if present
//   // Keep other plugins
// ],

// Add or update the theme configuration for navy bluish theme
themeConfig: {
  colorMode: {
    defaultMode: 'light',
    disableSwitch: false,
    respectPrefersColorScheme: true,
  },
  navbar: {
    // Your navbar configuration
  },
  footer: {
    // Your footer configuration
  },
  prism: {
    theme: require('prism-react-renderer/themes/github'),
    darkTheme: require('prism-react-renderer/themes/dracula'),
  },
  // Custom colors for navy bluish theme
  customCss: require('path').join(__dirname, 'src/css/custom.css'),
},
```

### Step 3: Create Navy Bluish Theme

1. **Create or update `src/css/custom.css`**:

```css
/* Navy Bluish Tech Theme */
:root {
  --ifm-color-primary: #1a365d;        /* Navy blue primary */
  --ifm-color-primary-dark: #152a48;   /* Darker navy */
  --ifm-color-primary-darker: #12243e; /* Even darker navy */
  --ifm-color-primary-darkest: #0d182a; /* Darkest navy */
  --ifm-color-primary-light: #2d4c74;  /* Lighter navy */
  --ifm-color-primary-lighter: #395c8a; /* Even lighter */
  --ifm-color-primary-lightest: #4a70a1; /* Lightest navy */
  --ifm-code-font-size: 95%;
}

/* Responsive adjustments */
@media (max-width: 996px) {
  :root {
    --ifm-navbar-height: 60px;
  }
}

/* Card styling for feature cards */
.hero-card {
  background: var(--ifm-color-emphasis-100);
  border-radius: 8px;
  padding: 2rem;
  margin: 1rem 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hero-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Accessibility improvements */
.navbar-sidebar__backdrop {
  backdrop-filter: blur(4px);
}

/* Custom button styles */
.button--primary {
  background-color: var(--ifm-color-primary);
  border-color: var(--ifm-color-primary);
}

.button--primary:hover {
  background-color: var(--ifm-color-primary-light);
  border-color: var(--ifm-color-primary-light);
}
```

### Step 4: Redesign Landing Page

1. **Create or update `src/pages/index.js`**:

```javascript
import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Physical AI & Humanoid Robotics Book Documentation">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {/* Feature Card 1 */}
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h2>Physical AI & Embodied Intelligence</h2>
                  <p>
                    Explore the intersection of artificial intelligence and physical systems.
                  </p>
                </div>
              </div>

              {/* Feature Card 2 */}
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h2>Humanoid Robotics & Simulation</h2>
                  <p>
                    Learn about humanoid robot design, control systems, and simulation environments.
                  </p>
                </div>
              </div>

              {/* Feature Card 3 */}
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h2>AI-to-Physical World Integration</h2>
                  <p>
                    Understand how AI systems interact with and control physical environments.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
```

### Step 5: Update Sidebar Configuration

1. **Edit `sidebars.js`** to remove references to deleted content:

```javascript
// Remove any references to tutorial-basics and tutorial-extras
module.exports = {
  docs: [
    // Keep only the documentation sections that remain
    // Remove any references to:
    // - 'tutorial-basics/...'
    // - 'tutorial-extras/...'
    // Keep your Physical AI & Humanoid Robotics content
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics',
      items: [
        // Your book content here
      ],
    },
  ],
};
```

### Step 6: Validate Implementation

1. **Test the site locally**:
   ```bash
   npm run start
   ```

2. **Build the site to verify production build**:
   ```bash
   npm run build
   ```

3. **Serve the build locally to test**:
   ```bash
   npm run serve
   ```

## Verification Checklist

- [ ] Tutorial-basics directory removed
- [ ] Tutorial-extras directory removed
- [ ] Blog directory removed or disabled
- [ ] Navy bluish theme applied consistently
- [ ] Landing page shows three feature cards with correct titles
- [ ] Responsive design works on mobile, tablet, and desktop
- [ ] All existing content remains accessible
- [ ] Site builds without errors
- [ ] Navigation structure updated to remove deleted content
- [ ] Color contrast meets WCAG AA standards

## Troubleshooting

### Common Issues

1. **Missing content after deletion**: Verify that you only removed default Docusaurus content, not the Physical AI & Humanoid Robotics book content.

2. **Theme not applying**: Check that `custom.css` is properly referenced in `docusaurus.config.js`.

3. **Build errors**: Run `npm run build` to see detailed error messages and address them accordingly.

4. **Navigation broken**: Verify that `sidebars.js` only references existing content paths.

## Next Steps

After completing this quickstart:
1. Test thoroughly on different devices and browsers
2. Review accessibility compliance using tools like axe-core
3. Optimize images and assets for performance
4. Prepare for deployment to production environment