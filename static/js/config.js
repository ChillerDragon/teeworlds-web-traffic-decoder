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
