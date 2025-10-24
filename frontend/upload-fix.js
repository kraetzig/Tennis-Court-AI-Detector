// Exemplo de código para upload de imagem que funciona com Lambda
async function uploadImage(file) {
    try {
        // Mostrar loading
        document.getElementById('loading').style.display = 'block';
        
        // Converter imagem para base64
        const base64 = await fileToBase64(file);
        
        // Fazer chamada para API Gateway
        const response = await fetch('/api/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                image: base64,
                filename: file.name,
                contentType: file.type
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Upload successful:', result);
        
        // Esconder loading
        document.getElementById('loading').style.display = 'none';
        
        return result;
        
    } catch (error) {
        console.error('Upload failed:', error);
        document.getElementById('loading').style.display = 'none';
        alert('Erro no upload: ' + error.message);
    }
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(',')[1]);
        reader.onerror = error => reject(error);
    });
}

// Event listener para input de arquivo
document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        uploadImage(file);
    }
});
