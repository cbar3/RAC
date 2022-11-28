const stripe = require("stripe")("pk_test_51M8pKPDX0d0RP5ri6t5BjxdzIVy5wnGNz5WKzobrheABZ7NMCMXGW5nEWechvvHDilJ1ClxV3ENjoToaJH46QgKp00tKcTIAV3");
const express = require('express');
const app = express();
app.set('trust proxy', true);

app.post('/create-confirm-intent', async (req, res) => {
  try {
    const intent = = await stripe.paymentIntents.create({
      confirm: true,
      amount: 1099,
      currency: 'usd',
      automatic_payment_methods: {enabled: true},
      payment_method: req.body, // the PaymentMethod ID sent by your client
    });
    res.json({
      client_secret: intent.client_secret,
      status: intent.status
    });
  } catch (err) {
    res.json({
      error: err
    })
  }
});

app.listen(3000, () => {
  console.log('Running on port 3000');
});