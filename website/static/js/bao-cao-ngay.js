let table1 = new DataTable('#dataTable1', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    lengthMenu: [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    order: [[0, "desc"]],
    drawCallback: function(settings) {
        let totalNewRevenue = 0;
        let totalAdvanceBudget = 0;
        let totalRealBudget = 0;
        let totalPhone = 0;
        let totalMess = 0;

        let data = this.api().rows({ page: 'current' }).data();

        data.each(function(row) {
            totalNewRevenue += parseInt(row[1].replace(/[^0-9.-]+/g, "")) || 0;
            totalAdvanceBudget += parseInt(row[2].replace(/[^0-9.-]+/g, "")) || 0;
            totalRealBudget += parseInt(row[3].replace(/[^0-9.-]+/g, "")) || 0;
            totalPhone += parseInt(row[6].replace(/[^0-9.-]+/g, "")) || 0;
            totalMess += parseInt(row[8].replace(/[^0-9.-]+/g, "")) || 0;
        });

        let totalCPP = parseInt(totalRealBudget / totalPhone) || 0;
        let totalCPR = (parseFloat(totalNewRevenue / totalRealBudget * 100) || 0).toFixed(2);
        let totalPPM = (parseFloat(totalPhone / totalMess * 100) || 0).toFixed(2);
        let totalBPM = parseInt(totalRealBudget / totalMess) || 0;

        $('#total-newRevenue').html(totalNewRevenue.toLocaleString() + " VND");
        $('#total-advanceBudget').html(totalAdvanceBudget.toLocaleString() + " VND");
        $('#total-realBudget').html(totalRealBudget.toLocaleString() + " VND");
        $('#total-cpp').html(totalCPP.toLocaleString() + " VND");
        $('#total-cpr').html(totalCPR.toLocaleString() + "%");
        $('#total-phoneNumber').html(totalPhone.toLocaleString());
        $('#total-ppm').html(totalPPM.toLocaleString() + "%");
        $('#total-mess').html(totalMess.toLocaleString());
        $('#total-bpm').html(totalBPM.toLocaleString() + " VND");
    }
});


document.getElementById('dateInput').addEventListener('change', function() {
    const selectedDate = dateInput.value;
    const baseUrl = "/bao-cao-ngay";
    const [year, month, day] = selectedDate.split('-');
    const newUrl = `${baseUrl}/${year}-${month}-${day}`;
    window.location.href = newUrl;
});


function nextDay() {
    const selectedDate = dateInput.value;
    const currentDate = new Date(selectedDate);
    currentDate.setDate(currentDate.getDate() + 1);
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const newUrl = `/bao-cao-ngay/${year}-${month}-${day}`;
    window.location.href = newUrl;
}

function lastDay() {
    const selectedDate = dateInput.value;
    const currentDate = new Date(selectedDate);
    currentDate.setDate(currentDate.getDate() - 1);
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const newUrl = `/bao-cao-ngay/${year}-${month}-${day}`;
    window.location.href = newUrl;
}