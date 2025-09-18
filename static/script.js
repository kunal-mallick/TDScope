document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("prediction-form");
  const predictBtn = document.getElementById("predict-btn");
  const clearBtn = document.getElementById("clear-btn");
  const resultDiv = document.getElementById("result");

  // Predict button click
  predictBtn.addEventListener("click", async () => {
    const formData = {};
    const inputs = form.querySelectorAll("input");
    inputs.forEach(input => {
      formData[input.name] = parseFloat(input.value); // convert to float
    });

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (data.tds !== undefined) {
        // Example: color-code based on TDS thresholds
        let color = "green";
        if (data.tds > 1000) color = "red";
        else if (data.tds > 500) color = "orange";

        resultDiv.innerHTML = `Predicted TDS: <span style="color:${color}">${data.tds}</span>`;
      } else if (data.error) {
        resultDiv.innerHTML = `<span style="color:red">${data.error}</span>`;
      }

    } catch (err) {
      console.error(err);
      resultDiv.innerHTML = `<span style="color:red">Error predicting TDS</span>`;
    }
  });

  // Clear button resets to default values
  clearBtn.addEventListener("click", () => {
    const inputs = form.querySelectorAll("input");
    inputs.forEach(input => {
      input.value = input.defaultValue; // reset to default
    });
    resultDiv.innerHTML = "";
  });
});
