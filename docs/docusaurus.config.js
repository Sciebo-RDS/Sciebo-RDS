// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");
const mdxMermaid = require("mdx-mermaid");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Sciebo-RDS",
  tagline: "Manage your research data",
  url: "https://www.research-data-services.org/",
  baseUrl: "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/Sciebo_Logo.svg",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "Sciebo-RDS", // Usually your GitHub org/user name.
  projectName: "Sciebo-RDS", // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  plugins: [],
  presets: [
    [
      "classic",
      {
        docs: {
          remarkPlugins: [mdxMermaid],
          routeBasePath: "/",
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/Sciebo-RDS/Sciebo-RDS/docs",
        },
        blog: {
          showReadingTime: true,
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl: "https://github.com/Sciebo-RDS/Sciebo-RDS/docs",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "Sciebo RDS",
        logo: {
          alt: "My Site Logo",
          src: "img/Sciebo_Logo.svg",
        },
        items: [
          {
            to: "/",
            position: "right",
            label: "About",
          },
          {
            type: "doc",
            docId: "gettingstarted/start",
            position: "right",
            label: "Getting started",
          },
          {
            to: "documentation/configuration",
            position: "right",
            label: "Configuration",
          },
          {
            to: "documentation/development",
            position: "right",
            label: "Development",
          },
          {
            to: "documentation/reference",
            position: "right",
            label: "Reference",
          } /* 
          {to: '/blog', label: 'News', position: 'right'}, */,
          {
            href: "https://github.com/Sciebo-RDS/Sciebo-RDS",
            className: "header-github-link",
            "aria-label": "GitHub repository",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Github",
            items: [
              {
                label: "ScieboRDS/ScieboRDS",
                href: "https://github.com/Sciebo-RDS/Sciebo-RDS",
              },
              {
                label: "Issues",
                href: "https://github.com/Sciebo-RDS/Sciebo-RDS/issues",
              },
              {
                label: "ScieboRDS/RDS-Connectors",
                href: "https://github.com/Sciebo-RDS/RDS-Connectors",
              },
            ],
          },
          {
            title: "Community",
            items: [
              {
                label: "Github Discussions",
                href: "https://github.com/Sciebo-RDS/Sciebo-RDS/discussions",
              },
            ],
          },
          {
            title: "Legal / Contact",
            items: [
              {
                label: "Imprint",
                to: "/imprint",
              },
              {
                label: "Email",
                href: "mailto:sciebo-rds@uni-muenster.de",
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
