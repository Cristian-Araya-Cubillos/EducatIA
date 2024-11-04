async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');

    const userMessage = userInput.value;
    if (userMessage.trim() === '') return;

    // Crear el contenedor para el mensaje del usuario
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('message', 'user');
    
    // Crear el alert y agregarlo al contenedor
    const userAlert = document.createElement('div');
    userAlert.classList.add('alert', 'alert-info', 'rounded');
    userAlert.textContent = userMessage;
    
    userMessageElement.appendChild(userAlert);
    chatBox.appendChild(userMessageElement);

    // Limpiar el campo de entrada
    userInput.value = '';

    // Desplazar hacia abajo el chat
    chatBox.scrollTop = chatBox.scrollHeight;

    // Hacer la solicitud al servidor
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mensaje: userMessage })
    });

    if (response.ok) {
        const data = await response.json();

        // Crear el contenedor para la respuesta del asistente
        const assistantMessageElement = document.createElement('div');
        assistantMessageElement.classList.add('message', 'assistant');
        
        // Crear el alert y agregarlo al contenedor
        const assistantAlert = document.createElement('div');
        assistantAlert.classList.add('alert', 'alert-light', 'rounded');
        assistantAlert.textContent = data.respuesta;

        assistantMessageElement.appendChild(assistantAlert);
        chatBox.appendChild(assistantMessageElement);

        // Desplazar hacia abajo el chat
        chatBox.scrollTop = chatBox.scrollHeight;

        // Renderizar las ecuaciones matemáticas (si es necesario)
        MathJax.typesetPromise();

        // Enfocar el campo de entrada para escribir el próximo mensaje
        userInput.focus();
    } else {
        console.error("Error al obtener respuesta del servidor");
    }
}

// Función para desplazar el chat al final al cargar la página
window.addEventListener('load', () => {
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});