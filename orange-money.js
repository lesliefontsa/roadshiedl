// Fonction pour basculer les champs de paiement - XAF uniquement
function togglePaymentFields() {
    const paymentMethod = document.getElementById('paymentMethod').value;
    const orangeFields = document.getElementById('orangeMoneyFields');
    const seatCount = parseInt(document.getElementById('seatCount').value) || 1;
    
    // Cacher tous les champs spécifiques
    if (orangeFields) orangeFields.style.display = 'none';
    
    // Afficher les champs selon la méthode
    if (paymentMethod === 'orange_money' && orangeFields) {
        orangeFields.style.display = 'block';
    }
    
    // Mettre à jour le calcul des frais en XAF
    updatePaymentSummary(paymentMethod, seatCount);
}

// Fonction pour mettre à jour le résumé de paiement - XAF uniquement
function updatePaymentSummary(paymentMethod, seatCount) {
    const basePrice = 15000; // Prix de base en XAF
    
    let serviceFees = 0;
    const totalPrice = basePrice * seatCount;
    
    // Calculer les frais selon la méthode
    if (paymentMethod === 'orange_money') {
        serviceFees = Math.max(100, totalPrice * 0.015); // 1.5% avec minimum 100 XAF
    }
    
    // Mettre à jour l'affichage
    const priceDisplay = document.getElementById('pricePerSeat');
    const seatCountDisplay = document.getElementById('seatCountDisplay');
    const serviceFeesDisplay = document.getElementById('serviceFees');
    const totalDisplay = document.getElementById('totalAmount');
    
    if (priceDisplay) priceDisplay.textContent = `${basePrice.toLocaleString('fr-FR')} XAF`;
    if (seatCountDisplay) seatCountDisplay.textContent = seatCount;
    if (serviceFeesDisplay) serviceFeesDisplay.textContent = `${serviceFees.toLocaleString('fr-FR')} XAF`;
    if (totalDisplay) totalDisplay.textContent = `${(totalPrice + serviceFees).toLocaleString('fr-FR')} XAF`;
}

// Mettre à jour le nombre de places
function updateSeatCount() {
    const seatCount = parseInt(document.getElementById('seatCount').value) || 1;
    const paymentMethod = document.getElementById('paymentMethod').value;
    updatePaymentSummary(paymentMethod, seatCount);
}

// Validation du numéro Orange Money Cameroun
function validateOrangeNumber(phoneNumber) {
    const orangePatterns = [
        /^\+237\s?69\d{7}$/, // Orange 69X XXX XXX
        /^\+237\s?65\d{7}$/  // Orange 65X XXX XXX
    ];
    
    return orangePatterns.some(pattern => pattern.test(phoneNumber));
}