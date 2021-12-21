/**
 * Takes an object from state and creates a copy of it with only the values (no watchers, etc.)
 * Editing the copied object does not result in errors due to modifying the state.
 * The copied object is still reactive.
 * @param {Object} state Object in the state to be copied
 * @return {Object} Copied object
 */
export function cloneStateObject(state) {
  return JSON.parse(JSON.stringify(state))
}
