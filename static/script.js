function calculateDTI() {
    const income = document.getElementById("income").value;
    const expenses = document.getElementById("expenses").value;

    fetch("/calculate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ income, expenses })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("dtiResult").innerHTML =
            `DTI: ${data.dti}%<br>${data.status}`;

        if (data.show_ltv) {
            document.getElementById("ltvSection").style.display = "block";
        }
    });
}

function calculateLTV() {
    const property_value = document.getElementById("propertyValue").value;
    const loan_amount = document.getElementById("loanAmount").value;

    fetch("/calculate_ltv", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ property_value, loan_amount })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("ltvResult").innerHTML =
            `LTV: ${data.ltv}%<br>${data.status}`;
    });
}
