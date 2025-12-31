// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

// Load environment variables from .env file
require('dotenv').config();

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'AI-Native Textbook Platform for Physical AI and Humanoid Robotics Education',
  favicon: 'img/OIP.webp',
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },
  url: 'https://TehreemFatimaTF.github.io', // Replace with your GitHub Pages URL
  baseUrl: '/', // GitHub Pages subdirectory for this project
  organizationName: 'TehreemFatimaTF', // Usually your GitHub org/user name.
  projectName: 'physical-ai-robotics-textbook',
  onBrokenLinks: 'throw',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
     navbar: {
  title: 'Physical AI & Humanoid Robotics Textbook',
  logo: {
    alt: 'Physical AI & Humanoid Robotics Logo',
    src: 'img/OIP.webp',
  },
  items: [
    {
      type: 'docSidebar',
      sidebarId: 'tutorialSidebar',
      position: 'left',
      label: 'Book',
    },
    
    {
      href: 'https://github.com/your-username/MY-HACKATHON',
      label: 'GitHub',
      position: 'right',
    },
  ],
},

      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Modules',
            items: [
              {
                label: 'ROS 2',
                to: '/docs/module-1-ros2/chapter-1-intro-ros2',
              },
              {
                label: 'Digital Twin',
                to: '/docs/module-2-digital-twin/chapter-1-physics-simulation',
              },
              {
                label: 'NVIDIA Isaac',
                to: '/docs/module-3-nvidia-isaac/chapter-1-isaac-sim',
              },
              {
                label: 'VLA Humanoids',
                to: '/docs/module-4-vla-humanoids/chapter-1-voice-to-action',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'Blog',
                to: '/blog',
              },
              {
                label: 'GitHub',
                href: 'https://github.com/your-username/MY-HACKATHON',
              },
            ],
          },
        ],
                copyright: ` Copyright � 2025 Physical AI & Humanoid Robotics Textbook, Built with ❤️ by Tehreem Fatima.`

      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
      // Add environment variables to be available in the browser
      // These will be replaced at build time
      firebaseConfig: {
        apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "AIzaSyDimxaQNxOqtT-BvG9x_7E13jIWXo1Pbk8",
        authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "my-docusaurus-site.firebaseapp.com",
        projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "my-docusaurus-site",
        storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "my-docusaurus-site.firebasestorage.app",
        messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "812534412214",
        appId: process.env.REACT_APP_FIREBASE_APP_ID || "1:812534412214:web:9eaacd21ead0afae8d8717",
        measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID || "G-KGJ96XLC0G",
      }
    })
  }
export default config;

