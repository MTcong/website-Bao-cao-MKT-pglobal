function editSupplier(supplier) {
    var editsupplierModal = document.getElementById('edit-supplier');
    editsupplierModal.querySelector('#edit-id').value = supplier.id;
    editsupplierModal.querySelector('#edit-name').value = supplier.name;
    editsupplierModal.querySelector('#edit-address').value = supplier.address;
    editsupplierModal.querySelector('#edit-phone').value = supplier.phone;
    editsupplierModal.querySelector('#edit-cccd').value = supplier.cccd;
    editsupplierModal.querySelector('#edit-email').value = supplier.email;
    editsupplierModal.querySelector('#edit-dob').value = convertDate(supplier.dob);
    editsupplierModal.querySelector('#edit-stk').value = supplier.stk;
    editsupplierModal.querySelector('#edit-note').value = supplier.note;
    editsupplierModal.querySelector('#edit-bank').value = supplier.bank_shortName;
    editsupplierModal.querySelector('#edit-bank_id').value = supplier.bank_id;
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

function deleteSupplier(supplierID) {
    fetch(`/supplier/delete/${supplierID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/supplier";
    });
}

function handleBankSelection(inputId, datalistId, outputId) {
    document.getElementById(inputId).addEventListener("input", function() {
      const input = this.value;
      const options = document.getElementById(datalistId).querySelectorAll("option");
      const selectedId = Array.from(options).find(option => option.value === input)?.getAttribute("data-id") || "";
      document.getElementById(outputId).value = selectedId;
    });
}
  
handleBankSelection("selected_bank", "browsers", "bank_id");
handleBankSelection("edit-bank", "edit-browsers", "edit-bank_id");
  