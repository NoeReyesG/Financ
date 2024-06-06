document.addEventListener('DOMContentLoaded',()=>{
    console.log("Hola1");
   
})

let save = false;

/**
 * Funcion para habilitar la edición de los campos del cliente.
 * @param {*} event 
 */
function editar(event){
    if (save){
        save = !save;
    }
    else{
        event.preventDefault();

        submitButton = document.querySelector('#editar-btn');
        submitButton.innerHTML='';
        submitButton.innerHTML='Guardar cambios';
        console.log("2");
        inputs = document.querySelectorAll('#cliente input');
        inputs.forEach(input => {
            input.disabled = false;
        });
        save = !save;
    }
}

function agregar_pedido(e){
    e.preventDefault();
    console.log("ojo aquí");
}

/**
 * Funcion para verificar si el abono que se quiere realizar si se puede aplicar al pago antes de hacerlo,
 * es decir, deuda >= pago (por implementar)
 * @param {*} e 
 */
function nuevo_pago(e){
    e.preventDefault();
   
    const form = e.target
    let balance = form.dataset.balance;
    let pedido_id = form.dataset.pedidoid;
    abono = form.querySelector('input[type="number"]').value;

    if (parseInt(balance) >= parseInt(abono)){
        form.submit();
    }
    else{
        console.log("El importe es mayor a la deuda");
    }

   

    
    //const data = new FormData(e.target);
    //console.log([...data.entries()]);
}

async function aplicarPago(){

}