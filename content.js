// Allergens and icon paths
const ALLERGENS = {
    milk: "icons/milk.png", //<a href="https://www.flaticon.com/free-icons/milk" title="milk icons">Milk icons created by Freepik - Flaticon</a>
    eggs: "icons/eggs.png", //<a href="https://www.flaticon.com/free-icons/egg" title="egg icons">Egg icons created by Roundicons Premium - Flaticon</a>
    fish: "icons/fish.png", //<a href="https://www.flaticon.com/free-icons/fish" title="fish icons">Fish icons created by Freepik - Flaticon</a>
    shellfish: "icons/shellfish.png", //<a href="https://www.flaticon.com/free-icons/shrimp" title="Shrimp icons">Shrimp icons created by Good Ware - Flaticon</a>
    "tree nuts": "icons/tree_nuts.png", //<a href="https://www.flaticon.com/free-icons/almond" title="almond icons">Almond icons created by Konkapp - Flaticon</a>
    peanuts: "icons/peanuts.png", //<a href="https://www.flaticon.com/free-icons/peanuts" title="peanuts icons">Peanuts icons created by Freepik - Flaticon</a>
    wheat: "icons/wheat.png", //<a href="https://www.flaticon.com/free-icons/wheat" title="wheat icons">Wheat icons created by max.icons - Flaticon</a>
    soy: "icons/soy.png", //<a href="https://www.flaticon.com/free-icons/soy" title="soy icons">Soy icons created by Freepik - Flaticon</a>
    sesame: "icons/sesame.png" //<a href="https://www.flaticon.com/free-icons/sesame" title="sesame icons">Sesame icons created by Freepik - Flaticon</a>
  };
  
  function extractIngredients() {
    const ingredientElements = document.querySelectorAll(".pantry--ui.ingredient_ingredient__rfjvs");
    const ingredients = Array.from(ingredientElements).map(el => el.innerText.trim());
    console.log("Extracted ingredients:", ingredients);  // debug output
    return ingredients;
  }
  
  
  function injectAllergenIcons(allergens) {
    console.log("Allergens passed to icon injector:", allergens);
    const target = document.querySelector("dt.pantry--ui-strong");
    if (!target) {
        console.warn("Could not find 'Total Time' section for icon injection.");
        return;
    }
    // Container for icons
    const iconDT = document.createElement("dt");
    iconDT.style.display = "flex";
    iconDT.style.alignItems = "center";
    iconDT.style.gap = "6px";
    iconDT.style.margin = "6px 0";

    // Adding the icons
    allergens.forEach(allergen => {
      const img = document.createElement("img");
      const filename = allergen.replace(/\s+/g, '_').toLowerCase(); // e.g. "tree nuts" → "tree_nuts"
    img.src = chrome.runtime.getURL(`icons/${filename}.png`);
      img.alt = allergen;
      img.title = allergen;
      img.style.height = "24px";
      img.style.width = "24px";
      img.style.objectFit = "contain";
      iconDT.appendChild(img);
      console.log(`Adding icon: ${allergen} → ${img.src}`);
    });

    // Adds empty <dd> to keep alignment
    const iconDD = document.createElement("dd");
    iconDD.style.margin = "0";
    iconDD.style.padding = "0";

    // Insert above Total Time
    target.parentNode.insertBefore(iconDT, target);
    target.parentNode.insertBefore(iconDD, target);
  }
  
  function detectAllergens(ingredients) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(
        {
          type: "FETCH_ALLERGENS",
          ingredients: ingredients
        },
        response => {
          if (response && response.allergens) {
            resolve(response.allergens);
          } else {
            console.error("Error from background:", response?.error);
            resolve([]);
          }
        }
      );
    });
  }
  
  // Run on page load
  (async () => {
    const ingredients = extractIngredients();
    const allergens = await detectAllergens(ingredients);
    injectAllergenIcons(allergens);
  })();
  