var instructions = {

    start: function(params, next) {
        instructions_div = document.createElement('div') 
        instructions_div.id = 'instructions_div'
        document.getElementById('main').appendChild(instructions_div)

        // Generate Objects
        continue_button = document.createElement('button')
        continue_button.id = 'continue'
        continue_button.appendChild(document.createTextNode('Next'))
        continue_button.addEventListener('click', function () {
            // destroy and continue
            instructions_div.innerHTML = ''
            next()
        })

        // add to DOM      
        txt = document.createElement('p')
        txt.id = 'instructions'
        txt.innerHTML = params['text']

  
        instructions_div.appendChild(txt)
        instructions_div.appendChild(document.createElement('br'))
        instructions_div.appendChild(document.createElement('br'))
        instructions_div.appendChild(continue_button)

        console.log('started instructions')
    }

}