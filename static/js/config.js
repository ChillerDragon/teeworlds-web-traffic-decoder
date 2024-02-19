// lololol not used

const urlParams = new URLSearchParams(document.location.search)

/**
 * Object holding the config and defining the defaults
 * all properties can be overwritten with query parameters
 *
 * @property {string} v nothing separated teeworlds protocol versions
 *                      for example "6" or "7" or "67"
 * @property {string} d input hexdump data for decoding
 */
const globalConfig = {
  v: '67',
  d: ''
}

Object.keys(globalConfig).forEach((configKey) => {
  if (urlParams.get(configKey)) {
    globalConfig[configKey] = urlParams.get(configKey)
  }
})

console.log('loaded config:')
console.log(globalConfig)

/**
 * update url to make the current state sharable via link
 *
 * @param {string} key
 * @param {string} value
 */
const setQueryParam = (key, value) => {
  if(!value) {
    return
  }
  urlParams.set(key, value)
  // window.location.search = urlParams
  // window.history.pushState('teeworlds traffic decoder', '', urlParams)
  window.history.replaceState({}, '', `${location.pathname}?${urlParams}`)
}

const checkProt6 = document.querySelector('#protocol-6')
const checkProt7 = document.querySelector('#protocol-7')
if (globalConfig['v']) {
  if(globalConfig['v'].includes('6')) {
    checkProt6.checked = true
  } else {
    checkProt6.checked = false
  }
  if(globalConfig['v'].includes('7')) {
    checkProt7.checked = true
  } else {
    checkProt7.checked = false
  }
}

[checkProt6, checkProt7].forEach((checkbox) => {
  checkbox.addEventListener('change', () => {
    let versions = []
    if (checkProt6.checked) {
      versions.push('6')
    }
    if (checkProt7.checked) {
      versions.push('7')
    }
    setQueryParam('v', versions.join(''))
  })
})
