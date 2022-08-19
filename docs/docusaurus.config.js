// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'My Site',
  tagline: 'Dinosaurs are cool',
  url: 'https://your-docusaurus-test-site.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'facebook', // Usually your GitHub org/user name.
  projectName: 'docusaurus', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  plugins: 
    [[
    'content-docs',
    /** @type {import('@docusaurus/plugin-content-docs').Options} */
    ({
      id: 'about',
      path: 'about',
      routeBasePath: 'about',
       /* editUrl: ({locale, versionDocsDirPath, docPath}) => {
        if (locale !== 'en') {
          return `https://crowdin.com/project/docusaurus-v2/${locale}`;
        }
        return `https://github.com/Sciebo-RDS/Sciebo-RDS${versionDocsDirPath}/${docPath}`;
      },
      editCurrentVersion: true,  */
      sidebarPath: require.resolve('./sidebarsAbout.js'),
    }),
    ],
  ], 
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Sciebo-RDS/Sciebo-RDS/docs',
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/Sciebo-RDS/Sciebo-RDS/docs',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Sciebo RDS',
        logo: {
          alt: 'My Site Logo',
          src: 'img/Sciebo_Logo.svg',
        },
        items: [
          {
            to: 'about',
            position: 'right',
            label: 'About',
          },
          {
            type: 'doc',
            docId: 'gettingstarted/start',
            position: 'right',
            label: 'Getting started',
          },
          {
            to: 'docs/documentation/configuration',
            position: 'right',
            label: 'Configuration',
          },
          {
            to: 'docs/documentation/development',
            position: 'right',
            label: 'Development',
          },
          {
            to: 'docs/documentation/reference',
            position: 'right',
            label: 'Reference',
          },/* 
          {to: '/blog', label: 'News', position: 'right'}, */
          {
            href: 'https://github.com/Sciebo-RDS/Sciebo-RDS',
            className: "header-github-link",
            "aria-label": "GitHub repository",
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Links',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/Sciebo-RDS/Sciebo-RDS',
              },
              {
                label: 'Issues',
                href: 'https://github.com/Sciebo-RDS/Sciebo-RDS/issues',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Github Discussions',
                href: 'https://github.com/Sciebo-RDS/Sciebo-RDS/discussions',
              },
            ],
          },
          {
            title: 'Contact',
            items: [
              {
                label: 'Imprint',
                to: '/imprint',
              },
              {
                label: 'Email',
                href: 'mailto:sciebo-rds@uni-muenster.de',
              },
            ],
          },
        ],
        copyright: `
        Sciebo RDS, 2019 - ${new Date().getFullYear()}<br/>
        Developed at <a href="http://uni-muenster.de">University of Münster</a>.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
