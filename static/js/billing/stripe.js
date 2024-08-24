console.log("Sanity check!");

// Get Stripe publishable key
fetch("/billing/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // サブスクリプションの識別（月額）
        const subscription_monthly_limited = "monthly_limited";
        // サブスクリプションの識別（年額）
        const subscription_yearly_limited = "yearly_limited";

        // チェックアウトURL（一部）
        const checkout_url = "/billing/create-checkout-session?query=";
        // チェックアウトURL（月額）
        const checkout_url_monthly_limited = checkout_url + subscription_monthly_limited;
        // チェックアウトURL（年額）
        const checkout_url_yearly_limited = checkout_url + subscription_yearly_limited;
        

        //
        // サブスクリプション（月額）
        //
        let submitBtnMonthlyLimited = document.querySelector("#checkout_monthly_limited");
        if (submitBtnMonthlyLimited !== null) {
            submitBtnMonthlyLimited.addEventListener("click", () => {
                // Get Checkout Session ID
                fetch(checkout_url_monthly_limited)
                    .then((result) => { return result.json(); })
                    .then((data) => {
                        console.log(data);
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({ sessionId: data.sessionId })
                    })
                    .then((res) => {
                        console.log(res);
                    });
            });
        }

        //
        // サブスクリプション（年額）
        //
        let submitBtnYearlyLimited = document.querySelector("#checkout_yearly_limited");
        if (submitBtnYearlyLimited !== null) {
            submitBtnYearlyLimited.addEventListener("click", () => {
                // Get Checkout Session ID
                fetch(checkout_url_yearly_limited)
                    .then((result) => { return result.json(); })
                    .then((data) => {
                        console.log(data);
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({ sessionId: data.sessionId })
                    })
                    .then((res) => {
                        console.log(res);
                    });
            });
        }
    });
