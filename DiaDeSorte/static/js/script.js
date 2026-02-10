// Dia de Sorte - Utility Functions

/**
 * Formata número para moeda brasileira
 */
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

/**
 * Formata data para padrão brasileiro
 */
function formatarData(dataStr) {
    const partes = dataStr.split('/');
    if (partes.length === 3) {
        return `${partes[0]}/${partes[1]}/${partes[2]}`;
    }
    return dataStr;
}

/**
 * Mostra notificação toast
 */
function mostrarNotificacao(mensagem, tipo = 'info') {
    const toastContainer = document.createElement('div');
    toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
    toastContainer.style.zIndex = '11';
    
    const cores = {
        'success': 'bg-success',
        'error': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    };
    
    const cor = cores[tipo] || cores['info'];
    
    toastContainer.innerHTML = `
        <div class="toast ${cor} text-white" role="alert">
            <div class="toast-body">
                ${mensagem}
            </div>
        </div>
    `;
    
    document.body.appendChild(toastContainer);
    
    const toast = new bootstrap.Toast(toastContainer.querySelector('.toast'));
    toast.show();
    
    setTimeout(() => {
        toastContainer.remove();
    }, 5000);
}

/**
 * Copia texto para área de transferência
 */
async function copiarParaClipboard(texto) {
    try {
        await navigator.clipboard.writeText(texto);
        mostrarNotificacao('Copiado para área de transferência!', 'success');
    } catch (err) {
        console.error('Erro ao copiar:', err);
        mostrarNotificacao('Erro ao copiar', 'error');
    }
}

/**
 * Valida se é um número válido do Dia de Sorte
 */
function validarNumero(num) {
    const numero = parseInt(num);
    return numero >= 1 && numero <= 31;
}

/**
 * Gera cor baseada em valor
 */
function gerarCor(valor, min, max) {
    const porcentagem = ((valor - min) / (max - min)) * 100;
    
    if (porcentagem > 75) return 'success';
    if (porcentagem > 50) return 'info';
    if (porcentagem > 25) return 'warning';
    return 'secondary';
}

// Console log para debug
console.log('Dia de Sorte - Scripts carregados');
