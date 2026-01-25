import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'PhysicalAI Book',
  tagline: 'Learn about Physical AI and Humanoid Robotics Book',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://physical-ai-human-robotics-hackatho-ebon.vercel.app/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-username', // Usually your GitHub org/user name.
  projectName: 'ai-book', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'physicalAI',
      logo: {
        alt: 'physicalAI Book Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Intro',
        },
        {
          type: 'docSidebar',
          sidebarId: 'module01Sidebar',
          position: 'left',
          label: 'Module 1',
        },
        {
          type: 'docSidebar',
          sidebarId: 'module02Sidebar',
          position: 'left',
          label: 'Module 2',
        },
        {
          type: 'docSidebar',
          sidebarId: 'module03Sidebar',
          position: 'left',
          label: 'Module 3',
        },
        {
          type: 'docSidebar',
          sidebarId: 'module04Sidebar',
          position: 'left',
          label: 'Module 4',
        },

        {
          href: 'https://github.com/BakhtawarAbbasi/physicalAI-humanRobotics-hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Module 1 - Physical AI & Embodied Intelligence',
              to: '/docs/module-01/chapter-1-ros2-fundamentals',
            },
            {
              label: 'Module 2 - Humanoid Robotics & Simulation',
              to: '/docs/module-02/chapter-1-gazebo-physics',
            },
            {
              label: 'Module 3 - AI-to-Physical World Integration',
              to: '/docs/module-03/isaac-sim',
            },
            {
              label: 'Module 4 - Voice to Action & Cognitive Planning',
              to: '/docs/module-04/voice-to-action',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'GitHub Repository',
              href: 'https://github.com/BakhtawarAbbasi/physicalAI-humanRobotics-hackathon',
            },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/bakhtawar-abbasi-59ba15304/',
            },
            {
              label: 'Twitter/X',
              href: 'https://x.com/Bakhtawar160419',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,

  // Add the Root component to wrap the entire app
  themes: [],
  stylesheets: [],

    // Client modules to load
  clientModules: [
    './src/Root.tsx',
  ],

  // Additional configuration
  headTags: [
    // Add meta tag for API URL
    {
      tagName: 'meta',
      attributes: {
        name: 'chatbot-api-url',
        content: 'http://localhost:8000',
      },
    },
    // Add inline script to set the API URL globally
    {
      tagName: 'script',
      attributes: { type: 'text/javascript' },
      innerHTML: `
        if (typeof window !== 'undefined') {
          window.chatbotConfig = {
            apiBaseUrl: 'http://localhost:8000'
          };
        }
      `,
    },
  ],
};

export default config;
