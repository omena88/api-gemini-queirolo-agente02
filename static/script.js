document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const pdfFileInput = document.getElementById('pdfFile');
    const requirementsContainer = document.getElementById('requirements');
    const errorMessage = document.getElementById('error');

    // Actualizar el texto del label cuando se selecciona un archivo
    pdfFileInput.addEventListener('change', (e) => {
        const fileName = e.target.files[0]?.name || 'Seleccionar PDF';
        document.querySelector('.file-label').textContent = fileName;
    });

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = pdfFileInput.files[0];
        if (!file) {
            showError('Por favor, selecciona un archivo PDF');
            return;
        }

        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showError('El archivo debe ser un PDF');
            return;
        }

        // Mostrar indicador de carga
        requirementsContainer.innerHTML = '<p class="placeholder">Procesando PDF...</p>';
        hideError();

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('https://apps-api-queirolo-agente02.di8b44.easypanel.host/upload-pdf/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }

            const data = await response.json();
            
            // Mostrar los requisitos extraídos
            if (data.requirements) {
                requirementsContainer.innerHTML = `<pre>${data.requirements}</pre>`;
            } else {
                requirementsContainer.innerHTML = '<p class="placeholder">No se encontraron requisitos en el PDF</p>';
            }

        } catch (error) {
            showError(`Error al procesar el PDF: ${error.message}`);
            requirementsContainer.innerHTML = '<p class="placeholder">Los requisitos extraídos aparecerán aquí...</p>';
        }
    });

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add('show');
    }

    function hideError() {
        errorMessage.classList.remove('show');
    }
}); 