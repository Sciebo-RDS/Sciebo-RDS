export default {
  currentFolder: null,
  files: [],
  filesSearched: [],
  selected: [],
  inProgress: [],
  searchTermGlobal: '',
  davProperties: [
    '{http://owncloud.org/ns}permissions',
    '{http://owncloud.org/ns}favorite',
    '{http://owncloud.org/ns}fileid',
    '{http://owncloud.org/ns}owner-id',
    '{http://owncloud.org/ns}owner-display-name',
    '{http://owncloud.org/ns}share-types',
    '{http://owncloud.org/ns}privatelink',
    '{DAV:}getcontentlength',
    '{http://owncloud.org/ns}size',
    '{DAV:}getlastmodified',
    '{DAV:}getetag',
    '{DAV:}resourcetype',
    '{http://owncloud.org/ns}downloadURL'
  ],
  dropzone: false,
  shareOpen: null,
  versions: [],

  /**
   * Outgoing shares and links from currently highlighted element
   */
  currentFileOutgoingShares: [],
  currentFileOutgoingSharesError: null,
  currentFileOutgoingSharesLoading: false,

  /**
   * Incoming shares from currently highlighted element
   */
  incomingShares: [],
  incomingSharesError: null,
  incomingSharesLoading: false,

  /**
   * Shares from parent folders
   **/
  sharesTree: {},
  sharesTreeError: null,
  sharesTreeLoading: false,

  loadingFolder: false,
  highlightedResourceId: null,
  publicLinkPassword: null,
  uploaded: [],
  actionsInProgress: [],

  /**
   * Right sidebar
   */
  appSidebarExpandedAccordion: null,
  appSidebarAccordionContext: null,

  /**
   * Public links
   */
  publicLinkInEdit: {
    id: null,
    name: '',
    permissions: 1,
    hasPassword: false,
    expireDate: null
  },

  /**
   * Pagination
   */
  currentPage: 1,
  filesPageLimit: 100,

  /**
   * View settings
   */
  areHiddenFilesShown: true
}
