document.addEventListener('DOMContentLoaded', ()=>{

    
    let form = document.querySelector('form');
    form.addEventListener('submit', ()=>{
        //call to spinner when login
        spinner();
    })
})


/**
 * Spinner function for login
 */
function spinner(){
    const login_button = document.querySelector('#btn-login');
    login_button.innerHTML = '';
    login_button.innerHTML = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">Cargando...</span>
    ` ;
    login_button.disabled = true;
}