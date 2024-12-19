function editCustomer(customer) {
    var editCustomerModal = document.getElementById('edit-customer');
    editCustomerModal.querySelector('#edit-id').value = customer.id;
    editCustomerModal.querySelector('#edit-name').value = customer.name;
    editCustomerModal.querySelector('#edit-address').value = customer.address;
    editCustomerModal.querySelector('#edit-phone').value = customer.phone;
    editCustomerModal.querySelector('#edit-cccd').value = customer.cccd;
    editCustomerModal.querySelector('#edit-email').value = customer.email;
    editCustomerModal.querySelector('#edit-dob').value = convertDate(customer.dob);
    editCustomerModal.querySelector('#edit-note').value = customer.note;
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

function deleteCustomer(customerID) {
    fetch(`/customer/delete/${customerID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/customer";
    });
}
