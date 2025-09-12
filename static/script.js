document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("prediction-form");
  const predictBtn = document.getElementById("predict-btn");
  const clearBtn = document.getElementById("clear-btn");
  const resultBox = document.getElementById("result");

  // Predict button handler
  predictBtn.addEventListener("click", async function () {
    // Collect values as floats
    const formData = {};
    form.querySelectorAll("input").forEach((input) => {
      const val = parseFloat(input.value);
      formData[input.name] = isNaN(val) ? 0.0 : val;
    });

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (data.error) {
        resultBox.textContent = "Error: " + data.error;
        resultBox.style.color = "red";
      } else {
        resultBox.textContent = `Predicted TDS: ${data.TDS_prediction}`;
        resultBox.style.color = "green";
      }
    } catch (error) {
      resultBox.textContent = "Error connecting to server.";
      resultBox.style.color = "red";
    }
  });

  // Clear button handler
  clearBtn.addEventListener("click", function () {
    form.querySelectorAll("input").forEach((input) => (input.value = ""));
    resultBox.textContent = "";
  });
});
