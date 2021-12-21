let numAjaxRequestsStart = 0
let start = 0
let end = 0
const sleepWhenNoNewAjaxCallsStarted = function(result) {
  const currentTime = Date.now()
  if (result.value <= numAjaxRequestsStart && currentTime < end) {
    this.pause(this.globals.waitForConditionPollInterval)
    checkSumStartedAjaxRequests(this)
  }
  if (currentTime >= end) {
    console.error('Timeout waiting for Ajax calls to start')
  }
}

const checkSumStartedAjaxRequests = function(api) {
  api.execute('return window.sumStartedAjaxRequests', [], sleepWhenNoNewAjaxCallsStarted)
}
exports.command = function() {
  // init the ajax counters if they haven't been initialized yet
  this.execute('return (typeof window.sumStartedAjaxRequests === "undefined")', [], function(
    result
  ) {
    if (result.value === true) {
      this.initAjaxCounters()
    }
  })

  this.execute('return window.sumStartedAjaxRequests', [], function(result) {
    numAjaxRequestsStart = result.value
  })
  start = Date.now()
  end = start + this.globals.waitForNegativeConditionTimeout
  checkSumStartedAjaxRequests(this)
  this.waitForOutstandingAjaxCalls()
}
