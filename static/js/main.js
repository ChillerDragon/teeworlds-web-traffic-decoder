const input = document.querySelector('#data')
const output = document.querySelector('.output')
const form = document.querySelector('form')

const decode = () => {
  const data = input.value
  const options = {
    method: 'POST',
    body: new FormData(form)
  }
  fetch(form.action, options)
    .then(response => response.json())
    .then(data => {
      console.log(data)
      if (data.message) {
        output.innerHTML = data.message
      }
    })
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  decode()
})

input.addEventListener('keydown', () => {
  decode()
})
