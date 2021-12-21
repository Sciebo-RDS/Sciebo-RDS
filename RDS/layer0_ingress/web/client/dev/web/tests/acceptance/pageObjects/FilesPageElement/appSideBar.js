/* eslint-disable no-unused-expressions */
const util = require('util')
const _ = require('lodash')
const timeoutHelper = require('../../helpers/timeoutHelper')

module.exports = {
  commands: {
    isThumbnailVisible: function() {
      return this.waitForElementVisible(
        this.api.page.personalPage().elements.sideBar
      ).waitForElementVisible(this.elements.sidebarThumbnail)
    },
    closeSidebar: function(timeout = null) {
      timeout = timeoutHelper.parseTimeout(timeout)
      try {
        this.click({
          selector: '@sidebarCloseBtn',
          timeout: timeout
        })
      } catch (e) {
        // do nothing
      }
      return this.api.page.FilesPageElement.filesList()
    },
    selectAccordionItem: async function(item) {
      await this.waitForElementVisible(this.api.page.personalPage().elements.sideBar)
      const expanded = await this.isAccordionItemExpanded(
        item,
        this.api.globals.waitForNegativeConditionTimeout
      )
      if (!expanded) {
        this.useXpath()
          .initAjaxCounters()
          .click(this.getXpathOfLinkToAccordionItemInSidePanel(item))
          .waitForOutstandingAjaxCalls()
          .useCss()
      }
      const panelName = item === 'people' ? 'collaborators' : item
      const element = this.elements[panelName + 'Panel']
      const selector = element.selector + ' > .oc-accordion-content:not(:empty)'
      return this.waitForElementVisible(selector)
    },
    /**
     * return the complete xpath of the link to the specified accordion item in the side-bar
     * @param item
     * @returns {string}
     */
    getXpathOfLinkToAccordionItemInSidePanel: function(item) {
      return (
        this.api.page.personalPage().elements.sideBar.selector +
        util.format(this.elements.linkToOpenAccordionItem.selector, item)
      )
    },
    getVisibleAccordionItems: async function() {
      const items = []
      let elements
      await this.api.elements('@accordionItems', function(result) {
        elements = result.value
      })
      for (const { ELEMENT } of elements) {
        await this.api.elementIdText(ELEMENT, function(result) {
          items.push(result.value.toLowerCase())
        })
      }
      return items
    },
    getVisibleActionsMenuItems: async function() {
      const items = []
      let elements
      await this.api.elements('@actionPanelItems', function(result) {
        elements = result.value
      })
      for (const { ELEMENT } of elements) {
        await this.api.elementIdText(ELEMENT, function(result) {
          items.push(result.value.toLowerCase())
        })
      }
      return items
    },
    getActionsMenuItemsExceptDefaults: async function() {
      const defaultItems = ['mark as favorite', 'copy', 'move', 'rename', 'delete']
      const items = []
      let elements
      await this.api.elements('@actionPanelItems', function(result) {
        elements = result.value
      })
      for (const { ELEMENT } of elements) {
        await this.api.elementIdText(ELEMENT, function(result) {
          let notDefault = true
          for (const item of defaultItems) {
            if (_.isEqual(item, result.value.toLowerCase())) {
              notDefault = false
              break
            }
          }
          notDefault ? items.push(result.value.toLowerCase()) : null
        })
      }
      return items
    },
    isAccordionItemExpanded: async function(panelName, timeout = null) {
      panelName = panelName === 'people' ? 'collaborators' : panelName
      const element = this.elements[panelName + 'Panel']
      const selector = element.selector + ' > .oc-accordion-content:not(:empty)'
      let isVisible = false
      timeout = timeoutHelper.parseTimeout(timeout)
      await this.isVisible({ locateStrategy: 'css selector', selector, timeout }, result => {
        isVisible = result.status === 0
      })
      return isVisible
    },
    /**
     * checks if the item with the given selector is present on the files-page-sidebar
     *
     * @param {object} selector
     * @returns {Promise<boolean>}
     */
    isAccordionItemPresent: async function(selector) {
      let isPresent = true
      await this.useXpath()
        .waitForElementVisible(this.api.page.personalPage().elements.sideBar) // sidebar is expected to be opened and visible
        .api.elements(selector, result => {
          isPresent = result.value.length > 0
        })
        .useCss()
      return isPresent
    },
    /**
     * @returns {Promise<boolean>}
     */
    isLinksAccordionItemPresent: function() {
      return this.isAccordionItemPresent(this.elements.linksAccordionItem)
    },
    /**
     * @returns {Promise<boolean>}
     */
    isCollaboratorsAccordionItemPresent: function() {
      return this.isAccordionItemPresent(this.elements.collaboratorsAccordionItem)
    },
    markFavoriteSidebar: function() {
      return this.useXpath()
        .waitForElementVisible(this.api.page.personalPage().elements.sideBar)
        .waitForElementVisible('@favoriteStarDimm')
        .click('@sidebarToggleFavoriteButton')
        .waitForElementVisible('@favoriteStarShining')
    },
    unmarkFavoriteSidebar: function() {
      return this.waitForElementVisible(this.api.page.personalPage().elements.sideBar)
        .waitForElementVisible('@favoriteStarShining')
        .click('@sidebarToggleFavoriteButton')
        .waitForElementVisible('@favoriteStarDimm')
    }
  },
  elements: {
    /**
     * path from inside the side-bar
     */
    linkToOpenAccordionItem: {
      // the translate bit is to make it case-insensitive
      selector:
        "//button[contains(translate(.,'ABCDEFGHJIKLMNOPQRSTUVWXYZ','abcdefghjiklmnopqrstuvwxyz'),'%s')]",
      locateStrategy: 'xpath'
    },
    accordionItems: {
      selector:
        '//div[contains(@class, "oc-app-side-bar")]//div[@class="oc-accordion-item"]/h3/button',
      locateStrategy: 'xpath'
    },
    sidebarThumbnail: {
      selector: '.sidebar-title .oc-icon'
    },
    sidebarCloseBtn: {
      selector: '//div[contains(@class, "oc-app-side-bar")]//div[@class="action"]//button',
      locateStrategy: 'xpath'
    },
    collaboratorsAccordionItem: {
      selector: '#app-sidebar-sharing-item'
    },
    linksAccordionItem: {
      selector: '#app-sidebar-links-item'
    },
    sidebarToggleFavoriteButton: {
      selector: '#files-sidebar-star-icon'
    },
    favoriteStarDimm: {
      selector: '.oc-star-dimm'
    },
    favoriteStarShining: {
      selector: '.oc-star-shining'
    },
    versionsPanel: {
      selector: '#app-sidebar-versions-item'
    },
    collaboratorsPanel: {
      selector: '#app-sidebar-sharing-item'
    },
    linksPanel: {
      selector: '#app-sidebar-links-item'
    },
    actionsPanel: {
      selector: '#app-sidebar-actions-item'
    },
    actionPanelItems: {
      selector:
        '//div[@class="oc-accordion-content"]//li/button/span[@class="oc-files-actions-sidebar-action-label"] | //div[@class="oc-accordion-content"]//li/a/span[@class="oc-files-actions-sidebar-action-label"]',
      locateStrategy: 'xpath'
    },
    detailsPanel: {
      selector: '#app-sidebar-details-item'
    }
  }
}
