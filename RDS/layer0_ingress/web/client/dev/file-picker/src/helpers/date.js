import { DateTime } from 'luxon'
import Vue from 'vue'

// TODO: Investiage if we can set language manually
// Getting the browser set language is not a good UX
// Passing as a prop doesn't seem like a nice solution

export function formDateFromNow(date) {
  const locale = Vue.config.language.replace('cs_CZ', 'cs')

  return DateTime.fromJSDate(new Date(date)).setLocale(locale).toRelative()
}
