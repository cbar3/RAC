// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = Stripe('pk_test_51M8pKPDX0d0RP5ri6t5BjxdzIVy5wnGNz5WKzobrheABZ7NMCMXGW5nEWechvvHDilJ1ClxV3ENjoToaJH46QgKp00tKcTIAV3');

const options = {
  clientSecret: '{{CLIENT_SECRET}}',
  // Fully customizable with appearance API.
  appearance: {/*...*/},
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
const elements = stripe.elements(options);

// Create and mount the Payment Element
const paymentElement = elements.create('payment', {
  layout: {
    type: 'accordion',
    defaultCollapsed: false,
    radios: true,
    spacedAccordionItems: false
  }
});

const handleServerResponse = async (response) => {
  if (response.error) {
    // Show error from server on payment form
  } else if (response.requires_action) {
    // Use Stripe.js to handle the required next action
    const {
      error: errorAction,
      paymentIntent
    } = await stripe.handleNextAction({
      clientSecret: response.payment_intent_client_secret
    });


    if (errorAction) {
      // Show error from Stripe.js in payment form
    } else {
      // Actions handled, show success message
    }
  } else {
    // No actions needed, show success message
  }
}

paymentElement.mount('#payment-element');

const form = document.getElementById('payment-form');


paymentElement.mount('#payment-element');

async function handleDiscountCode(code) {
  const { newAmount } = await applyDiscountCode(code);
  elements.update({ amount: newAmount });
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {error} = await stripe.confirmPayment({
    //`Elements` instance that was used to create the Payment Element
    elements,
    confirmParams: {
      return_url: 'https://example.com/order/123/complete',
    },
  });

  if (error) {
    // This point will only be reached if there is an immediate error when
    // confirming the payment. Show error to your customer (for example, payment
    // details incomplete)
    const messageContainer = document.querySelector('#error-message');
    messageContainer.textContent = error.message;
  } else {
    // Your customer will be redirected to your `return_url`. For some payment
    // methods like iDEAL, your customer will be redirected to an intermediate
    // site first to authorize the payment, then redirected to the `return_url`.
  }
});