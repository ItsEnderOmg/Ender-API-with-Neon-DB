// // Definis la url q vas a estar usando, esta es la raiz
// const API_URL = "http://127.0.0.1:8000/"

// // Esta es la forma basica que usa JavaScrip pa comunicarse con mi API
// // fetch significa "ir a buscar" o "traer"
// fetch('http://127.0.0.1:8000/users')
//     .then(response => response.json ) // Convierte la respuesta a un JSON
//     .then(data => console.log(data)) // Pa q use los datos
//     .catch(error => console.log(error)) // por si hay error

/* Para definir constants (no puede cambiar) usa const 'SCREAMING_SNAKE_CASE'
para definir una variable (su valor puede cambiar despues) usa 'let camelCase' */
const API_URL = 'http://127.0.0.1:8000'
let juegoFavorito = 'Esto puede variar'

/* Función para obtener TODOS los usuarios, async indica que la funcion puede tomar pausas en lo que se esta ejecutando
Sin async no puedes usar await, pq fallaran */
async function loadUsers() {
    try {
        /* Hace la peticion a esta url, y await impide que continue sin tener fetch completo
        el $ es pa anidar las strings, como hacer: "http://127.0.0.1:8000/" + "/users"  */
        const response = await fetch('${API_URL}/users') 
        
        /* Manejo de errores, el ! significa no, es como decir "If the response is not ok, show this error" 
        Aqui muestras el mensaje de error tecnico, un mensaje corto para el dev especificando que salio mal (en este caso devuelves el status)*/
        if (!response.ok) {
            throw new Error('Response not OK. HTTP ${response.status}')
        }
        
        // Convierte la respuesta a JSON y espera a q termine, y luego muestra los usuarios
        const users = await response.json()
        showUsers(usuarios)
    } 
        // Si no funciono el try
        catch (error) {
        console.error(error) // Show in console the complete error for debugging
        showError('No se pudieron cargar los usuarios') // Este es pal usuario pq modifica el html
    
    }
}

// Función para mostrar los usuarios en la página
function showUsers(users) {
    // A esa parte especifica del html le asignas el nombre 'contenedor' pa usarlo en la function
    const container = document.getElementById('usuarios-contenedor')
    container.innerHTML = '' // Limpiar contenido anterior

    // Si no hay users en la db, mostras msj de error en esa parte del html
    if (users.length === 0) {
        container.innerHTML = '<p>No hay usuarios</p>'
        return // Todo termina aqui con el return 
    }
 
    /* Usuarios es un array (en este caso es una lista de dicts), forEach es una funcion q toma otra funcion como argumento */
    users.forEach(user => {
        /* Por cada usuario (asi es como llamaste a los elementos del array) crea un div en memoria, y a eso lo llamaras card*/
        const card = document.createElement('div')
        /* A ese div le asignas la clase 'usuario-card' para llamarlo desde el CSS pa editar el div y lo q contiene, tmb puede ser
        para llamarla desde otra funcion en JavaScript eso es como hacer <div class='usuario-card'></div> */
        card.className = 'usuario-card'

        /* Ahora dentro del div que creaste, agregas los key,value del dict usuario (accedes a los valores haciendo usuario.key
        y las key son los nombres de las columnas en la database*/
        card.innerHTML = `
            <p><strong>ID:</strong> ${user.id}</p>
            <p><strong>Username:</strong> ${user.username}</p>
            <p><strong>Email:</strong> ${user.email}</p>
        `
        // Agregas la card al contenedor en el HTML, card es un 'child' pq hay muchos jaksj
        container.appendChild(card)
    })
}

// Función para crear un usuario
async function createUser() {
    // Crea las variables para almacenar los valores que ingresaron en los <input> de los HTML, .value es especifico para inputs
    const username = document.getElementById('username').value
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value

    // Validación básica, es como hacer if not username or not email or not password
    if (!username || !email || !password) {
        showError('Por favor completa todos los campos')
        return
    }

    try {
        const response = await fetch(`${API_URL}/users`, {
            // Defines el metodo que usaras, el predeterminado es GET
            method: 'POST',
            // Los headers son info extra sobre la peticion, es metadata
            headers: {
                // Especificas el tipo de dato q le envias al servidor (siempre es json)
                'Content-Type': 'application/json'
            },
            // Convertis el objeto a JSON
            body: JSON.stringify({
                /*Los nombres de la izquierda son los nombre de instancia de clase en UserCreate de schemas.py
                y al mismo tiempo coincide con los nombres de columnas de la tabla q llama la API*/
                username: username,
                email: email,
                password: password
            })
        })

        // Manejo de datos del gigante fetch anterior
        if (!response.ok) {
            throw new Error('Error creating the user. HTTP ${response.status}')
        }

        // Convertis la response a json, asi luego puedes acceder a sus valores por si los ocupas, o solo para ofrecer mejor UX
        const newUser = await response.json()
        showSucces(`Usuario ${nuevoUsuario.username} creado exitosamente`)
        
        // Limpiar formulario (se tiene q usar .value para inputs)
        document.getElementById('username').value = ''
        document.getElementById('email').value = ''
        document.getElementById('password').value = ''
        
        /* Recargar lista para q el cliente no tenga que reiniciar manualmente el sitio web si quiere ver el usuario en la lista
        de usuarios que genera el boton. */
        loadUsers()
    } catch (error) {
        console.error(error)
        showError('No se pudo crear el usuario')
    }
}

// Función para mostrar mensajes de error
function showError(message) {
    const container = document.getElementById('usuarios-contenedor')
    // Create the div that is going to store the error message
    const div = document.createElement('div')
    div.className = 'error' //For CSS propouses
    // Defines the text content for the div, it's a good alternative for .innerHTML when you only want to add text
    div.textContent(message)
    // Adds it to the start o the container
    container.prepend(div)
}

// Función para mostrar mensajes de éxito (the only thing that changes with showError is the className and the name of the function)
function showSucces(message) {
    const container = document.getElementById('usuarios-contenedor')
    const div = document.createElement('div')
    div.className = 'succes'
    div.textContent(message)
    container.prepend(div)
}

// Event listeners (cuando carga la página) 
document.addEventListener('DOMContentLoaded', function() {
    /* Con'DOMContentLoaded', JavaScript espera a q el HTML termine de cargar 
    para ejecutar lo de abajo, pero en este caso espera acciones del usuario (click) */
    document.getElementById('cargar-btn').addEventListener('click', loadUsers())
    // .addEventListener('event', function) Cuando ocurra X evento ejecuta Y funcion
    document.getElementById('crear-btn').addEventListener('click', createUser())
})

