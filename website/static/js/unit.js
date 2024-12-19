function editUnit(unit) {
    var editUnitModal = document.getElementById('edit-unit');
    editUnitModal.querySelector('#edit-id').value = unit.id;
    editUnitModal.querySelector('#edit-name').value = unit.name;
    editUnitModal.querySelector('#edit-note').value = unit.note;
}

function deleteUnit(unitID) {
    fetch(`/unit/delete/${unitID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/unit";
    });
}
