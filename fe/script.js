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
async function cargarUsuarios() {
    try {
        /* Hace la peticion a esta url, y await impide que continue sin tener fetch completo
        el $ es pa anidar las strings, como hacer: "http://127.0.0.1:8000/" + "/users"  */
        const response = await fetch('${API_URL}/users') 
        
        // Manejo de errores, el ! significa no, es como decir "If the response is not ok, show this error"
        if (!response.ok) {
            throw new Error('Error al cargar usuarios')
        }
        
        const usuarios = await response.json()
        mostrarUsuarios(usuarios)
    } catch (error) {
        console.error(error)
        mostrarError('No se pudieron cargar los usuarios')
    }
}

// Función para mostrar los usuarios en la página
function mostrarUsuarios(usuarios) {
    const contenedor = document.getElementById('usuarios-contenedor')
    contenedor.innerHTML = '' // Limpiar contenido anterior

    if (usuarios.length === 0) {
        contenedor.innerHTML = '<p>No hay usuarios</p>'
        return
    }

    usuarios.forEach(usuario => {
        const card = document.createElement('div')
        card.className = 'usuario-card'
        card.innerHTML = `
            <p><strong>ID:</strong> ${usuario.id}</p>
            <p><strong>Username:</strong> ${usuario.username}</p>
            <p><strong>Email:</strong> ${usuario.email}</p>
        `
        contenedor.appendChild(card)
    })
}

// Función para crear un usuario
async function crearUsuario() {
    const username = document.getElementById('username').value
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value

    // Validación básica
    if (!username || !email || !password) {
        mostrarError('Por favor completa todos los campos')
        return
    }

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        })

        if (!response.ok) {
            throw new Error('Error al crear usuario')
        }

        const nuevoUsuario = await response.json()
        mostrarExito(`Usuario ${nuevoUsuario.username} creado exitosamente`)
        
        // Limpiar formulario
        document.getElementById('username').value = ''
        document.getElementById('email').value = ''
        document.getElementById('password').value = ''
        
        // Recargar lista
        cargarUsuarios()
    } catch (error) {
        console.error(error)
        mostrarError('No se pudo crear el usuario')
    }
}

// Función para mostrar mensajes de error
function mostrarError(mensaje) {
    const contenedor = document.getElementById('usuarios-contenedor')
    const div = document.createElement('div')
    div.className = 'error'
    div.textContent = mensaje
    contenedor.prepend(div)
}

// Función para mostrar mensajes de éxito
function mostrarExito(mensaje) {
    const contenedor = document.getElementById('usuarios-contenedor')
    const div = document.createElement('div')
    div.className = 'success'
    div.textContent = mensaje
    contenedor.prepend(div)
}

// Event listeners (cuando carga la página)
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('cargar-btn').addEventListener('click', cargarUsuarios)
    document.getElementById('crear-btn').addEventListener('click', crearUsuario)
})