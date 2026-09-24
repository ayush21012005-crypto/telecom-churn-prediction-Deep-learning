// =========================================================
// API URL
// =========================================================

const API_URL = "http://127.0.0.1:8000/predict";


// =========================================================
// ELEMENTS
// =========================================================

const form =
    document.getElementById("predictionForm");

const predictBtn =
    document.getElementById("predictBtn");

const buttonText =
    document.getElementById("buttonText");

const loader =
    document.getElementById("loader");

const emptyResult =
    document.getElementById("emptyResult");

const predictionResult =
    document.getElementById("predictionResult");

const errorResult =
    document.getElementById("errorResult");

const predictionTitle =
    document.getElementById("predictionTitle");

const predictionStatus =
    document.getElementById("predictionStatus");

const predictionIcon =
    document.getElementById("predictionIcon");

const probabilityText =
    document.getElementById("probabilityText");

const progressBar =
    document.getElementById("progressBar");

const predictionValue =
    document.getElementById("predictionValue");

const riskValue =
    document.getElementById("riskValue");

const errorMessage =
    document.getElementById("errorMessage");

const resetBtn =
    document.getElementById("resetBtn");

const retryBtn =
    document.getElementById("retryBtn");


// =========================================================
// GET FORM DATA
// =========================================================

function getFormData() {

    return {

        SeniorCitizen:
            Number(
                document.getElementById(
                    "SeniorCitizen"
                ).value
            ),

        tenure:
            Number(
                document.getElementById(
                    "tenure"
                ).value
            ),

        MonthlyCharges:
            Number(
                document.getElementById(
                    "MonthlyCharges"
                ).value
            ),

        TotalCharges:
            Number(
                document.getElementById(
                    "TotalCharges"
                ).value
            ),

        gender:
            document.getElementById(
                "gender"
            ).value,

        Partner:
            document.getElementById(
                "Partner"
            ).value,

        Dependents:
            document.getElementById(
                "Dependents"
            ).value,

        PhoneService:
            document.getElementById(
                "PhoneService"
            ).value,

        MultipleLines:
            document.getElementById(
                "MultipleLines"
            ).value,

        InternetService:
            document.getElementById(
                "InternetService"
            ).value,

        OnlineSecurity:
            document.getElementById(
                "OnlineSecurity"
            ).value,

        OnlineBackup:
            document.getElementById(
                "OnlineBackup"
            ).value,

        DeviceProtection:
            document.getElementById(
                "DeviceProtection"
            ).value,

        TechSupport:
            document.getElementById(
                "TechSupport"
            ).value,

        StreamingTV:
            document.getElementById(
                "StreamingTV"
            ).value,

        StreamingMovies:
            document.getElementById(
                "StreamingMovies"
            ).value,

        Contract:
            document.getElementById(
                "Contract"
            ).value,

        PaperlessBilling:
            document.getElementById(
                "PaperlessBilling"
            ).value,

        PaymentMethod:
            document.getElementById(
                "PaymentMethod"
            ).value

    };

}


// =========================================================
// LOADING STATE
// =========================================================

function setLoading(isLoading) {

    if (isLoading) {

        predictBtn.disabled = true;

        buttonText.textContent =
            "Analyzing Customer...";

        loader.classList.remove("hidden");

    } else {

        predictBtn.disabled = false;

        buttonText.textContent =
            "Predict Customer Churn";

        loader.classList.add("hidden");

    }

}


// =========================================================
// SHOW ERROR
// =========================================================

function showError(message) {

    emptyResult.classList.add("hidden");

    predictionResult.classList.add("hidden");

    errorResult.classList.remove("hidden");

    errorMessage.textContent = message;

}


// =========================================================
// SHOW PREDICTION
// =========================================================

function showPrediction(data) {

    emptyResult.classList.add("hidden");

    errorResult.classList.add("hidden");

    predictionResult.classList.remove("hidden");


    const probability =
        Number(data.churn_percentage);


    probabilityText.textContent =
        `${probability.toFixed(2)}%`;


    predictionValue.textContent =
        data.prediction;


    riskValue.textContent =
        data.status;


    predictionTitle.textContent =
        data.result;


    predictionStatus.textContent =
        data.status;


    // Animate progress bar

    progressBar.style.width = "0%";


    setTimeout(() => {

        progressBar.style.width =
            `${probability}%`;

    }, 100);


    // -----------------------------------------------------
    // CHURN
    // -----------------------------------------------------

    if (data.prediction === 1) {

        predictionIcon.textContent = "!";

        predictionIcon.style.background =
            "#fee2e2";

        predictionIcon.style.color =
            "#dc2626";

        predictionStatus.style.color =
            "#dc2626";

        riskValue.style.color =
            "#dc2626";

    }


    // -----------------------------------------------------
    // STAY
    // -----------------------------------------------------

    else {

        predictionIcon.textContent = "✓";

        predictionIcon.style.background =
            "#dcfce7";

        predictionIcon.style.color =
            "#16a34a";

        predictionStatus.style.color =
            "#16a34a";

        riskValue.style.color =
            "#16a34a";

    }

}


// =========================================================
// FORM SUBMIT
// =========================================================

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // Browser validation
        if (!form.checkValidity()) {

            form.reportValidity();

            return;

        }


        setLoading(true);


        // Hide old result

        emptyResult.classList.add("hidden");

        predictionResult.classList.add("hidden");

        errorResult.classList.add("hidden");


        const customerData =
            getFormData();


        try {

            const response =
                await fetch(
                    API_URL,
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(
                                customerData
                            )

                    }
                );


            // Handle HTTP errors

            if (!response.ok) {

                let errorText =
                    "API request failed.";

                try {

                    const errorData =
                        await response.json();

                    if (
                        errorData.detail
                    ) {

                        if (
                            Array.isArray(
                                errorData.detail
                            )
                        ) {

                            errorText =
                                errorData.detail
                                    .map(
                                        error =>
                                            error.msg
                                    )
                                    .join(", ");

                        } else {

                            errorText =
                                errorData.detail;

                        }

                    }

                } catch (e) {

                    // Ignore JSON parsing error

                }


                throw new Error(
                    errorText
                );

            }


            const result =
                await response.json();


            // Backend error

            if (
                result.success === false
            ) {

                throw new Error(
                    result.error ||
                    "Prediction failed."
                );

            }


            // Show prediction

            showPrediction(result);


        } catch (error) {

            console.error(
                "Prediction error:",
                error
            );


            // Connection error

            if (
                error.name ===
                "TypeError"
            ) {

                showError(
                    "Unable to connect to the FastAPI server. Make sure the backend is running on http://127.0.0.1:8000"
                );

            } else {

                showError(
                    error.message ||
                    "Something went wrong while predicting churn."
                );

            }

        } finally {

            setLoading(false);

        }

    }
);


// =========================================================
// RESET
// =========================================================

resetBtn.addEventListener(
    "click",
    function () {

        form.reset();

        predictionResult.classList.add(
            "hidden"
        );

        errorResult.classList.add(
            "hidden"
        );

        emptyResult.classList.remove(
            "hidden"
        );

        progressBar.style.width =
            "0%";

    }
);


// =========================================================
// RETRY
// =========================================================

retryBtn.addEventListener(
    "click",
    function () {

        errorResult.classList.add(
            "hidden"
        );

        emptyResult.classList.remove(
            "hidden"
        );

    }
);
