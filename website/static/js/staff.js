function editStaff(staff) {
    var editStaffModal = document.getElementById('edit-staff');
    editStaffModal.querySelector('#edit-id').value = staff.id;
    editStaffModal.querySelector('#edit-name').value = staff.name;
    editStaffModal.querySelector('#edit-address').value = staff.address;
    editStaffModal.querySelector('#edit-phone').value = staff.phone;
    editStaffModal.querySelector('#edit-cccd').value = staff.cccd;
    editStaffModal.querySelector('#edit-email').value = staff.email;
    editStaffModal.querySelector('#edit-dob').value = convertDate(staff.dob);
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

function deleteStaff(staffID) {
    fetch(`/staff/delete/${staffID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/staff";
    });
}
