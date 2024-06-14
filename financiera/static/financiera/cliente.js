document.addEventListener('DOMContentLoaded',()=>{
    console.log("Hola1");
   
})

var pedidos = []
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


function nuevo_articulo(event){
    event.preventDefault();
    let articulo = {}
    const data = new FormData(event.target);
    articulo['cantidad'] = data.get("cantidad");
    articulo['titulo'] = data.get("titulo");
    articulo['url'] = data.get('url');
    articulo['precio'] = data.get('precio');
    
    pedidos.unshift(articulo);
    console.log(pedidos);
    
}
/**
 * Function to set the order-id to the item that's been added to the order.
 * We pass the data from the button "Agregar articulo" (add item) to the button agregar (add)
 * inside the component, in this way we identified the order where the item must be placed.
 * 
 * @param {*} e 
 */
function setPedidoIdToModal(e){
    id =  e.target.dataset.pedido;
    console.log(id);
    document.querySelector("#btn-pedido").dataset.pedidoId=id;
}



async function aplicarPago(){

}