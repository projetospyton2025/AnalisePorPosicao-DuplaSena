// Script principal da aplicação
console.log('Dupla Sena - Análise Por Posição carregado');

// Função para formatar números com casas decimais
function formatNumber(num, decimals = 2) {
    return parseFloat(num).toFixed(decimals);
}

// Função para criar badge de número
function createNumberBadge(numero, className = 'bg-primary') {
    return `<span class="badge ${className} fs-6">${numero}</span>`;
}
