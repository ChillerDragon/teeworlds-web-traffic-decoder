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
  }
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
      await fetchToBox(formData, `output-${String(i).padStart(2, '0')}`)
    }
  } else {
    fetchToBox(formData, 'output-01')
  }
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  decode()
})

input.addEventListener('keyup', () => {
  decode()
})
