
    let copyUrl = document.querySelector('#copyUrl')

    copyUrl.addEventListener('click', ()=>{

        if (navigator && navigator.clipboard && navigator.clipboard.writeText)
          return navigator.clipboard.writeText(document.querySelector('#urlGenerated').value);
        return Promise.reject("The Clipboard API is not available.");
    })
