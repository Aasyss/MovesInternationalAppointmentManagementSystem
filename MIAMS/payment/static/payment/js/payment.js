document.addEventListener('DOMContentLoaded', function() {
    const stripe = Stripe('pk_test_51NszRaDB62Qu8opnwq7aT31qzXqXkPacWtXms8NSQLdYrrfGnFdin0ui1PDMKp0Xx4refg9oAT4Qi3Auu6FUOHhE00Bhi0AIa8');

    const elements = stripe.elements();
    const cardElement = elements.create('card');

    cardElement.mount('#card-element');

    const form = document.getElementById('payment-form');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const { paymentIntent, error } = await stripe.confirmCardPayment(
            clientSecret, {
                payment_method: {
                    card: cardElement,
                }
            }
        );

        if (error) {
            console.error(error);
        } else {
            // Handle successful payment
            // For example, you can submit the form to a Django view for further processing
            form.submit();
        }
    });
});
