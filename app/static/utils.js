window.onbeforeunload = function() { return "Are you sure you want to go back? Your data will not be saved..."; }


// next
async function next(subject_id, subject_condition, results, message = 'Thanks for completing that experiment. Click `next` to move on to the next event.') {
    window.onbeforeunload = false
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            subject_id: subject_id,
            subject_condition: subject_condition,
            results: results
        })
    }

    const resp = await fetch('/_next_', options)
    const resp_data = await resp.json()
    window.location = resp_data['next_page']

}