const generateBtn =
    document.getElementById("generateBtn");

let recipeText = "";

generateBtn.addEventListener(
    "click",
    async () => {

        console.log("BUTTON CLICKED");

        const recipe_type =
            document.getElementById("recipeType").value;

        const ingredients =
            document.getElementById("ingredients").value;

        const prep_time =
            document.getElementById("prepTime").value;

        try {

            const response =
                await fetch("/generate_recipe", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        recipe_type,
                        ingredients,
                        prep_time
                    })
                });

            const data =
                await response.json();

            if (data.success) {

                recipeText = data.recipe;

                document.getElementById(
                    "recipeOutput"
                ).innerText = recipeText;

            } else {

                document.getElementById(
                    "recipeOutput"
                ).innerText =
                    "Error: " + data.error;
            }

        } catch (error) {

            console.error(error);

            document.getElementById(
                "recipeOutput"
            ).innerText =
                "An error occurred. Check browser console.";
        }
    }
);