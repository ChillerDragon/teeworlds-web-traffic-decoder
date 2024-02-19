const input = document.querySelector('#data')
const outputs = document.querySelector('.outputs')
const output1 = document.querySelector('.output-01')
const form = document.querySelector('form')

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
