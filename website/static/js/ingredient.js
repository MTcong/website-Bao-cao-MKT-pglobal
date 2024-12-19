function editIngredient(ingredient) {
    var editIngredientModal = document.getElementById('edit-ingredient');
    editIngredientModal.querySelector('#edit-id').value = ingredient.id;
    editIngredientModal.querySelector('#edit-name').value = ingredient.name;
    editIngredientModal.querySelector('#edit-long').value = ingredient.long;
    editIngredientModal.querySelector('#edit-wide').value = ingredient.wide;
    editIngredientModal.querySelector('#edit-high').value = ingredient.high;
    editIngredientModal.querySelector('#edit-buy').value = ingredient.buy;
    editIngredientModal.querySelector('#edit-sale').value = ingredient.sale;
    editIngredientModal.querySelector('#edit-note').value = ingredient.note;
    editIngredientModal.querySelector('#edit-unit_id').value = ingredient.unit_id;
    editIngredientModal.querySelector('#edit-selected_unit').value = ingredient.unit_name;
}

function convertDate(dateStr) {
    var parts = dateStr.split('/');
    var day = parts[0];
    var month = parts[1];
    var year = parts[2];

    // Rearrange the components to the desired format
    var newDateStr = `${year}-${month}-${day}`;
    return newDateStr;
}

function deleteIngredient(ingredientID) {
    fetch(`/ingredient/delete/${ingredientID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/ingredient";
    });
}

function handleUnitSelection(inputId, datalistId, outputId) {
    document.getElementById(inputId).addEventListener("input", function() {
      const input = this.value;
      const options = document.getElementById(datalistId).querySelectorAll("option");
      const selectedId = Array.from(options).find(option => option.value === input)?.getAttribute("data-id") || "";
      document.getElementById(outputId).value = selectedId;
    });
}
  
handleUnitSelection("selected_unit", "browsers", "unit_id");
handleUnitSelection("edit-selected_unit", "edit-browsers", "edit-unit_id");
  