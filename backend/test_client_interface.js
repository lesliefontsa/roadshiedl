/**
 * Script de test pour l'interface client - Test du paiement Stripe
 * À exécuter dans la console du navigateur sur http://127.0.0.1:8009/client-dashboard/
 */

console.log("🧪 Test de l'interface de paiement Stripe");

// Fonction pour tester la sélection d'un voyage et l'ouverture du modal de paiement
function testPaymentFlow() {
    console.log("1. Recherche des voyages disponibles...");
    
    // Simuler la sélection d'un voyage
    const firstTripCard = document.querySelector('.trip-card');
    if (!firstTripCard) {
        console.error("❌ Aucun voyage trouvé sur la page");
        return;
    }
    
    console.log("✅ Voyage trouvé");
    
    // Simuler la sélection du prix (aller simple)
    const priceOption = firstTripCard.querySelector('.price-option');
    if (priceOption) {
        priceOption.click();
        console.log("✅ Prix sélectionné");
    }
    
    // Simuler le clic sur "Réserver"
    const bookButton = firstTripCard.querySelector('.btn-book');
    if (bookButton && !bookButton.disabled) {
        bookButton.click();
        console.log("✅ Modal de paiement ouvert");
        
        // Vérifier que le modal est bien affiché
        setTimeout(() => {
            const modal = document.getElementById('paymentModal');
            if (modal && modal.classList.contains('show')) {
                console.log("✅ Modal de paiement affiché correctement");
                testModalContent();
            } else {
                console.error("❌ Modal de paiement non affiché");
            }
        }, 500);
    } else {
        console.error("❌ Bouton de réservation non disponible");
    }
}

// Fonction pour tester le contenu du modal
function testModalContent() {
    console.log("2. Test du contenu du modal...");
    
    // Vérifier les champs requis
    const requiredFields = [
        'passenger-name',
        'passenger-phone', 
        'passenger-email',
        'cardholder-name',
        'seat-count'
    ];
    
    let allFieldsPresent = true;
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field) {
            console.error(`❌ Champ manquant: ${fieldId}`);
            allFieldsPresent = false;
        }
    });
    
    if (allFieldsPresent) {
        console.log("✅ Tous les champs du formulaire sont présents");
    }
    
    // Vérifier la présence de Stripe Elements
    const cardElement = document.getElementById('card-element');
    if (cardElement) {
        console.log("✅ Élément Stripe Card présent");
    } else {
        console.error("❌ Élément Stripe Card manquant");
    }
    
    // Vérifier les montants
    const totalAmount = document.getElementById('total-amount');
    const paymentAmount = document.getElementById('payment-amount');
    
    if (totalAmount && paymentAmount) {
        console.log(`✅ Montants affichés: Total=${totalAmount.textContent}, Paiement=${paymentAmount.textContent}`);
    }
}

// Fonction pour remplir le formulaire de test
function fillTestData() {
    console.log("3. Remplissage des données de test...");
    
    const testData = {
        'passenger-name': 'Jean Dupont',
        'passenger-phone': '+225 01 02 03 04 05',
        'passenger-email': 'jean.dupont@example.com',
        'cardholder-name': 'Jean Dupont',
        'billing-address': '123 Rue de la Paix, Abidjan, Côte d\'Ivoire'
    };
    
    Object.entries(testData).forEach(([fieldId, value]) => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.value = value;
            console.log(`✅ ${fieldId}: ${value}`);
        }
    });
    
    console.log("📝 Données de test remplies");
    console.log("💳 Pour tester Stripe, utilisez le numéro de carte test: 4242 4242 4242 4242");
    console.log("📅 Date d'expiration: 12/25, CVC: 123");
}

// Fonction principale de test
function runFullTest() {
    console.log("🚀 Démarrage du test complet de l'interface de paiement");
    console.log("=" * 50);
    
    // Vérifier que Stripe est chargé
    if (typeof stripe === 'undefined') {
        console.error("❌ Stripe n'est pas chargé");
        return;
    }
    console.log("✅ Stripe chargé");
    
    // Démarrer le test
    testPaymentFlow();
    
    // Remplir les données après un délai
    setTimeout(() => {
        fillTestData();
    }, 1000);
}

// Message d'aide
console.log("🎯 Instructions de test:");
console.log("1. Exécutez: runFullTest()");
console.log("2. Le modal de paiement s'ouvrira automatiquement");
console.log("3. Les données de test seront remplies");
console.log("4. Utilisez la carte test 4242 4242 4242 4242 pour tester");
console.log("━".repeat(50));