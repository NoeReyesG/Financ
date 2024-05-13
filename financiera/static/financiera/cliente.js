document.addEventListener('DOMContentLoaded',()=>{
    console.log("Hola1");
    
})

let save = false;

function editar(event){
    if (save){
        save = !save;
    }
    else{
        event.preventDefault();

        submitButton = document.querySelector('#editar-btn');
        submitButton.innerHTML='';
        submitButton.innerHTML='Guardar';
        console.log("2");
        inputs = document.querySelectorAll('#cliente input');
        inputs.forEach(input => {
            input.disabled = false;
            // input.style.backgroundColor= 'red';
        });
        save = !save;
    }
}