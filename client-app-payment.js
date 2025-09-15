// Nouvelle fonction de confirmation avec paiement
showBookingConfirmation(bookingNumber, bookingData, paymentResult) {
    const confirmationHtml = `
        <div class="modal fade" id="confirmationModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-success text-white">
                        <h5 class="modal-title"> Réservation Confirmée</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>📋 Détails de la Réservation</h6>
                                <ul class="list-unstyled">
                                    <li><strong>Numéro:</strong> ${bookingNumber}</li>
                                    <li><strong>Passager:</strong> ${bookingData.passenger_name}</li>
                                    <li><strong>Téléphone:</strong> ${bookingData.passenger_phone}</li>
                                    <li><strong>Email:</strong> ${bookingData.passenger_email}</li>
                                    <li><strong>Places:</strong> ${bookingData.seat_count}</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>💳 Détails du Paiement</h6>
                                <ul class="list-unstyled">
                                    <li><strong>Montant:</strong> ${bookingData.total_amount}€</li>
                                    <li><strong>Méthode:</strong> ${paymentResult?.payment_method || bookingData.payment_method}</li>
                                    <li><strong>Transaction:</strong> ${paymentResult?.transaction_id || 'N/A'}</li>
                                    <li><strong>Statut:</strong> <span class="badge bg-success">Payé</span></li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="alert alert-info mt-3">
                            <h6>📱 Prochaines Étapes:</h6>
                            <ul class="mb-0">
                                <li>Un email de confirmation a été envoyé à ${bookingData.passenger_email}</li>
                                <li>Présentez-vous 30 minutes avant le départ</li>
                                <li>Munissez-vous d'une pièce d'identité valide</li>
                                <li>Votre numéro de réservation: <strong>${bookingNumber}</strong></li>
                            </ul>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" onclick="window.print()">
                            🖨️ Imprimer
                        </button>
                        <button type="button" class="btn btn-success" data-bs-dismiss="modal">
                            ✅ Terminé
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Supprimer l'ancienne modal si elle existe
    const existingModal = document.getElementById('confirmationModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Ajouter la nouvelle modal
    document.body.insertAdjacentHTML('beforeend', confirmationHtml);
    
    // Afficher la modal
    const modal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    modal.show();
    
    // Nettoyer après fermeture
    document.getElementById('confirmationModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}