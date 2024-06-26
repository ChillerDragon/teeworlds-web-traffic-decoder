const input = document.querySelector('#data')
const outputs = document.querySelector('.outputs')
const output1 = document.querySelector('.output-01')
const form = document.querySelector('form')
const flashesAlertDom = document.querySelector('.flashes-alert')
const flashesInfoDom = document.querySelector('.flashes-info')
let flashIdCounter = 0

/**
 * Show red flash on the top of the html page
 *
 * @param {string} msg
 */
const addFlashAlert = (msg) => {
  const maxFlashes = 6
  const numFlashes = document.querySelectorAll('.flash-alert').length

  if (numFlashes >= maxFlashes) {
    document.querySelector('.flash-alert').remove()
  }
  flashIdCounter++
  const flashId = `flash-${flashIdCounter}`
  const flashDiv = `
    <div class="flash flash-alert" id="${flashId}">
      <p>${msg}</p>
      <div class="flash-close">x</div>
    </div>
  `
  flashesAlertDom.insertAdjacentHTML('beforeend', flashDiv)
  const flashDom = document.querySelector(`#${flashId}`)
  flashDom.addEventListener('click', () => flashDom.remove())
}

/**
 * fetch backend with data from form
 * and create div with response
 *
 * @param {FormData} formData
 * @param {string} outputName Class name of the output div.
 *                            Will be created if it does not exist already
 *
 * @returns {string|null} the extracted udp payload bytes as hexstring
 */
const fetchToBox = async (formData, outputName) => {
  const options = {
    method: 'POST',
    body: formData
  }
  const response = await fetch(form.action, options)
  const data = await response.json()

  if (data.message) {
    const outputDiv = document.querySelector(`.${outputName}`)
    if (!outputDiv) {
      outputs.insertAdjacentHTML('beforeend', `<div class="${outputName} code-snippet delete-me">${data.message}</div>`)
    } else {
      outputDiv.innerHTML = data.message
    }
  } else {
    console.warn(data)
    if (data.error) {
      addFlashAlert(data.error)
    }
    return null
  }

  if (data.bytes) {
    return data.bytes
  } else if (data.bytes !== '') {
    console.warn("no bytes in response")
    console.warn(data)
  }
  return null
}

const decode = async () => {
  const formData = new FormData(form)
  const tcpdumpSplits = getTcpDumpSplits(input.value)

  const deleteMes = document.querySelectorAll('.delete-me')
  deleteMes.forEach((deleteMe) => deleteMe.remove())

  if (tcpdumpSplits) {
    let i = 0
    for(const split of tcpdumpSplits) {
      i++
      if (i >= 19) {
        console.warn('Maximum number of tcpdump splits reached. Ignoring the rest.')
        break
      }
      formData.set('data', split)
      const bytes = await fetchToBox(formData, `output-${String(i).padStart(2, '0')}`)
      setQueryParam('d', bytes) // TODO: sum up
    }
  } else {
    const bytes = await fetchToBox(formData, 'output-01')
    setQueryParam('d', bytes)
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  decode()
})

input.addEventListener('keyup', () => {
  decode()
})

if (globalConfig['d']) {
  input.value = globalConfig['d']
  decode()
}
