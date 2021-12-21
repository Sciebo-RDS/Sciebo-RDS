import mutations from '../../../src/store/mutations'
import { cloneDeep } from 'lodash-es'

const stateFixture = {
  files: [
    {
      id: 1,
      name: 'test1'
    },
    {
      id: 2,
      name: 'test2'
    },
    {
      id: 5,
      name: 'test5'
    }
  ]
}
let stateMock = {}
const resetState = () => {
  stateMock = cloneDeep(stateFixture)
}

describe('vuex store mutations', () => {
  describe('update resources by id', () => {
    beforeEach(resetState)
    it.each([
      [mutations.UPSERT_RESOURCE.name, mutations.UPSERT_RESOURCE],
      [mutations.UPDATE_RESOURCE.name, mutations.UPDATE_RESOURCE]
    ])('succeeds using mutation %s', (name, m) => {
      expect(stateMock.files).toEqual(stateFixture.files)
      expect(stateMock.files[1].name).toBe('test2')
      m(stateMock, {
        id: 2,
        name: 'test2-updated'
      })
      expect(stateMock.files[1].name).toBe('test2-updated')
      expect(stateMock.files.length).toBe(stateFixture.files.length)
    })
  })
  describe('insert resources', () => {
    beforeEach(resetState)
    it('succeeds using mutation UPSERT_RESOURCE', () => {
      expect(stateMock.files).toEqual(stateFixture.files)
      mutations.UPSERT_RESOURCE(stateMock, {
        id: 3,
        name: 'test3-inserted'
      })
      expect(stateMock.files).toEqual([...stateFixture.files, { id: 3, name: 'test3-inserted' }])
    })
    it('is ignored using mutation UPDATE_RESOURCE', () => {
      expect(stateMock.files).toEqual(stateFixture.files)
      mutations.UPDATE_RESOURCE(stateMock, {
        id: 3,
        name: 'test3-inserted'
      })
      expect(stateMock.files).toEqual(stateFixture.files)
    })
  })

  it('SET_HIDDEN_FILES_VISIBILITY', () => {
    const state = { areHiddenFilesShown: true }
    const { SET_HIDDEN_FILES_VISIBILITY } = mutations

    SET_HIDDEN_FILES_VISIBILITY(state, false)

    expect(state.areHiddenFilesShown).toEqual(false)
  })

  it('sets the files page limit', () => {
    const state = { filesPageLimit: 100 }
    const { SET_FILES_PAGE_LIMIT } = mutations

    SET_FILES_PAGE_LIMIT(state, 500)

    expect(state.filesPageLimit).toEqual(500)
    expect(window.localStorage.getItem('oc_filesPageLimit')).toEqual('500')
  })
})
